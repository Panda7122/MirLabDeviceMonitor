"""Multi-language message system for the bot's reply text.

This only translates the content the bot sends back (error messages,
confirmations, help text, pagination chrome) — it does not touch Discord's
own slash-command names/descriptions, which is a separate, client-locale-based
mechanism unrelated to a per-user stored preference.
"""

DEFAULT_LANGUAGE = "chinese"

LANGUAGE_NAMES = {
    "chinese": "繁體中文",
    "english": "English",
    "japanese": "日本語",
    "maid": "女僕",
    "anime": "動漫",
    "mygo": "MyGO!!!!!",
    "mesugaki": "雌小鬼",
}

_MESSAGES: dict[str, dict[str, str]] = {
    "chinese": {
        "error.unexpected": "執行指令時發生未預期的錯誤：{error}",
        "error.no_device": "找不到裝置 `{device}`，請確認裝置名稱是否正確。",
        "error.not_registered": "你尚未在裝置 `{device}` 上註冊登入資訊，請先使用 `/monitor add_user device:{device} ...` 註冊。",
        "add_user.registered": "已註冊你在裝置 `{device}` 上的登入資訊（使用者：`{username}`）。",
        "add_user.updated": "已更新你在裝置 `{device}` 上的登入資訊（使用者：`{username}`）。",
        "remove_user.removed": "已移除你在裝置 `{device}` 上註冊的登入資訊。",
        "remove_user.not_found": "你尚未在裝置 `{device}` 上註冊登入資訊。",
        "show_user_list.title": "你註冊的登入資訊",
        "add_device.added": "已新增裝置 `{name}` ({ip}:{port})。",
        "add_device.exists": "裝置 `{name}` 已經存在。",
        "remove_device.removed": "已移除裝置 `{name}`。",
        "remove_device.not_found": "找不到裝置 `{name}`。",
        "show_device_list.title": "裝置清單",
        "add_filter.added": "已將 `{name}` 加入使用者 `{username}` 的 filter list。",
        "add_filter.exists": "`{name}` 已經在使用者 `{username}` 的 filter list 中。",
        "remove_filter.removed": "已將 `{name}` 從使用者 `{username}` 的 filter list 移除。",
        "remove_filter.not_found": "使用者 `{username}` 的 filter list 中找不到 `{name}`。",
        "show_pid_list.fetch_failed": "取得裝置 `{device}` 的 pid 清單失敗：{error}",
        "show_pid_list.empty": "裝置 `{device}` 上目前沒有屬於 `{username}` 的行程。",
        "reminder.already_monitoring": "已經在監控裝置 `{device}` 的 pid `{pid}` 了。",
        "reminder.connect_failed": "連線裝置 `{device}` 失敗：{error}",
        "reminder.pid_not_found": "裝置 `{device}` 上找不到執行中的 pid `{pid}`。",
        "reminder.started": "開始監控裝置 `{device}` 的 pid `{pid}`{command_suffix}，執行完畢時會在此頻道通知你。",
        "reminder.watch_error": "監控裝置 `{device}` 的 pid `{pid}`{command_suffix} 時發生錯誤，已停止監控：{error}",
        "reminder.finished": "{mention} 裝置 `{device}` 的 pid `{pid}`{command_suffix} 已執行完畢。",
        "language.set": "已將你的顯示語言設定為「{language_name}」。",
        "pagination.not_yours": "這不是你的分頁訊息。",
        "pagination.page_footer": "頁 {current}/{total}",
        "pagination.prev_button": "⬅️ 上一頁",
        "pagination.next_button": "下一頁 ➡️",
        "help.text": (
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
            "`/monitor language lang` — 設定你的顯示語言（繁體中文 / English / 日本語 / 女僕 / 動漫 / MyGO!!!!! / 雌小鬼）\n"
            "`/monitor help` — 顯示這份說明\n"
            "\n"
            "`show_pid_list` 和 `reminder` 都需要先用 `add_user` 註冊該裝置的登入資訊。\n"
            "除了 reminder 完成時的通知會公開顯示在頻道，其餘指令的結果都只有你自己看得到。"
        ),
    },
    "english": {
        "error.unexpected": "An unexpected error occurred while running the command: {error}",
        "error.no_device": "Device `{device}` not found. Please check the device name.",
        "error.not_registered": "You haven't registered login credentials for device `{device}` yet. Please register first with `/monitor add_user device:{device} ...`.",
        "add_user.registered": "Registered your login for device `{device}` (username: `{username}`).",
        "add_user.updated": "Updated your login for device `{device}` (username: `{username}`).",
        "remove_user.removed": "Removed your registered login for device `{device}`.",
        "remove_user.not_found": "You haven't registered a login for device `{device}`.",
        "show_user_list.title": "Your registered logins",
        "add_device.added": "Added device `{name}` ({ip}:{port}).",
        "add_device.exists": "Device `{name}` already exists.",
        "remove_device.removed": "Removed device `{name}`.",
        "remove_device.not_found": "Device `{name}` not found.",
        "show_device_list.title": "Device List",
        "add_filter.added": "Added `{name}` to `{username}`'s filter list.",
        "add_filter.exists": "`{name}` is already in `{username}`'s filter list.",
        "remove_filter.removed": "Removed `{name}` from `{username}`'s filter list.",
        "remove_filter.not_found": "`{name}` was not found in `{username}`'s filter list.",
        "show_pid_list.fetch_failed": "Failed to fetch the pid list for device `{device}`: {error}",
        "show_pid_list.empty": "There are currently no processes owned by `{username}` on device `{device}`.",
        "reminder.already_monitoring": "Already monitoring pid `{pid}` on device `{device}`.",
        "reminder.connect_failed": "Failed to connect to device `{device}`: {error}",
        "reminder.pid_not_found": "No running pid `{pid}` found on device `{device}`.",
        "reminder.started": "Started monitoring pid `{pid}`{command_suffix} on device `{device}`. You'll be notified in this channel when it finishes.",
        "reminder.watch_error": "An error occurred while monitoring pid `{pid}`{command_suffix} on device `{device}`; monitoring stopped: {error}",
        "reminder.finished": "{mention} pid `{pid}`{command_suffix} on device `{device}` has finished.",
        "language.set": 'Your display language has been set to "{language_name}".',
        "pagination.not_yours": "This isn't your paginated message.",
        "pagination.page_footer": "Page {current}/{total}",
        "pagination.prev_button": "⬅️ Previous",
        "pagination.next_button": "Next ➡️",
        "help.text": (
            "**/monitor Command List**\n"
            "`/monitor add_user device username password` — Register your SSH login for a device (per Discord account, per device)\n"
            "`/monitor remove_user device` — Remove your registered login for a device\n"
            "`/monitor show_user_list` — Show the devices you've registered logins for (usernames only, no passwords)\n"
            "`/monitor add_device name ip port` — Add a device to the device list\n"
            "`/monitor remove_device name` — Remove a device from the device list\n"
            "`/monitor show_device_list` — Show the current device list\n"
            "`/monitor add_filter username name` — Hide a process name from that user's pid list\n"
            "`/monitor remove_filter username name` — Unhide a previously filtered process name\n"
            "`/monitor show_pid_list device [hide_system]` — Log in with your registered credentials and show your own pid / process name / command list (hide_system defaults to True; set False to also show commands starting with /)\n"
            "`/monitor reminder device pid` — Log in with your registered credentials and monitor a pid; you'll be mentioned in this channel when it finishes\n"
            "`/monitor language lang` — Set your display language (Traditional Chinese / English / Japanese / maid / anime / MyGO!!!!! / mesugaki)\n"
            "`/monitor help` — Show this help text\n"
            "\n"
            "`show_pid_list` and `reminder` both require you to register a login for that device with `add_user` first.\n"
            "Except for the reminder completion notice (posted publicly in the channel), every command's result is only visible to you."
        ),
    },
    "japanese": {
        "error.unexpected": "コマンドの実行中に予期しないエラーが発生しました：{error}",
        "error.no_device": "デバイス `{device}` が見つかりません。デバイス名を確認してください。",
        "error.not_registered": "デバイス `{device}` のログイン情報がまだ登録されていません。先に `/monitor add_user device:{device} ...` で登録してください。",
        "add_user.registered": "デバイス `{device}` のログイン情報を登録しました（ユーザー名：`{username}`）。",
        "add_user.updated": "デバイス `{device}` のログイン情報を更新しました（ユーザー名：`{username}`）。",
        "remove_user.removed": "デバイス `{device}` のログイン情報を削除しました。",
        "remove_user.not_found": "デバイス `{device}` にはログイン情報が登録されていません。",
        "show_user_list.title": "登録済みのログイン情報",
        "add_device.added": "デバイス `{name}` を追加しました（{ip}:{port}）。",
        "add_device.exists": "デバイス `{name}` は既に存在します。",
        "remove_device.removed": "デバイス `{name}` を削除しました。",
        "remove_device.not_found": "デバイス `{name}` が見つかりません。",
        "show_device_list.title": "デバイス一覧",
        "add_filter.added": "`{name}` をユーザー `{username}` のフィルターリストに追加しました。",
        "add_filter.exists": "`{name}` は既にユーザー `{username}` のフィルターリストにあります。",
        "remove_filter.removed": "`{name}` をユーザー `{username}` のフィルターリストから削除しました。",
        "remove_filter.not_found": "`{name}` はユーザー `{username}` のフィルターリストに見つかりません。",
        "show_pid_list.fetch_failed": "デバイス `{device}` の pid 一覧の取得に失敗しました：{error}",
        "show_pid_list.empty": "デバイス `{device}` には現在 `{username}` の行程がありません。",
        "reminder.already_monitoring": "デバイス `{device}` の pid `{pid}` は既に監視中です。",
        "reminder.connect_failed": "デバイス `{device}` への接続に失敗しました：{error}",
        "reminder.pid_not_found": "デバイス `{device}` で実行中の pid `{pid}` が見つかりません。",
        "reminder.started": "デバイス `{device}` の pid `{pid}`{command_suffix} の監視を開始しました。終了時にこのチャンネルで通知します。",
        "reminder.watch_error": "デバイス `{device}` の pid `{pid}`{command_suffix} の監視中にエラーが発生したため、監視を停止しました：{error}",
        "reminder.finished": "{mention} デバイス `{device}` の pid `{pid}`{command_suffix} が終了しました。",
        "language.set": "表示言語を「{language_name}」に設定しました。",
        "pagination.not_yours": "これはあなたのページ送りメッセージではありません。",
        "pagination.page_footer": "ページ {current}/{total}",
        "pagination.prev_button": "⬅️ 前へ",
        "pagination.next_button": "次へ ➡️",
        "help.text": (
            "**/monitor コマンド一覧**\n"
            "`/monitor add_user device username password` — そのデバイス上の SSH ログイン情報を登録します（Discordアカウントごと・デバイスごとに独立）\n"
            "`/monitor remove_user device` — そのデバイスに登録したログイン情報を削除します\n"
            "`/monitor show_user_list` — 自分が登録したデバイスとユーザー名を表示します（パスワードは表示されません）\n"
            "`/monitor add_device name ip port` — デバイスをデバイス一覧に追加します\n"
            "`/monitor remove_device name` — デバイス一覧からデバイスを削除します\n"
            "`/monitor show_device_list` — 現在のデバイス一覧を表示します\n"
            "`/monitor add_filter username name` — 指定したプロセス名をそのユーザーのフィルターリストに追加します（pid 一覧で非表示になります）\n"
            "`/monitor remove_filter username name` — フィルターリストからプロセス名を削除します\n"
            "`/monitor show_pid_list device [hide_system]` — 登録した認証情報でログインし、自分の pid / プロセス名 / コマンド一覧を表示します（hide_system は既定で True、False にすると / で始まるコマンドも表示します）\n"
            "`/monitor reminder device pid` — 登録した認証情報で pid を監視し、終了時にこのチャンネルであなたにメンションします\n"
            "`/monitor language lang` — 表示言語を設定します（繁體中文 / English / 日本語 / メイド / アニメ / MyGO!!!!! / メスガキ）\n"
            "`/monitor help` — このヘルプを表示します\n"
            "\n"
            "`show_pid_list` と `reminder` は、事前に `add_user` でそのデバイスのログイン情報を登録しておく必要があります。\n"
            "reminder の完了通知（チャンネルに公開されます）を除き、すべてのコマンドの結果はあなたにしか見えません。"
        ),
    },
    # ---- easter egg styles below: same functionality, different voice ----
    "maid": {
        "error.unexpected": "主人主人，好像出了一點小差錯呢～：{error}　人家會加油修好的！",
        "error.no_device": "咦～人家找不到裝置 `{device}` 耶，主人要不要再檢查一次名字呀？(｡•́︿•̀｡)",
        "error.not_registered": "主人還沒有在裝置 `{device}` 上登記登入資訊唷～快用 `/monitor add_user device:{device} ...` 讓人家記住吧！",
        "add_user.registered": "登記完成～♪ 人家記住主人在裝置 `{device}` 上的帳號 `{username}` 囉！",
        "add_user.updated": "更新好了喵～主人在裝置 `{device}` 的帳號 `{username}` 資料已經是最新的了！",
        "remove_user.removed": "遵命～已經把主人在裝置 `{device}` 的登入資訊忘掉囉！",
        "remove_user.not_found": "咦？主人在裝置 `{device}` 上還沒登記過呢，人家找不到資料唷～",
        "show_user_list.title": "主人登記過的裝置清單♪",
        "add_device.added": "新裝置 `{name}` ({ip}:{port}) 加入清單囉，人家會好好記住的！",
        "add_device.exists": "裝置 `{name}` 已經在清單裡面了唷，主人是不是忘記了呀～？",
        "remove_device.removed": "裝置 `{name}` 已經被人家移除囉～掰掰！",
        "remove_device.not_found": "找不到裝置 `{name}` 耶，是不是打錯名字了呀主人？",
        "show_device_list.title": "目前的裝置清單♪",
        "add_filter.added": "遵命！已經把 `{name}` 從使用者 `{username}` 的畫面裡藏起來囉～",
        "add_filter.exists": "`{name}` 已經被藏起來了唷，主人不用再說一次啦～",
        "remove_filter.removed": "好的～`{name}` 已經從 `{username}` 的隱藏清單裡拿出來囉！",
        "remove_filter.not_found": "咦，`{username}` 的隱藏清單裡沒有 `{name}` 耶～",
        "show_pid_list.fetch_failed": "嗚嗚，人家沒辦法取得裝置 `{device}` 的清單：{error}　對不起主人！",
        "show_pid_list.empty": "裝置 `{device}` 上目前沒有屬於 `{username}` 的行程唷，很乾淨呢～",
        "reminder.already_monitoring": "人家已經在幫主人盯著裝置 `{device}` 的 pid `{pid}` 囉，不用再說一次啦！",
        "reminder.connect_failed": "嗚嗚，連不上裝置 `{device}`：{error}　人家好難過～",
        "reminder.pid_not_found": "裝置 `{device}` 上找不到正在跑的 pid `{pid}` 耶～",
        "reminder.started": "好的主人！人家開始盯著裝置 `{device}` 的 pid `{pid}`{command_suffix} 囉，跑完會馬上來告訴你的♪",
        "reminder.watch_error": "嗚嗚，人家在盯著裝置 `{device}` 的 pid `{pid}`{command_suffix} 時出錯了，只好先停下來：{error}　對不起主人！",
        "reminder.finished": "{mention} 主人主人！裝置 `{device}` 的 pid `{pid}`{command_suffix} 已經跑完囉～辛苦了！",
        "language.set": "遵命～人家會用「{language_name}」跟主人說話囉♪",
        "pagination.not_yours": "咦，這不是主人的翻頁訊息唷～",
        "pagination.page_footer": "第 {current}/{total} 頁♪",
        "pagination.prev_button": "⬅️ 上一頁唷",
        "pagination.next_button": "下一頁唷 ➡️",
        "help.text": (
            "**♪ 主人的 /monitor 指令小手冊 ♪**\n"
            "`/monitor add_user device username password` — 讓人家記住主人在該裝置上的 SSH 帳號密碼（每位主人、每台裝置分開記錄喔）\n"
            "`/monitor remove_user device` — 請人家忘記某台裝置的登入資訊\n"
            "`/monitor show_user_list` — 看看人家幫主人記住了哪些裝置（密碼是秘密，不會說出來的♪）\n"
            "`/monitor add_device name ip port` — 把新裝置加進清單裡\n"
            "`/monitor remove_device name` — 把裝置從清單裡拿掉\n"
            "`/monitor show_device_list` — 看看目前的裝置清單\n"
            "`/monitor add_filter username name` — 把某個 process name 藏起來，不讓它出現在清單裡\n"
            "`/monitor remove_filter username name` — 把藏起來的 process name 找出來\n"
            "`/monitor show_pid_list device [hide_system]` — 用主人登記的帳密幫忙查看裝置上的 pid 清單（hide_system 預設為 True，設 False 就會連系統行程也一起顯示）\n"
            "`/monitor reminder device pid` — 幫主人盯著某個 pid，跑完會在這個頻道叫主人喔\n"
            "`/monitor language lang` — 讓人家換一種語氣跟主人說話（繁體中文 / English / 日本語 / 女僕 / 動漫 / MyGO!!!!! / 雌小鬼）\n"
            "`/monitor help` — 顯示這份小手冊\n"
            "\n"
            "`show_pid_list` 和 `reminder` 都要先用 `add_user` 讓人家記住登入資訊才能用喔！\n"
            "除了 reminder 跑完的通知會在頻道裡大聲說出來，其他的悄悄話都只有主人看得到唷♪"
        ),
    },
    "anime": {
        "error.unexpected": "……！執行中發生了無法預測的『因果律干涉』——錯誤詳情：{error}　這股力量究竟是……！",
        "error.no_device": "裝置 `{device}`……本座遍尋此界亦無法感知其存在。汝確定其真名無誤？",
        "error.not_registered": "汝尚未在裝置 `{device}` 締結『契約』。速速使用 `/monitor add_user device:{device} ...` 完成儀式吧！",
        "add_user.registered": "契約已締結！裝置 `{device}` 與使用者 `{username}` 之絆，已刻印於本座的記憶之中！",
        "add_user.updated": "契約已『重寫』！裝置 `{device}` 與使用者 `{username}` 之絆，已被賦予新的力量！",
        "remove_user.removed": "契約已解除。裝置 `{device}` 上的封印記錄，已從吾之記憶中抹除。",
        "remove_user.not_found": "裝置 `{device}` 上……並未存在汝與吾締結的契約。",
        "show_user_list.title": "汝與吾締結的契約一覽",
        "add_device.added": "新的『座標』已被銘刻——裝置 `{name}` ({ip}:{port})，已加入監視網。",
        "add_device.exists": "裝置 `{name}` 早已存在於監視網之中，無需二度封印。",
        "remove_device.removed": "裝置 `{name}` 的封印已經解除，其存在已從監視網中消去。",
        "remove_device.not_found": "監視網中並不存在名為 `{name}` 的座標。",
        "show_device_list.title": "受監視之座標一覽",
        "add_filter.added": "『隱匿之術』已施展——`{name}` 已從使用者 `{username}` 的視界中消去身影。",
        "add_filter.exists": "`{name}` 早已被隱匿之術封印，無需重複施法。",
        "remove_filter.removed": "隱匿之術已解除，`{name}` 重新顯現於使用者 `{username}` 的視界之中。",
        "remove_filter.not_found": "使用者 `{username}` 的封印清單中，並無 `{name}` 的蹤跡。",
        "show_pid_list.fetch_failed": "……窺探裝置 `{device}` 的『深淵』失敗了：{error}　果然，那並非吾等所能觸及之力。",
        "show_pid_list.empty": "裝置 `{device}` 之上，並無屬於 `{username}` 的『生命波動』。此界一片寂靜。",
        "reminder.already_monitoring": "裝置 `{device}` 的 pid `{pid}`……吾之『千里眼』早已鎖定其上，無需二度施法。",
        "reminder.connect_failed": "與裝置 `{device}` 的連結被『無形之壁』阻斷：{error}",
        "reminder.pid_not_found": "裝置 `{device}` 之上，並不存在仍在躍動的 pid `{pid}`。其『生命』或許早已終結。",
        "reminder.started": "『千里眼』已然開啟——吾將凝視裝置 `{device}` 的 pid `{pid}`{command_suffix}，待其終焉之時，必於此頻道昭告天下！",
        "reminder.watch_error": "凝視裝置 `{device}` 的 pid `{pid}`{command_suffix} 之時，『千里眼』遭到未知之力干擾，監視已被迫中斷：{error}",
        "reminder.finished": "{mention} 汝所託付之『宿命』已然完結——裝置 `{device}` 的 pid `{pid}`{command_suffix} 已迎來終焉。",
        "language.set": "汝之意志已被聽見。吾將以「{language_name}」之言靈，與汝對話。",
        "pagination.not_yours": "此乃他者之『記錄之書』，非汝所能翻閱。",
        "pagination.page_footer": "第 {current} / {total} 頁　封印進度",
        "pagination.prev_button": "⬅️ 前一頁的記憶",
        "pagination.next_button": "下一頁的真實 ➡️",
        "help.text": (
            "**——『/monitor』禁書目錄——**\n"
            "`/monitor add_user device username password` — 與裝置締結『契約』，銘刻專屬於汝的 SSH 認證之力（每位召喚者、每個座標各自獨立）\n"
            "`/monitor remove_user device` — 解除與該裝置的契約\n"
            "`/monitor show_user_list` — 窺探汝與各裝置締結的契約全貌（密碼之力永不外洩）\n"
            "`/monitor add_device name ip port` — 將新的座標銘刻於監視網之中\n"
            "`/monitor remove_device name` — 將座標從監視網中消去\n"
            "`/monitor show_device_list` — 顯示監視網中的所有座標\n"
            "`/monitor add_filter username name` — 對指定的行程施展『隱匿之術』\n"
            "`/monitor remove_filter username name` — 解除隱匿之術\n"
            "`/monitor show_pid_list device [hide_system]` — 以汝的契約之力窺探裝置深處的 pid / 行程 / 指令真名（hide_system 預設封印系統行程，設為 False 則解放全部真實）\n"
            "`/monitor reminder device pid` — 開啟『千里眼』監視特定 pid，終焉降臨時必在此頻道昭告於汝\n"
            "`/monitor language lang` — 切換吾與汝對話所使用的言靈（繁體中文 / English / 日本語 / 女僕 / 動漫 / MyGO!!!!! / 雌小鬼）\n"
            "`/monitor help` — 顯示此禁書目錄\n"
            "\n"
            "`show_pid_list` 與 `reminder` 皆須先以 `add_user` 締結契約，方能發動。\n"
            "除了 reminder 終焉降臨的宣告會響徹全頻道，其餘一切『真實』唯有汝一人可見。"
        ),
    },
    "mygo": {
        "error.unexpected": "真不敢相信……執行指令時出了問題：{error}",
        "error.no_device": "找不到裝置 `{device}`。這算什麼。",
        "error.not_registered": "你在裝置 `{device}` 上還沒有登入資訊——那我呢？先用 `/monitor add_user device:{device} ...` 登記一下吧。",
        "add_user.registered": "好，我知道了。裝置 `{device}` 的登入資訊（使用者 `{username}`）已經記住了。",
        "add_user.updated": "裝置 `{device}` 的登入資訊已經更新（使用者 `{username}`）——是嗎。",
        "remove_user.removed": "裝置 `{device}` 的登入資訊，已經被刪除了。",
        "remove_user.not_found": "裝置 `{device}` 上——什麼都沒有。你從來沒有登記過。",
        "show_user_list.title": "你登記過的裝置",
        "add_device.added": "裝置 `{name}` ({ip}:{port}) 加進來了。不錯吧。",
        "add_device.exists": "裝置 `{name}` 早就在了。妳是來找我吵架的嗎？",
        "remove_device.removed": "裝置 `{name}` 已經被移除了。",
        "remove_device.not_found": "找不到裝置 `{name}`——真不敢相信。",
        "show_device_list.title": "裝置清單",
        "add_filter.added": "`{name}` 已經從使用者 `{username}` 的畫面裡消失了。",
        "add_filter.exists": "`{name}` 已經藏起來了，妳沒有必要再說一次。",
        "remove_filter.removed": "`{name}` 已經從 `{username}` 的隱藏清單拿出來了。",
        "remove_filter.not_found": "`{username}` 的隱藏清單裡，沒有 `{name}` 這種東西。",
        "show_pid_list.fetch_failed": "取得裝置 `{device}` 的 pid 清單失敗了：{error}　這也太差勁了吧。",
        "show_pid_list.empty": "裝置 `{device}` 上，沒有任何屬於 `{username}` 的行程。滿腦子都只想到自己呢。",
        "reminder.already_monitoring": "裝置 `{device}` 的 pid `{pid}`，我已經在看了。不用再說一次。",
        "reminder.connect_failed": "連不上裝置 `{device}`：{error}　為什麼會這樣。",
        "reminder.pid_not_found": "裝置 `{device}` 上，找不到還在跑的 pid `{pid}`。",
        "reminder.started": "我開始看著裝置 `{device}` 的 pid `{pid}`{command_suffix} 了。結束的時候，我會在這裡跟妳說。",
        "reminder.watch_error": "看著裝置 `{device}` 的 pid `{pid}`{command_suffix} 的時候出了問題，只好先停下來：{error}",
        "reminder.finished": "{mention} 裝置 `{device}` 的 pid `{pid}`{command_suffix}，結束了。真的，結束了。",
        "language.set": "好，我知道了。之後我會用「{language_name}」跟妳說話。",
        "pagination.not_yours": "這不是妳的東西。",
        "pagination.page_footer": "第 {current}/{total} 頁",
        "pagination.prev_button": "⬅️ 上一頁",
        "pagination.next_button": "下一頁 ➡️",
        "help.text": (
            "**/monitor 指令一覽——由妳決定要不要看**\n"
            "`/monitor add_user device username password` — 登記妳在該裝置上的 SSH 帳號密碼（每個人、每台裝置都不一樣）\n"
            "`/monitor remove_user device` — 刪除妳在該裝置上的登入資訊\n"
            "`/monitor show_user_list` — 看看妳登記過哪些裝置（密碼不會被說出來）\n"
            "`/monitor add_device name ip port` — 把裝置加進清單\n"
            "`/monitor remove_device name` — 把裝置從清單移除\n"
            "`/monitor show_device_list` — 顯示目前的裝置清單\n"
            "`/monitor add_filter username name` — 把某個 process name 從畫面上藏起來\n"
            "`/monitor remove_filter username name` — 把藏起來的 process name 找回來\n"
            "`/monitor show_pid_list device [hide_system]` — 用妳登記的帳密登入，看看屬於妳自己的 pid 清單（hide_system 預設為 True，設 False 連系統行程也會顯示）\n"
            "`/monitor reminder device pid` — 盯著某個 pid，結束的時候會在這個頻道叫妳\n"
            "`/monitor language lang` — 換一種語氣說話（繁體中文 / English / 日本語 / 女僕 / 動漫 / MyGO / 雌小鬼）\n"
            "`/monitor help` — 顯示這份說明\n"
            "\n"
            "`show_pid_list` 和 `reminder` 都要先用 `add_user` 登記過才能用。\n"
            "除了 reminder 結束的通知會在頻道裡公開，其他的——都只有妳看得到。"
        ),
    },
    "mesugaki": {
        "error.unexpected": "呃……才、才不是我的問題呢！是系統自己出錯的：{error}　哼！",
        "error.no_device": "嘿嘿，裝置 `{device}` 根本不存在唷，雜魚是不是連名字都打錯了呀？",
        "error.not_registered": "你連在裝置 `{device}` 上登記都還沒做呢，真是個沒用的雜魚。快用 `/monitor add_user device:{device} ...` 登記啦！",
        "add_user.registered": "哼，裝置 `{device}` 的帳號 `{username}` 我記住了。這種小事對我來說一下就搞定啦，雜魚應該要感謝我才對吧？",
        "add_user.updated": "裝置 `{device}` 的帳號 `{username}` 更新好了唷～看吧，果然沒我不行呢。",
        "remove_user.removed": "裝置 `{device}` 的登入資訊被我刪掉囉，嘿嘿，滿意了嗎，雜魚？",
        "remove_user.not_found": "你根本沒在裝置 `{device}` 上登記過吧？連這種事都會搞錯，真是個雜魚呢。",
        "show_user_list.title": "你登記過的裝置（要不是我記性好，你早就忘光了吧）",
        "add_device.added": "裝置 `{name}` ({ip}:{port}) 加進來囉。哼，這種程度當然難不倒我啦～",
        "add_device.exists": "裝置 `{name}` 早就有了啦，雜魚是不是忘記了呀？",
        "remove_device.removed": "裝置 `{name}` 被我刪掉了，嘿嘿，很快吧？雜魚應該跟不上我的速度呢。",
        "remove_device.not_found": "找不到裝置 `{name}` 耶……才、才不是我沒找到啦！是根本就不存在！",
        "show_device_list.title": "裝置清單（乖乖看好，別漏看囉）",
        "add_filter.added": "`{name}` 已經從使用者 `{username}` 的畫面裡藏起來了，嘿嘿，我的手腳很快的唷～",
        "add_filter.exists": "`{name}` 早就被藏起來了啦，雜魚是不是忘記自己做過了？",
        "remove_filter.removed": "`{name}` 已經從 `{username}` 的隱藏清單裡拿出來了，滿意了嗎？",
        "remove_filter.not_found": "`{username}` 的隱藏清單裡根本沒有 `{name}` 這種東西啦，雜魚是不是記錯了？",
        "show_pid_list.fetch_failed": "呃……才、才不是我的錯呢！是裝置 `{device}` 自己連不上的：{error}",
        "show_pid_list.empty": "裝置 `{device}` 上沒有任何屬於 `{username}` 的行程唷，很乾淨吧？畢竟是我在看嘛～",
        "reminder.already_monitoring": "裝置 `{device}` 的 pid `{pid}`，我早就在看著了啦。雜魚是不是忘記自己說過了？",
        "reminder.connect_failed": "連不上裝置 `{device}` 啦：{error}　才、才不是我的問題呢，哼！",
        "reminder.pid_not_found": "裝置 `{device}` 上找不到還在跑的 pid `{pid}` 耶，雜魚是不是記錯 pid 了呀？",
        "reminder.started": "哼，好啦，我就大發慈悲幫你盯著裝置 `{device}` 的 pid `{pid}`{command_suffix} 吧。結束了會告訴你，雜魚要好好感謝我唷～",
        "reminder.watch_error": "盯著裝置 `{device}` 的 pid `{pid}`{command_suffix} 的時候出錯了……才、才不是我沒看好啦！只好先停下來：{error}",
        "reminder.finished": "{mention} 喂，雜魚，裝置 `{device}` 的 pid `{pid}`{command_suffix} 跑完了唷，還不快說謝謝？",
        "language.set": "哼，知道了啦，之後就用「{language_name}」跟你這個雜魚說話吧～",
        "pagination.not_yours": "這才不是你的分頁訊息呢，雜魚。",
        "pagination.page_footer": "第 {current}/{total} 頁（乖乖往下看唷）",
        "pagination.prev_button": "⬅️ 上一頁啦",
        "pagination.next_button": "下一頁啦 ➡️",
        "help.text": (
            "**/monitor 指令一覽（雜魚沒看過的話，先給我乖乖看好）**\n"
            "`/monitor add_user device username password` — 讓我記住你這個雜魚在該裝置上的 SSH 帳密（每個人、每台裝置都分開記，別搞混囉）\n"
            "`/monitor remove_user device` — 叫我忘記你在該裝置上的登入資訊\n"
            "`/monitor show_user_list` — 看看我幫你記住了哪些裝置（密碼才不會說出來呢，哼）\n"
            "`/monitor add_device name ip port` — 把新裝置加進清單\n"
            "`/monitor remove_device name` — 把裝置從清單裡刪掉\n"
            "`/monitor show_device_list` — 看看目前的裝置清單\n"
            "`/monitor add_filter username name` — 把某個 process name 藏起來，眼不見為淨\n"
            "`/monitor remove_filter username name` — 把藏起來的 process name 找出來\n"
            "`/monitor show_pid_list device [hide_system]` — 用你登記的帳密幫你查看裝置上的 pid 清單（hide_system 預設為 True，設 False 就會連系統行程也顯示，雜魚別亂設唷）\n"
            "`/monitor reminder device pid` — 大發慈悲幫你盯著某個 pid，跑完了會在這個頻道叫你\n"
            "`/monitor language lang` — 換一種語氣跟你這個雜魚說話（繁體中文 / English / 日本語 / 女僕 / 動漫 / MyGO!!!!! / 雌小鬼）\n"
            "`/monitor help` — 顯示這份說明（雜魚才需要看第二次啦）\n"
            "\n"
            "`show_pid_list` 和 `reminder` 都要先用 `add_user` 登記過才能用唷，這都不知道嗎，雜魚？\n"
            "除了 reminder 跑完的通知會在頻道裡大聲說出來，其他的都只有你看得到啦……才、才不是我想偷偷跟你說的呢！"
        ),
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    messages = _MESSAGES.get(lang) or _MESSAGES[DEFAULT_LANGUAGE]
    template = messages.get(key) or _MESSAGES[DEFAULT_LANGUAGE].get(key, key)
    return template.format(**kwargs)
