"""Curated MyGO!!!!! meme images for the "mygo" easter-egg language.

Source: https://mygo.miyago9267.com/api/v1/images — each entry below is a real
image from that site, hand-picked to match the mood of the message key it's
attached to (some reuse the exact meme line the mygo-style text itself quotes).
Only "reaction"-style messages (errors/confirmations/reminder events) get an
image; table/list outputs (show_pid_list, show_user_list, show_device_list)
are left alone since a meme image would just clutter a data table.
"""

# key -> (image_url, alt_text_used_as_caption)
MYGO_IMAGES: dict[str, tuple[str, str]] = {
    "error.unexpected": ("https://storageapi.miyago9267.com/f/c6a4646c-9017-4fdf-bb7c-d03845fe9b19.jpg", "真不敢相信"),
    "error.no_device": ("https://storageapi.miyago9267.com/f/598e383f-3d7f-484f-a664-cd6037d41c92.jpg", "這算什麼"),
    "error.not_registered": ("https://storageapi.miyago9267.com/f/212358c0-95b9-45a4-a4c1-7ff37b817bfe.jpg", "為什麼都不回答我啊"),
    "add_user.registered": ("https://storageapi.miyago9267.com/f/a3a17a12-ff1b-44fb-9c2a-268e589ff544.jpg", "那真是可喜可賀"),
    "add_user.updated": ("https://storageapi.miyago9267.com/f/34ab5340-e916-4f8b-9953-32dd22a50f69.jpg", "是嗎"),
    "remove_user.removed": ("https://storageapi.miyago9267.com/f/f81cc001-95e9-4915-bc0a-1f42fb8bd3e4.jpg", "這個不用了"),
    "remove_user.not_found": ("https://storageapi.miyago9267.com/f/3ae25b25-0ea3-4a6a-b5fa-e012b5b3b92b.jpg", "差勁"),
    "add_device.added": ("https://storageapi.miyago9267.com/f/c1e4d5e8-7924-4f7c-8c1e-f350c9f53fa6.jpg", "不錯吧"),
    "add_device.exists": ("https://storageapi.miyago9267.com/f/dea6c6bd-1048-4b69-bdee-fe86a0fa0d33.jpg", "妳是來找我吵架的嗎"),
    "remove_device.removed": ("https://storageapi.miyago9267.com/f/c00911d5-1a10-4afe-aa9a-ae0522359e40.jpg", "原來妳是這麼想的呀"),
    "remove_device.not_found": ("https://storageapi.miyago9267.com/f/555aab37-16be-450e-b28b-93fff765bfe6.jpg", "怎麼會...簡直不敢相信"),
    "add_filter.added": ("https://storageapi.miyago9267.com/f/8ddfda2e-3a1f-4bb8-8940-b9086f1e16a7.jpg", "我懂"),
    "add_filter.exists": ("https://storageapi.miyago9267.com/f/3a030739-be5e-470c-aae5-4e1f751bb4cf.jpg", "是沒錯啊"),
    "remove_filter.removed": ("https://storageapi.miyago9267.com/f/683a9ab9-25bf-4244-b399-17325734aab8.jpg", "也沒有啦"),
    "remove_filter.not_found": ("https://storageapi.miyago9267.com/f/8c6b9b76-45b3-4fb6-8e35-aa7864236cc5.jpg", "這傢伙根本什麼也不懂"),
    "show_pid_list.fetch_failed": ("https://storageapi.miyago9267.com/f/3c5fa304-1692-4d36-87f1-225524c01116.jpg", "妳到底是怎樣啊"),
    "show_pid_list.empty": ("https://storageapi.miyago9267.com/f/be924755-85a4-4dfe-9859-1ca2be343933.jpg", "滿腦子都只想到自己呢"),
    "reminder.already_monitoring": ("https://storageapi.miyago9267.com/f/9d45ed00-582f-4378-a43b-1dde9e2bcf4d.jpg", "我有啊"),
    "reminder.connect_failed": ("https://storageapi.miyago9267.com/f/55af4a26-e002-4b54-8b2e-2faaa714cca7.jpg", "愛音:蛤"),
    "reminder.pid_not_found": ("https://storageapi.miyago9267.com/f/8141a396-28ab-494d-9156-4a0bf805cf24.jpg", "我想應該不是"),
    "reminder.started": ("https://storageapi.miyago9267.com/f/c6591ba9-3c7c-4dbd-b271-07da289739fb.jpg", "我都會全力以赴的"),
    "reminder.watch_error": ("https://storageapi.miyago9267.com/f/afba7bff-aaee-4074-8f91-001e10c1f253.jpg", "我都說了討厭了吧"),
    "reminder.finished": ("https://storageapi.miyago9267.com/f/c4934591-33ab-421f-90a2-502d866ee25c.jpg", "真是太對了"),
    "language.set": ("https://storageapi.miyago9267.com/f/eafc252e-2dd3-4cf6-974b-111b2a1f1d65.jpg", "好厲害"),
}
