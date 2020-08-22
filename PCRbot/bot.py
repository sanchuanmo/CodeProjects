from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
import threading
import datetime
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="graia-mirai-api-http-authkey", # 填入 authKey
        account=765183386, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

from graia.application.event.messages import FriendMessage
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend
from graia.application.event.messages import GroupMessage
from graia.application.group import Group
from graia.application.group import Member
import graia.application.message.elements.internal as internal
from boss import Boss
from player import Player
import config

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend:Friend, message:MessageChain):
    print(message)
    print("type:",type(message))
    print("friend")
    print(friend)
    print(type(friend))

@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group:Group, message:MessageChain, member:Member):
    # print(group)
    # id=1130879466 name='测试群' accountPerm=<MemberPerm.Member: 'MEMBER'>
    # print(type(group))
    if group.id in config.GROUPS:
        # print(message.asDisplay())
        # print(message.__root__)
        # print(message.__root__[2].target)
        # print(type(message.__root__[2].target))
        if config.STATE == 0 and message.asDisplay() == "开启bot":
            await app.sendGroupMessage(group,MessageChain.create([
                Plain("加载群成员数据")
            ]))
            group_info = await app.memberList(group)
            for i in group_info:
                Player.member_list[i.id] = i.name
            print(Player.member_list)
            await app.sendGroupMessage(group,MessageChain.create([
                Plain("加载成功\n bot已开启")
            ]))
            # bot start
            config.STATE = 1
        elif config.STATE == 1 and message.asDisplay() == "关闭bot":
            config.STATE = 0
            await app.sendGroupMessage(group,MessageChain.create([
                Plain("关闭bot")
            ]))
        elif (config.STATE == 0 and message.asDisplay() == "关闭bot") or \
            (config.STATE == 1 and message.asDisplay() == "开启bot"):
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("异常操作")
            ]))
        elif config.STATE == 1:
            message_return = ""
            # 申请出刀，解除出刀，完成，击杀，代打，撤回出刀，挂树，查树，强行下树
            if message.asDisplay() == "申请出刀":
                if member.name not in Player.player_list and member.name not in Player.player_on_tree_list:
                    # 正常
                    Player.player_list.append(member.name)
                    message_return = "%s开始出刀" %member.name
                elif member.name in Player.player_list:
                    message_return = "您已在出刀序列中"
                elif member.name in Player.player_on_tree_list:
                    message_return = "您已挂树"
            elif message.asDisplay() == "解除出刀":
                if member.name in Player.player_list:
                    Player.player_list.remove(member.name)
                    message_return = "成功解除出刀"
                elif member.name not in Player.player_list:
                    message_return = "您不在出刀序列中"
                elif member.name in Player.player_on_tree_list:
                    message_return = "您已挂树"
            elif message.asDisplay().startswith("完成"):
                hurtNum = Boss.split_message(Boss,message.asDisplay())
                hurtNum = int(hurtNum)
                if member.name in Player.player_list:
                    message_return = Boss.hurtNum(Boss,member.name,hurtNum)
                    Player.player_list.remove(member.name)
                elif member.name not in Player.player_list:
                    message_return = "您还没有出刀"
            elif message.asDisplay().startswith("代打"):
                print(message.__root__[2].target)
                print(type(message.__root__[2].target))
                name = Player.member_list.get(message.__root__[2].target)
                print("name",name)
                hurtNum = int(Boss.split_message(Boss,message.asDisplay()))
                message_return = Boss.hurtNum(Boss,name,hurtNum)
            elif message.asDisplay() == "撤回出刀":
                message_return = Boss.recall_last_hurtNum(Boss,member.name)
            elif message.asDisplay() == "挂树":
                if member.name in Player.player_list:
                    Player.player_list.remove(member.name)
                    Player.player_on_tree_list.append(member.name)
                    message_return = "%s挂树" %(member.name)
                elif member.name not in Player.player_list:
                    message_return = "您还没有出刀"
                elif member.name in Player.player_on_tree_list:
                    message_return = "您已经挂树"
            elif message.asDisplay() == "查树":
                message_return = Player.read_tree(Player)
            elif message.asDisplay().startswith("强行下树"):
                if member.name in Player.player_on_tree_list:
                    hurtNum = Boss.split_message(Boss,message.asDisplay())
                    hurtNum = int(hurtNum)
                    message_return = Boss.hurtNum(Boss,member.name,hurtNum)
                elif member.name in Player.player_list:
                    message_return = "您没有挂树，请正常报刀"
                elif member.name not in Player.player_list and member.name not in Player.player_on_tree_list:
                    message_return = "请申请出刀"



            # boss数据操作
            elif message.asDisplay() == "查看":
                message_return = Boss.get_boss_info(Boss)
            elif message.asDisplay().startswith("修正"):
                round,i,boss_remain = Boss.split_message(Boss,message.asDisplay())
                round = int(round)
                i = int(i)
                boss_remain = int(boss_remain)
                message_return = Boss.set_boss_info(Boss,round,i,boss_remain)

            # 会战数据操作
            elif message.asDisplay() == "出刀数据":
                message_return = Player.read(Player,Player.fight_data)
            elif message.asDisplay() == "读取":
                message_return = Player.readf(Player)
            elif message.asDisplay() == "保存":
                message_return = Player.savef(Player)
            else:
                message_return = ""
            await app.sendGroupMessage(group,MessageChain.create([
                Plain(message_return)
            ]))




def timerClear_fight_data():
    print("start")
    if datetime.datetime.now().hour == 5:
        message_return = Player.automatic_savef(Player)
        print(message_return)
        print("fight_data", Player.fight_data)
    global t1
    t1 = threading.Timer(1200, timerClear_fight_data)
    t1.start()
if __name__ == "__main__":
    Player()
    Boss()
    timer = threading.Timer(1200,timerClear_fight_data)
    timer.start()
    app.launch_blocking()