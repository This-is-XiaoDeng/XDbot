from . import __commands__ as commands
from . import __config__ as config
from nonebot.log import logger
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import nonebot.params
import random
import asyncio


async def autoremove(group):
    await asyncio.sleep(config.guessnum.max_time)
    logger.info(f"Stopping the game in {group}")
    if group in list(config.guessnum.number.keys()):
        # BUG: 无法正常删除
        await commands.guessnum.send(f"时间到，游戏结束，正确答案：{config.guessnum.number[group]}")
        config.guessnum.number.pop(group)


@commands.guessnum_onmsg.handle()
async def guessnum_onmessage_handle(
    event: nonebot.adapters.onebot.v11.event.GroupMessageEvent
):
    argv = event.get_plaintext()
    group = event.get_session_id().split("_")[1]
    if group in list(config.guessnum.number.keys()):
        # Guess number
        try:
            guessed = int(argv)
            if guessed == config.guessnum.number[group]:
                answer = config.guessnum.number.pop(group)
                await commands.guessnum.finish(f"{answer}，回答正确！", at_sender=True)
            elif guessed > config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，大了", at_sender=True)
            elif guessed < config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，小了", at_sender=True)
        except Exception as e:
            logger.error(e)


@commands.guessnum.handle()
async def guessnum_handle(
    event: nonebot.adapters.onebot.v11.event.MessageEvent,
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    argv = message.extract_plain_text().split(" ")
    group = event.get_session_id().split("_")[1]
    # Start Game
    if argv[0] == "start":
        if group not in config.guessnum.number.keys():
            config.guessnum.number[group] = random.randint(
                0, config.guessnum.max)
            logger.info(
                f"Created game in group {group}, answer {config.guessnum.number[group]}")
            asyncio.create_task(autoremove(group))
            await commands.guessnum.finish(f"【猜数字】：请在 {config.guessnum.max_time}s 内使用 /guess <number> 作答，0 <= <number> <= {config.guessnum.max}")
        else:
            await commands.guessnum.finish("游戏已存在")
    # Ranking
    elif argv[0] == "list":
        await commands.guessnum.finish("敬请期待")
    # Stop Game
    elif argv[0] == "stop":
        try:
            answer = config.guessnum.number.pop(group)
        except KeyError:
            await commands.guessnum.finish("找不到游戏", at_sender=True)
        else:
            await commands.guessnum.finish(f"游戏结束，正确答案：{answer}")
    else:
        # Guess number
        try:
            guessed = int(argv[0])
            if guessed == config.guessnum.number[group]:
                answer = config.guessnum.number.pop(group)
                await commands.guessnum.finish(f"{answer}，回答正确！", at_sender=True)
            elif guessed > config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，大了", at_sender=True)
            elif guessed < config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，小了", at_sender=True)
        except KeyError:
            await commands.guessnum.finish(f"游戏未开始或已结束，使用 {config.__config__.command_help.command_start}guess start 创建游戏", at_sender=True)
        except ValueError:
            await commands.guessnum.finish(f"""未知参数：{argv[0]}
/guess start （开始游戏）
/guess stop （结束游戏）
/guess <number: int> （作答）
/guess list（排行榜：敬请期待）
在游戏进行中：<number: int>（作答）""".replace("/", config.__config__.command_help.command_start))
