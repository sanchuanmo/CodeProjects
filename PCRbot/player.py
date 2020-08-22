# 玩家
import json
import datetime
import os
class Player(object):
    # 会战运行数据
    player_list = []
    player_on_tree_list = []
    member_list = {}
    # 会战存储数据 data = [round,i,hurtNum,boolean]  boolean 是否击杀boss
    fight_data = {} #  {"三川":[[1,1,34535535,true],[1,2,43535]],"四川":[[1,1,353535],[1,2,45235]]}


    def read(self, fight_data)->str:
        # 读取当前内存数据
        message_return = ""
        if len(fight_data) == 0:
            message_return = "内存无数据"
        else:
            # 读取数据
            for key,value in fight_data.items():
                name = key
                datas = value
                message_return = message_return + name + "\n"
                for data in datas:
                    if data[-1] is True:
                        message_return = message_return + "%s对%d周目%d王造成了%d伤害 击杀" \
                                        %(name,data[0],data[1],data[2]) + "\n"
                    elif data[-1] is False:
                        message_return = message_return + "%s对%d周目%d王造成了%d伤害" \
                                         % (name, data[0], data[1], data[2]) + "\n"
        return message_return



    def savef(self)->str:
        # 存储会战数据到本地，json格式
        # 获取存储文件名:当前时间
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        filename = "%d-%d-%d" %(year,month,day)
        with open("./data/"+filename,"w") as fw:
            fw.write(json.dumps(self.fight_data))
        return "文件已存储到服务器"
    def automatic_savef(self):
        # 自动存储会战数据到本地，并清空会战数据缓存
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day - 1
        filename = "%d-%d-%d" %(year,month,day)
        with open("./data/"+filename,"w") as fw:
            fw.write(json.dumps(self.fight_data))
        self.fight_data.clear()
        return "文件已存储到服务器\n数据已清除"
    def readf(self)->str:
        # 读取本地数据
        message_return = ""
        for root, dirs, files in os.walk("./data"):
            for file in files:
                message_return = message_return + file + "\n"
                with open("./data/"+file,"r") as fr:
                    fight_data_file = json.load(fr)
                    print(type(fight_data_file))
                    message_return = message_return + self.read(self,fight_data_file) + "\n"
        return message_return

    def read_tree(self):
        message_return = "挂树人员\n:"
        for player in self.player_on_tree_list:
            message_return = message_return + player + "\n"
        return message_return
if __name__ == "__main__":
    import threading
    import bot
    Player.fight_data = {"三川":[[1,1,34535535,False],[1,2,43535,False]],"四川":[[1,1,353535,True],
                                                                             [1,2,45235,True]]}
    # print(Player.read(Player,Player.fight_data))
    # print(Player.savef(Player))
    # print(Player.readf(Player))
    # Player.player_on_tree_list = ["demo","demo3"]
    # print(Player.read_tree(Player))
    # timer = threading.Timer(15,bot.timerClear_fight_data)
    # timer.start()
    #
    # print("fight_data",Player.fight_data)