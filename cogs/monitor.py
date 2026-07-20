import asyncio
import traceback

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import ssh_utils, storage
from utils.i18n import LANGUAGE_NAMES, t
from utils.pagination import paginate, send_paginated

LANGUAGE_CHOICES = [
    app_commands.Choice(name=name, value=code) for code, name in LANGUAGE_NAMES.items()
]


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
        lang = await storage.get_user_language(str(interaction.user.id))
        message = t(lang, "error.unexpected", error=error)
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="help", description="顯示 /monitor 指令說明")
    async def help_(self, interaction: discord.Interaction):
        lang = await storage.get_user_language(str(interaction.user.id))
        await interaction.response.send_message(t(lang, "help.text"), ephemeral=True)

    @app_commands.command(name="language", description="設定你的顯示語言 / Set your display language / 表示言語を設定")
    @app_commands.describe(lang="顯示語言 / Display language / 表示言語")
    @app_commands.choices(lang=LANGUAGE_CHOICES)
    async def language(self, interaction: discord.Interaction, lang: app_commands.Choice[str]):
        await storage.set_user_language(str(interaction.user.id), lang.value)
        await interaction.response.send_message(
            t(lang.value, "language.set", language_name=lang.name), ephemeral=True
        )

    # ---- user list: per-(Discord user, device) SSH login ----

    @app_commands.command(name="add_user", description="註冊你在該裝置上的 SSH 登入資訊")
    @app_commands.describe(device="裝置名稱", username="該裝置上的 SSH 使用者名稱", password="該裝置上的 SSH 密碼")
    async def add_user(self, interaction: discord.Interaction, device: str, username: str, password: str):
        lang = await storage.get_user_language(str(interaction.user.id))
        device_data = await storage.get_device(device)
        if device_data is None:
            await interaction.response.send_message(t(lang, "error.no_device", device=device), ephemeral=True)
            return

        is_new = await storage.set_user_credential(str(interaction.user.id), device, username, password)
        key = "add_user.registered" if is_new else "add_user.updated"
        await interaction.response.send_message(t(lang, key, device=device, username=username), ephemeral=True)

    @app_commands.command(name="remove_user", description="移除你在該裝置上註冊的登入資訊")
    @app_commands.describe(device="裝置名稱")
    async def remove_user(self, interaction: discord.Interaction, device: str):
        lang = await storage.get_user_language(str(interaction.user.id))
        removed = await storage.remove_user_credential(str(interaction.user.id), device)
        key = "remove_user.removed" if removed else "remove_user.not_found"
        await interaction.response.send_message(t(lang, key, device=device), ephemeral=True)

    @app_commands.command(name="show_user_list", description="顯示你自己註冊過的裝置與使用者名稱")
    async def show_user_list(self, interaction: discord.Interaction):
        lang = await storage.get_user_language(str(interaction.user.id))
        credentials = await storage.list_user_credentials(str(interaction.user.id))
        rows = [f"- {device}: {cred['username']}" for device, cred in credentials.items()]
        pages = paginate(t(lang, "show_user_list.title"), rows, lang)
        await send_paginated(interaction, pages, lang, use_followup=False)

    # ---- device list ----

    @app_commands.command(name="add_device", description="新增裝置到 device list")
    @app_commands.describe(name="裝置名稱", ip="裝置 IP", port="SSH port")
    async def add_device(self, interaction: discord.Interaction, name: str, ip: str, port: int):
        lang = await storage.get_user_language(str(interaction.user.id))
        device = {"name": name, "ip": ip, "port": port}
        added = await storage.add_device(device)
        if added:
            await interaction.response.send_message(t(lang, "add_device.added", name=name, ip=ip, port=port), ephemeral=True)
        else:
            await interaction.response.send_message(t(lang, "add_device.exists", name=name), ephemeral=True)

    @app_commands.command(name="remove_device", description="從 device list 移除裝置")
    @app_commands.describe(name="裝置名稱")
    async def remove_device(self, interaction: discord.Interaction, name: str):
        lang = await storage.get_user_language(str(interaction.user.id))
        removed = await storage.remove_device(name)
        key = "remove_device.removed" if removed else "remove_device.not_found"
        await interaction.response.send_message(t(lang, key, name=name), ephemeral=True)

    @app_commands.command(name="show_device_list", description="顯示目前的 device list")
    async def show_device_list(self, interaction: discord.Interaction):
        lang = await storage.get_user_language(str(interaction.user.id))
        devices = await storage.load_devices()
        rows = [f"- {d['name']} ({d['ip']}:{d['port']})" for d in devices]
        pages = paginate(t(lang, "show_device_list.title"), rows, lang)
        await send_paginated(interaction, pages, lang, use_followup=False)

    # ---- filter list ----

    @app_commands.command(name="add_filter", description="將 process name 加入使用者的 filter list")
    @app_commands.describe(username="process 擁有者的使用者名稱", name="要隱藏的 process name")
    async def add_filter(self, interaction: discord.Interaction, username: str, name: str):
        lang = await storage.get_user_language(str(interaction.user.id))
        added = await storage.add_filter(username, name)
        key = "add_filter.added" if added else "add_filter.exists"
        await interaction.response.send_message(t(lang, key, username=username, name=name), ephemeral=True)

    @app_commands.command(name="remove_filter", description="從使用者的 filter list 移除 process name")
    @app_commands.describe(username="process 擁有者的使用者名稱", name="要移除的 process name")
    async def remove_filter(self, interaction: discord.Interaction, username: str, name: str):
        lang = await storage.get_user_language(str(interaction.user.id))
        removed = await storage.remove_filter(username, name)
        key = "remove_filter.removed" if removed else "remove_filter.not_found"
        await interaction.response.send_message(t(lang, key, username=username, name=name), ephemeral=True)

    # ---- pid list ----

    @app_commands.command(name="show_pid_list", description="使用你註冊的帳密登入裝置，顯示你自己的 pid / process name / command 清單")
    @app_commands.describe(device="裝置名稱", hide_system="是否隱藏 COMMAND 開頭為 / 的系統行程（預設：是）")
    async def show_pid_list(self, interaction: discord.Interaction, device: str, hide_system: bool = True):
        lang = await storage.get_user_language(str(interaction.user.id))
        device_data = await storage.get_device(device)
        if device_data is None:
            await interaction.response.send_message(t(lang, "error.no_device", device=device), ephemeral=True)
            return

        credential = await storage.get_user_credential(str(interaction.user.id), device)
        if credential is None:
            await interaction.response.send_message(t(lang, "error.not_registered", device=device), ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        username = credential["username"]
        try:
            processes = await ssh_utils.get_process_list(device_data, username, credential["password"])
        except ssh_utils.SSHCommandError as e:
            await interaction.followup.send(t(lang, "show_pid_list.fetch_failed", device=device, error=e), ephemeral=True)
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
            await interaction.followup.send(t(lang, "show_pid_list.empty", device=device, username=username), ephemeral=True)
            return

        header = f"{'PID':>8}  {'OWNER':<15}  {'NAME':<20}  COMMAND"
        rows = [
            f"{p['pid']:>8}  {p['owner']:<15}  {p['name']:<20}  {p['command'] or '-'}"
            for p in processes
        ]
        pages = paginate(header, rows, lang)
        await send_paginated(interaction, pages, lang, use_followup=True)

    # ---- reminder ----

    @app_commands.command(name="reminder", description="使用你註冊的帳密監控裝置上的 pid，執行完畢時在本頻道通知你")
    @app_commands.describe(device="裝置名稱", pid="要監控的 pid")
    async def reminder(self, interaction: discord.Interaction, device: str, pid: int):
        lang = await storage.get_user_language(str(interaction.user.id))
        device_data = await storage.get_device(device)
        if device_data is None:
            await interaction.response.send_message(t(lang, "error.no_device", device=device), ephemeral=True)
            return

        credential = await storage.get_user_credential(str(interaction.user.id), device)
        if credential is None:
            await interaction.response.send_message(t(lang, "error.not_registered", device=device), ephemeral=True)
            return

        key = (device, pid)
        if key in self.active_reminders:
            await interaction.response.send_message(t(lang, "reminder.already_monitoring", device=device, pid=pid), ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        username = credential["username"]
        password = credential["password"]
        try:
            alive = await ssh_utils.is_pid_alive(device_data, username, password, pid)
        except ssh_utils.SSHCommandError as e:
            await interaction.followup.send(t(lang, "reminder.connect_failed", device=device, error=e), ephemeral=True)
            return

        if not alive:
            await interaction.followup.send(t(lang, "reminder.pid_not_found", device=device, pid=pid), ephemeral=True)
            return

        try:
            command = await ssh_utils.get_pid_command(device_data, username, password, pid)
        except ssh_utils.SSHCommandError:
            command = ""
        command_suffix = f"（`{command}`）" if command else ""

        await interaction.followup.send(
            t(lang, "reminder.started", device=device, pid=pid, command_suffix=command_suffix), ephemeral=True
        )
        task = self.bot.loop.create_task(
            self._watch_pid(
                interaction.channel, interaction.user, device, device_data,
                username, password, pid, command, key,
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
        command: str,
        key: tuple[str, int],
    ):
        command_suffix = f"（`{command}`）" if command else ""
        lang = await storage.get_user_language(str(author.id))
        try:
            while True:
                await asyncio.sleep(config.PID_POLL_INTERVAL_SECONDS)
                try:
                    alive = await ssh_utils.is_pid_alive(device_data, username, password, pid)
                except ssh_utils.SSHCommandError as e:
                    await channel.send(
                        t(lang, "reminder.watch_error", device=device_name, pid=pid, command_suffix=command_suffix, error=e)
                    )
                    return
                if not alive:
                    await channel.send(
                        t(
                            lang, "reminder.finished", mention=author.mention,
                            device=device_name, pid=pid, command_suffix=command_suffix,
                        )
                    )
                    return
        except asyncio.CancelledError:
            raise
        finally:
            self.active_reminders.pop(key, None)


async def setup(bot: commands.Bot):
    await bot.add_cog(MonitorCog(bot))
