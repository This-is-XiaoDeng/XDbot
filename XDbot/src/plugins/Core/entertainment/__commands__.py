import nonebot
import nonebot.permission

guessnum_onmsg = nonebot.on_message()
user_status = nonebot.on_command(
    "user-info", aliases={"user-i", "info"})
sign_command = nonebot.on_command("sign", aliases={"签到"})
use_item = nonebot.on_command("use")
get_bag = nonebot.on_command("bag")
list_items = nonebot.on_command("list")
give_item = nonebot.on_command("give", permission=nonebot.permission.SUPERUSER)
sign_keyword = nonebot.on_keyword({"签到"})
guessnum = nonebot.on_command("guess", aliases={"gn"})
hijack_command = nonebot.on_command("sign", aliases={"抢劫", "打劫"})
