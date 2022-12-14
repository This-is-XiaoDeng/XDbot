from nonebot.log import logger
from . import __config__ as config
from . import __commands__ as commands
import nonebot.adapters.onebot.v11
import nonebot.params
import requests
import json


@commands.translate.handle()
async def translate_handle(
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    keyword = message.extract_plain_text()
    req = requests.get(
        f"https://api.muxiaoguo.cn/api/Tn_tencent?api_key={config.translate.api_key}&text={keyword}")
    data = json.loads(req.text)
    answer = ""

    logger.info(f"Translation server reply {data}")

    if data["code"] == 200:
        answer += f'''【翻译结果】
原文：{data["data"]["Original"]}
译文：{data["data"]["Translation"]}'''
    else:
        logger.error(f"Translation server error: {data['msg']}")
        answer += f"失败（{data['code']}）：{data['msg']}"

    await commands.translate.finish(answer)
