import asyncio
import shlex

import paramiko

import config


class SSHCommandError(Exception):
    """Raised when connecting to or running a command on a device fails."""


def _run_command_raw_sync(device: dict, command: str) -> tuple[int, str, str]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=device["ip"],
            port=int(device["port"]),
            username=config.SSH_DEFAULT_USER,
            password=config.SSH_DEFAULT_PASSWORD,
            key_filename=config.SSH_DEFAULT_KEY_PATH,
            timeout=config.SSH_TIMEOUT_SECONDS,
            banner_timeout=config.SSH_TIMEOUT_SECONDS,
            auth_timeout=config.SSH_TIMEOUT_SECONDS,
        )
        _stdin, stdout, stderr = client.exec_command(command, timeout=config.SSH_TIMEOUT_SECONDS)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        exit_status = stdout.channel.recv_exit_status()
        return exit_status, out, err
    except paramiko.AuthenticationException as e:
        raise SSHCommandError(f"SSH 認證失敗: {e}") from e
    except (paramiko.SSHException, OSError) as e:
        raise SSHCommandError(f"無法連線到裝置 {device.get('name', device.get('ip'))}: {e}") from e
    finally:
        client.close()


async def run_command_raw(device: dict, command: str) -> tuple[int, str, str]:
    # asyncio.wait_for only stops *waiting*: paramiko's blocking calls run in a
    # real OS thread that can't be killed from here. On timeout that thread
    # keeps running until its own per-op SSH_TIMEOUT_SECONDS eventually unblocks
    # it; this wrapper just keeps the caller (a Discord interaction) from
    # hanging until then.
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_run_command_raw_sync, device, command),
            timeout=config.SSH_TOTAL_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError as e:
        name = device.get("name", device.get("ip"))
        raise SSHCommandError(
            f"裝置 {name} 執行指令逾時（超過 {config.SSH_TOTAL_TIMEOUT_SECONDS} 秒），可能是裝置負載過高或網路異常"
        ) from e


async def run_command(device: dict, command: str) -> str:
    exit_status, out, err = await run_command_raw(device, command)
    if exit_status != 0 and not out.strip():
        raise SSHCommandError(f"指令執行失敗 (exit {exit_status}): {err.strip() or command}")
    return out


_CMD_MARKER = "---CMD---"

# ps lists pid/owner/name; the /proc loop reconstructs each pid's full command
# line (like htop's "Command" column) from /proc/<pid>/cmdline in the same SSH
# round trip. cmdline is NUL-separated and empty for kernel threads or when the
# process has already exited, in which case the pid is just skipped.
#
# mapfile (a bash builtin) reads each cmdline file without forking a
# subprocess per pid — a naive `tr ... < file` loop forks twice per pid, which
# on a busy device with hundreds of processes made the whole call take so long
# it looked like the bot had frozen. Requires bash (hence the explicit
# `bash -c` wrapper below), bash >= 4.4 for `mapfile -d`.
_PROCESS_LIST_LOOP = (
    "for d in /proc/[0-9]*; do "
    "pid=${d#/proc/}; "
    'if [ -r "$d/cmdline" ]; then '
    'mapfile -d "" -t args < "$d/cmdline" 2>/dev/null; '
    # /proc files always report stat size 0, so emptiness has to be checked
    # via the array length after reading, not with a `-s` test beforehand.
    'if [ "${#args[@]}" -gt 0 ]; then printf "%s\\t%s\\n" "$pid" "${args[*]}"; fi; '
    "fi; "
    "done"
)
_PROCESS_LIST_SCRIPT = f"ps -eo pid=,user:32=,comm=\necho '{_CMD_MARKER}'\n{_PROCESS_LIST_LOOP}"


async def get_process_list(device: dict) -> list[dict]:
    """Returns a list of {"pid": int, "name": str, "owner": str, "command": str}."""
    output = await run_command(device, f"bash -c {shlex.quote(_PROCESS_LIST_SCRIPT)}")
    ps_part, _marker, cmd_part = output.partition(_CMD_MARKER)

    processes = []
    for line in ps_part.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 2)
        if len(parts) != 3:
            continue
        pid_str, owner, name = parts
        if not pid_str.isdigit():
            continue
        processes.append({"pid": int(pid_str), "owner": owner, "name": name, "command": ""})

    cmd_by_pid = {}
    for line in cmd_part.splitlines():
        if "\t" not in line:
            continue
        pid_str, cmd = line.split("\t", 1)
        pid_str = pid_str.strip()
        if pid_str.isdigit():
            cmd_by_pid[int(pid_str)] = cmd.strip()

    for p in processes:
        p["command"] = cmd_by_pid.get(p["pid"], "")
    return processes


async def is_pid_alive(device: dict, pid: int) -> bool:
    _exit_status, out, _err = await run_command_raw(device, f"ps -p {shlex.quote(str(pid))} -o pid=")
    return out.strip() != ""
