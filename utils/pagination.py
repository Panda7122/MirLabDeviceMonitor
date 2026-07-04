import discord


def paginate(header: str, rows: list[str], page_size: int = 20, max_len: int = 1800) -> list[str]:
    """Splits rows into ```code block``` pages of at most page_size rows each,
    also respecting Discord's message length limit. Returns fully rendered
    page strings (including a footer "頁 x/y" when there's more than one page).
    """
    if not rows:
        return [f"```\n{header}\n```"]

    chunks: list[list[str]] = []
    current: list[str] = []
    length = len(header) + 1
    for row in rows:
        exceeds_len = length + len(row) + 1 > max_len
        exceeds_count = len(current) >= page_size
        if current and (exceeds_len or exceeds_count):
            chunks.append(current)
            current = []
            length = len(header) + 1
        current.append(row)
        length += len(row) + 1
    chunks.append(current)

    total = len(chunks)
    pages = []
    for i, rows_chunk in enumerate(chunks, start=1):
        body = "\n".join([header, *rows_chunk])
        page = f"```\n{body}\n```"
        if total > 1:
            page += f"\n頁 {i}/{total}"
        pages.append(page)
    return pages


class Paginator(discord.ui.View):
    """Prev/Next button pager for a list of pre-rendered page strings.

    Since the message this is attached to is always sent ephemeral, only the
    invoking user can ever see or click the buttons — the author check below
    is just defense in depth.
    """

    def __init__(self, pages: list[str], author_id: int, timeout: float = 180):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.author_id = author_id
        self.index = 0
        self.message: discord.InteractionMessage | discord.WebhookMessage | None = None
        self._update_buttons()

    def _update_buttons(self) -> None:
        self.previous_page.disabled = self.index <= 0
        self.next_page.disabled = self.index >= len(self.pages) - 1

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("這不是你的分頁訊息。", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="⬅️ 上一頁", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.index -= 1
        self._update_buttons()
        await interaction.response.edit_message(content=self.pages[self.index], view=self)

    @discord.ui.button(label="下一頁 ➡️", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.index += 1
        self._update_buttons()
        await interaction.response.edit_message(content=self.pages[self.index], view=self)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


async def send_paginated(
    interaction: discord.Interaction,
    pages: list[str],
    *,
    use_followup: bool,
) -> None:
    """Sends the first page ephemerally, attaching Prev/Next buttons if there's more than one page."""
    view = Paginator(pages, author_id=interaction.user.id) if len(pages) > 1 else None
    # discord.py's view kwarg defaults to a MISSING sentinel, not None — passing
    # view=None explicitly fails its type check, so it must be omitted entirely
    # when there's nothing to attach.
    kwargs = {"view": view} if view is not None else {}
    if use_followup:
        message = await interaction.followup.send(pages[0], ephemeral=True, **kwargs)
    else:
        await interaction.response.send_message(pages[0], ephemeral=True, **kwargs)
        message = await interaction.original_response()
    if view is not None:
        view.message = message
