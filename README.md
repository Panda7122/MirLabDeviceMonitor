# Lab Device Monitor Discord Bot

A Discord bot for monitoring processes on lab machines over SSH — list your
own processes on a device, hide noise you don't care about, and get pinged
when a specific process finishes.

All commands are Discord **slash commands** under the `/monitor` group.
Every reply is ephemeral (only you can see it) except the "process finished"
notification from `/monitor reminder`, which is posted publicly in the
channel where it was started.

Each Discord user registers their **own SSH login per device** with
`add_user` — there's no shared/global SSH identity. `show_pid_list` and
`reminder` log in as that registered user and only ever show that user's own
processes, so different Discord users querying the same device only ever see
their own stuff.

## Commands

| Command | Description |
| --- | --- |
| `/monitor add_user <device> <username> <password>` | Register your SSH login for a device (per Discord account, per device) |
| `/monitor remove_user <device>` | Remove your registered login for a device |
| `/monitor show_user_list` | Show the devices *you've* registered logins for (usernames only, never passwords) |
| `/monitor add_device <name> <ip> <port>` | Add a device (SSH host + port) to the device list |
| `/monitor remove_device <name>` | Remove a device from the device list |
| `/monitor show_device_list` | Show the current device list |
| `/monitor add_filter <username> <name>` | Hide a process name from that user's `show_pid_list` output |
| `/monitor remove_filter <username> <name>` | Un-hide a previously filtered process name |
| `/monitor show_pid_list <device> [hide_system]` | Log in with your registered credentials and list your pid / process name / command on that device |
| `/monitor reminder <device> <pid>` | Log in with your registered credentials and get pinged in this channel when that pid finishes |
| `/monitor language <lang>` | Set your own display language: Traditional Chinese, English, or Japanese |
| `/monitor help` | Show this command list in Discord |

`show_pid_list` and `reminder` both require you to have run `add_user` for
that device first. `show_pid_list` shows only processes owned by your
registered username, minus anything in that username's filter list, and
(unless `hide_system:False`) minus processes whose command starts with `/`
(system daemons — leaves user-run commands like `python3 train.py`). Long
results are paginated with ⬅️/➡️ buttons.

Every reply is localized to whatever language you last set with
`/monitor language` (defaults to Traditional Chinese for anyone who hasn't
set one). This only affects the bot's reply text — not the slash command
names/descriptions shown in Discord's own command picker, which is a
separate, Discord-client-locale-based mechanism.

Besides the 3 real languages, `/monitor language` also has 3 easter-egg
voices that reword every message in-character: 女僕風格 (maid), 中二動漫風
(chuunibyou anime), and MyGO!!!!! 風格 (deadpan band-drama meme lines). Same
functionality, different flavor text. In `mygo` mode, error/confirmation/
reminder messages also attach a matching MyGO!!!!! meme image — curated by
hand in `utils/mygo_images.py` from real images on
[mygo.miyago9267.com](https://mygo.miyago9267.com/api/v1/images) (not fetched
live at runtime, so there's no external API dependency while the bot runs).

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
3. In the Discord Developer Portal, make sure the bot's invite URL includes
   the `applications.commands` scope (required for slash commands), then
   invite it to your server.
4. Run it:
   ```bash
   python bot.py
   ```

## Requirements on each monitored device

- SSH access reachable at the `ip`/`port` you register with `add_device`,
  using whatever username/password each Discord user registers for
  themselves with `add_user`.
- `bash` available on the device (used for `mapfile` when reading
  `/proc/<pid>/cmdline` without forking a subprocess per process — this is
  what keeps `show_pid_list` fast even with hundreds of running processes).

## Security note

`add_user` passwords are stored **in plaintext** in `data/users.json` (not
committed — see `.gitignore`) so the bot can re-authenticate on your behalf
for `show_pid_list`/`reminder`. Treat that file, and the machine the bot
runs on, as sensitive. This is meant for a trusted internal lab setting, not
a public server.

## Data files

Everything is plain JSON under `data/`, read/written directly (no database),
and gitignored:

- `data/users.json` — `dict[discord_user_id, dict[device_name, {"username", "password"}]]`
- `data/devices.json` — `list[{"name", "ip", "port"}]`
- `data/filters.json` — `dict[username, list[process_name]]`
- `data/languages.json` — `dict[discord_user_id, "chinese" | "english" | "japanese"]`

## Project layout

```
bot.py                 # entrypoint; syncs the slash command tree on startup
config.py              # reads .env
cogs/monitor.py         # all /monitor slash commands
utils/storage.py        # JSON read/write for users/devices/filters/languages
utils/ssh_utils.py       # paramiko: run remote commands, list processes, check if a pid is alive
utils/pagination.py      # ephemeral pagination (Prev/Next button view)
utils/i18n.py            # translation strings + t(lang, key, **kwargs) for chinese/english/japanese
data/                   # users.json, devices.json, filters.json, languages.json
```
