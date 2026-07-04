import asyncio

import discord
from discord.ext import commands

import config

intents = discord.Intents.default()


class MonitorBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.monitor")
        if config.GUILD_ID:
            guild = discord.Object(id=config.GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


bot = MonitorBot(command_prefix=config.COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


async def main():
    if not config.DISCORD_TOKEN:
        raise SystemExit("請在 .env 中設定 DISCORD_TOKEN（可參考 .env.example）")

    async with bot:
        await bot.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
