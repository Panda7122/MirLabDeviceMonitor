import asyncio
import traceback

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import ssh_utils, storage
from utils.pagination import paginate, send_paginated

HELP_TEXT = (
    "**/monitor 指令列表**\n"
    "`/monitor add_user device username password` — 註冊你在該裝置上的 SSH 登入資訊（每個 Discord 帳號、每台裝置各自獨立）\n"
    "`/monitor remove_user device` — 移除你在該裝置上註冊的登入資訊\n"
    "`/monitor show_user_list` — 顯示你自己註冊過的裝置與使用者名稱（不會顯示密碼）\n"
    "`/monitor add_device name ip port` — 新增裝置到 device list\n"
    "`/monitor remove_device name` — 從 device list 移除裝置\n"
    "`/monitor show_device_list` — 顯示目前的 device list\n"
    "`/monitor add_filter username name` — 將 process name 加入該使用者的 filter list（顯示 pid 清單時會被隱藏）\n"
    "`/monitor remove_filter username name` — 從該使用者的 filter list 移除 process name\n"
    "`/monitor show_pid_list device [hide_system]` — 使用你在該裝置註冊的帳密登入，顯示你自己的 pid / process name / command 清單（hide_system 預設為 True，可設 False 顯示 COMMAND 開頭為 / 的系統行程）\n"
    "`/monitor reminder device pid` — 使用你在該裝置註冊的帳密監控 pid，執行完畢時在本頻道 mention 你\n"
    "`/monitor help` — 顯示這份說明\n"
    "\n"
    "`show_pid_list` 和 `reminder` 都需要先用 `add_user` 註冊該裝置的登入資訊。\n"
    "除了 reminder 完成時的通知會公開顯示在頻道，其餘指令的結果都只有你自己看得到。"
)


class MonitorCog(commands.GroupCog, group_name="monitor"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # key: (device_name, pid) -> asyncio.Task
        self.active_reminders: dict[tuple[str, int], asyncio.Task] = {}

    async def cog_unload(self) -> None:
        for task in self.active_reminders.values():
            task.cancel()

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        # Safety net: without this, an exception not already caught inside a
        # command (e.g. after `defer()`) leaves the interaction stuck showing
        # "thinking..." forever instead of ever resolving.
        traceback.print_exception(type(error), error, error.__traceback__)
        message = f"執行指令時發生未預期的錯誤：{error}"
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="help", description="顯示 /monitor 指令說明")
    async def help_(self, interaction: discord.Interaction):
        await interaction.response.send_message(HELP_TEXT, ephemeral=True)

    # ---- user list: per-(Discord user, device) SSH login ----

    @app_commands.command(name="add_user", description="註冊你在該裝置上的 SSH 登入資訊")
    @app_commands.describe(device="裝置名稱", username="該裝置上的 SSH 使用者名稱", password="該裝置上的 SSH 密碼")
    async def add_user(self, interaction: discord.Interaction, device: str, username: str, password: str):
        device_data = await storage.get_device(device)
        if device_data is None:
            await interaction.response.send_message(f"找不到裝置 `{device}`，請確認裝置名稱是否正確。", ephemeral=True)
            return

        is_new = await storage.set_user_credential(str(interaction.user.id), device, username, password)
        if is_new:
            await interaction.response.send_message(f"已註冊你在裝置 `{device}` 上的登入資訊（使用者：`{username}`）。", ephemeral=True)
        else:
            await interaction.response.send_message(f"已更新你在裝置 `{device}` 上的登入資訊（使用者：`{username}`）。", ephemeral=True)

    @app_commands.command(name="remove_user", description="移除你在該裝置上註冊的登入資訊")
    @app_commands.describe(device="裝置名稱")
    async def remove_user(self, interaction: discord.Interaction, device: str):
        removed = await storage.remove_user_credential(str(interaction.user.id), device)
        if removed:
            await interaction.response.send_message(f"已移除你在裝置 `{device}` 上註冊的登入資訊。", ephemeral=True)
        else:
            await interaction.response.send_message(f"你尚未在裝置 `{device}` 上註冊登入資訊。", ephemeral=True)

    @app_commands.command(name="show_user_list", description="顯示你自己註冊過的裝置與使用者名稱")
    async def show_user_list(self, interaction: discord.Interaction):
        credentials = await storage.list_user_credentials(str(interaction.user.id))
        rows = [f"- {device}: {cred['username']}" for device, cred in credentials.items()]
        pages = paginate("Your registered logins", rows)
        await send_paginated(interaction, pages, use_followup=False)

    # ---- device list ----

    @app_commands.command(name="add_device", description="新增裝置到 device list")
    @app_commands.describe(name="裝置名稱", ip="裝置 IP", port="SSH port")
    async def add_device(self, interaction: discord.Interaction, name: str, ip: str, port: int):
        device = {"name": name, "ip": ip, "port": port}
        added = await storage.add_device(device)
        if added:
            await interaction.response.send_message(f"已新增裝置 `{name}` ({ip}:{port})。", ephemeral=True)
        else:
            await interaction.response.send_message(f"裝置 `{name}` 已經存在。", ephemeral=True)

    @app_commands.command(name="remove_device", description="從 device list 移除裝置")
    @app_commands.describe(name="裝置名稱")
    async def remove_device(self, interaction: discord.Interaction, name: str):
        removed = await storage.remove_device(name)
        if removed:
            await interaction.response.send_message(f"已移除裝置 `{name}`。", ephemeral=True)
        else:
            await interaction.response.send_message(f"找不到裝置 `{name}`。", ephemeral=True)

    @app_commands.command(name="show_device_list", description="顯示目前的 device list")
    async def show_device_list(self, interaction: discord.Interaction):
        devices = await storage.load_devices()
        rows = [f"- {d['name']} ({d['ip']}:{d['port']})" for d in devices]
        pages = paginate("Device List", rows)
        await send_paginated(interaction, pages, use_followup=False)

    # ---- filter list ----

    @app_commands.command(name="add_filter", description="將 process name 加入使用者的 filter list")
    @app_commands.describe(username="process 擁有者的使用者名稱", name="要隱藏的 process name")
    async def add_filter(self, interaction: discord.Interaction, username: str, name: str):
        added = await storage.add_filter(username, name)
        if added:
            await interaction.response.send_message(f"已將 `{name}` 加入使用者 `{username}` 的 filter list。", ephemeral=True)
        else:
            await interaction.response.send_message(f"`{name}` 已經在使用者 `{username}` 的 filter list 中。", ephemeral=True)

    @app_commands.command(name="remove_filter", description="從使用者的 filter list 移除 process name")
    @app_commands.describe(username="process 擁有者的使用者名稱", name="要移除的 process name")
    async def remove_filter(self, interaction: discord.Interaction, username: str, name: str):
        removed = await storage.remove_filter(username, name)
        if removed:
            await interaction.response.send_message(f"已將 `{name}` 從使用者 `{username}` 的 filter list 移除。", ephemeral=True)
        else:
            await interaction.response.send_message(f"使用者 `{username}` 的 filter list 中找不到 `{name}`。", ephemeral=True)

    # ---- pid list ----

    @app_commands.command(name="show_pid_list", description="使用你註冊的帳密登入裝置，顯示你自己的 pid / process name / command 清單")
    @app_commands.describe(device="裝置名稱", hide_system="是否隱藏 COMMAND 開頭為 / 的系統行程（預設：是）")
    async def show_pid_list(self, interaction: discord.Interaction, device: str, hide_system: bool = True):
        device_data = await storage.get_device(device)
        if device_data is None:
            await interaction.response.send_message(f"找不到裝置 `{device}`，請確認裝置名稱是否正確。", ephemeral=True)
            return

        credential = await storage.get_user_credential(str(interaction.user.id), device)
        if credential is None:
            await interaction.response.send_message(
                f"你尚未在裝置 `{device}` 上註冊登入資訊，請先使用 `/monitor add_user device:{device} ...` 註冊。",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        username = credential["username"]
        try:
            processes = await ssh_utils.get_process_list(device_data, username, credential["password"])
        except ssh_utils.SSHCommandError as e:
            await interaction.followup.send(f"取得裝置 `{device}` 的 pid 清單失敗：{e}", ephemeral=True)
            return

        filters = await storage.load_filters()
        hidden_names = filters.get(username, [])
        processes = [
            p for p in processes
            if p["owner"] == username
            and p["name"] not in hidden_names
            and (not hide_system or not p["command"].startswith("/"))
        ]

        if not processes:
            await interaction.followup.send(f"裝置 `{device}` 上目前沒有屬於 `{username}` 的行程。", ephemeral=True)
            return

        header = f"{'PID':>8}  {'OWNER':<15}  {'NAME':<20}  COMMAND"
        rows = [
            f"{p['pid']:>8}  {p['owner']:<15}  {p['name']:<20}  {p['command'] or '-'}"
            for p in processes
        ]
        pages = paginate(header, rows)
        await send_paginated(interaction, pages, use_followup=True)

    # ---- reminder ----

    @app_commands.command(name="reminder", description="使用你註冊的帳密監控裝置上的 pid，執行完畢時在本頻道通知你")
    @app_commands.describe(device="裝置名稱", pid="要監控的 pid")
    async def reminder(self, interaction: discord.Interaction, device: str, pid: int):
        device_data = await storage.get_device(device)
        if device_data is None:
            await interaction.response.send_message(f"找不到裝置 `{device}`，請確認裝置名稱是否正確。", ephemeral=True)
            return

        credential = await storage.get_user_credential(str(interaction.user.id), device)
        if credential is None:
            await interaction.response.send_message(
                f"你尚未在裝置 `{device}` 上註冊登入資訊，請先使用 `/monitor add_user device:{device} ...` 註冊。",
                ephemeral=True,
            )
            return

        key = (device, pid)
        if key in self.active_reminders:
            await interaction.response.send_message(f"已經在監控裝置 `{device}` 的 pid `{pid}` 了。", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        username = credential["username"]
        password = credential["password"]
        try:
            alive = await ssh_utils.is_pid_alive(device_data, username, password, pid)
        except ssh_utils.SSHCommandError as e:
            await interaction.followup.send(f"連線裝置 `{device}` 失敗：{e}", ephemeral=True)
            return

        if not alive:
            await interaction.followup.send(f"裝置 `{device}` 上找不到執行中的 pid `{pid}`。", ephemeral=True)
            return

        await interaction.followup.send(
            f"開始監控裝置 `{device}` 的 pid `{pid}`，執行完畢時會在此頻道通知你。", ephemeral=True
        )
        task = self.bot.loop.create_task(
            self._watch_pid(
                interaction.channel, interaction.user, device, device_data, username, password, pid, key
            )
        )
        self.active_reminders[key] = task

    async def _watch_pid(
        self,
        channel: discord.abc.Messageable,
        author: discord.abc.User,
        device_name: str,
        device_data: dict,
        username: str,
        password: str,
        pid: int,
        key: tuple[str, int],
    ):
        try:
            while True:
                await asyncio.sleep(config.PID_POLL_INTERVAL_SECONDS)
                try:
                    alive = await ssh_utils.is_pid_alive(device_data, username, password, pid)
                except ssh_utils.SSHCommandError as e:
                    await channel.send(
                        f"監控裝置 `{device_name}` 的 pid `{pid}` 時發生錯誤，已停止監控：{e}"
                    )
                    return
                if not alive:
                    await channel.send(
                        f"{author.mention} 裝置 `{device_name}` 的 pid `{pid}` 已執行完畢。"
                    )
                    return
        except asyncio.CancelledError:
            raise
        finally:
            self.active_reminders.pop(key, None)


async def setup(bot: commands.Bot):
    await bot.add_cog(MonitorCog(bot))
