# Lab Device Monitor Discord Bot

A Discord bot for monitoring processes on lab machines over SSH — list who's
running what on a device, hide noise you don't care about, and get pinged
when a specific process finishes.

All commands are Discord **slash commands** under the `/monitor` group.
Every reply is ephemeral (only you can see it) except the "process finished"
notification from `/monitor reminder`, which is posted publicly in the
channel where it was started.

## Commands

| Command | Description |
| --- | --- |
| `/monitor add_user <username>` | Add a username to the user list |
| `/monitor remove_user <username>` | Remove a username from the user list |
| `/monitor show_user_list` | Show the current user list |
| `/monitor add_device <name> <ip> <port>` | Add a device (SSH host + port) to the device list |
| `/monitor remove_device <name>` | Remove a device from the device list |
| `/monitor show_device_list` | Show the current device list |
| `/monitor add_filter <username> <name>` | Hide a process name from that user's `show_pid_list` output |
| `/monitor remove_filter <username> <name>` | Un-hide a previously filtered process name |
| `/monitor show_pid_list <device>` | List pid / owner / process name / full command for a device |
| `/monitor reminder <device> <pid>` | Get pinged in this channel when that pid finishes |
| `/monitor help` | Show this command list in Discord |

`show_pid_list` only shows processes whose owner is in the user list, whose
name isn't in that owner's filter list, and whose command doesn't start with
`/` (which filters out system daemons that show as an absolute path, leaving
user-run commands like `python3 train.py`). Long results are paginated with
⬅️/➡️ buttons.

## Setup

1. Create the environment and install dependencies:
   ```bash
   conda create -n lab_device_monitor_dcbot python=3.11 -y
   conda activate lab_device_monitor_dcbot
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill it in:
   - `DISCORD_TOKEN` — from the Discord Developer Portal (Bot page)
   - `GUILD_ID` — optional; set this to your server's ID while developing so
     slash commands sync instantly (a few seconds) instead of globally
     (which can take up to an hour to show up)
   - `SSH_DEFAULT_USER` / `SSH_DEFAULT_KEY_PATH` / `SSH_DEFAULT_PASSWORD` —
     one SSH identity used for every device (key auth recommended)
3. In the Discord Developer Portal, make sure the bot's invite URL includes
   the `applications.commands` scope (required for slash commands), then
   invite it to your server.
4. Run it:
   ```bash
   python bot.py
   ```

## Requirements on each monitored device

- SSH access reachable at the `ip`/`port` you register with `add_device`,
  using the single identity configured in `.env`.
- `bash` available on the device (used for `mapfile` when reading
  `/proc/<pid>/cmdline` without forking a subprocess per process — this is
  what keeps `show_pid_list` fast even with hundreds of running processes).
- Reading another user's `/proc/<pid>/cmdline` requires either being that
  user or root; if the SSH identity is an unprivileged user, `show_pid_list`
  will only be able to show full commands for that user's own processes.

## Data files

Everything is plain JSON under `data/`, read/written directly (no database):

- `data/users.json` — `list[str]` of usernames
- `data/devices.json` — `list[{"name", "ip", "port"}]`
- `data/filters.json` — `dict[username, list[process_name]]`

## Project layout

```
bot.py                 # entrypoint; syncs the slash command tree on startup
config.py              # reads .env
cogs/monitor.py         # all /monitor slash commands
utils/storage.py        # JSON read/write for users/devices/filters
utils/ssh_utils.py       # paramiko: run remote commands, list processes, check if a pid is alive
utils/pagination.py      # ephemeral pagination (Prev/Next button view)
data/                   # users.json, devices.json, filters.json
```
