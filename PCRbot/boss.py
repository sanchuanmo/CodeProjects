# boss 数据
from player import Player
import re
class Boss(object):
    blood = [6000000, 8000000, 10000000, 12000000, 20000000]  # boss血量数据
    round = 1   # 周目
    i = 1   # 序号
    blood_remain = blood[0]  # 剩余血量


    def hurtNum(self, name:str,hurtNum:int)->str:
        # 伤害计算
        message_return = ""
        old_round = self.round
        old_i = self.i
        self.blood_remain = self.blood_remain - hurtNum
        # 伤害高于血量，击杀 需要存储之前的round，之前的i，和hurtNum
        if self.blood_remain <= 0:
            state = True
            if self.i == 5:
                self.round = self.round + 1
                self.i = 1
                self.blood_remain = self.blood[self.i-1]
            else:
                self.i = self.i + 1
                self.blood_remain = self.blood[self.i-1]
            message_return = message_return + "%s对%d周目%d王造成了%d伤害 击杀获得补刀\n" \
                                              "当前boss为%d周目%d王\t血量为%d" \
                             % (name, old_round, old_i, hurtNum, self.round, self.i, self.blood_remain)
            self.record_playerHurtNum(self,name, old_round, old_i, hurtNum, state)
        elif self.blood_remain > 0 :
            state = False
            message_return = message_return + "%s对%d周目%d王造成了%d伤害\n当前boss为%d周目%d王\t血量为%d"\
                             % (name, old_round, old_i, hurtNum, self.round, self.i, self.blood_remain)
            self.record_playerHurtNum(self,name,old_round,old_i,hurtNum,state)
        return message_return
    def record_playerHurtNum(self,name:str,old_i:int,old_round:int,hurtnum:int,state:bool):
        if Player.fight_data.get(name):
            Player.fight_data[name].append([old_round,old_i,hurtnum,state])
        elif not Player.fight_data.get(name):
            Player.fight_data[name] = []
            Player.fight_data[name].append([old_round, old_i, hurtnum, state])
    def split_message(self, message):
        print(message)
        role01 = r'^(\w+)\s+(\d+)$'
        role02 = r'^(\w+@\w+)\s+(\d+)$'
        role03 = r'^(\w+)\s+(\d+)\s+(\d+)\s+(\d+)$'
        if message.startswith("完成") or message.startswith("强行下树"):
            # 处理 完成 32141234
            m = re.match(role01,message)
            print(m.group(1),m.group(2))
            return m.group(2)
        elif message.startswith("代打"):
            # 处理 代打@dfa 242314
            m = re.match(role02,message)
            print(m.group(1),m.group(2))
            return m.group(2)
        elif message.startswith("修正"):
            # 处理 修正 round i blood_remain
            m = re.match(role03,message)
            return m.group(2),m.group(3),m.group(4)
    def recall_last_hurtNum(self,name):
        message_return = ""
        if Player.fight_data.get(name):
            data = Player.fight_data.get(name)[-1]
            # data [round,i,hurtNum,False]
            if data[-1] is False and data[0] == self.round and data[1] == self.i:
                self.blood_remain = self.blood_remain + data[2]
                Player.fight_data[name].pop()
                message_return = "已撤回出刀" + self.get_boss_info(self)
            else:
                message_return = "撤回失败"
        else:
            message_return = "撤回失败"
        return message_return
    def get_boss_info(self):
        return "当前为\n%d周目%d王\n剩余血量为%d" %(self.round,self.i,self.blood_remain)
    def set_boss_info(self,round,i,blood_remain):
        self.round = round

        if i < 5 and blood_remain <= self.blood[i] :
            self.i = i
            self.blood_remain = blood_remain
            message_return = "设置成功\n" + self.get_boss_info(self)
        else:
            message_return = "设置非法数据，请重新设置"
        return message_return


if __name__ == "__main__":
    hurtNum = Boss.split_message(Boss,"完成 13242")
    print("hurtnum")
    print(hurtNum)
    print(isinstance(hurtNum,str))
    # print(Boss.blood)
    #
    # print(Boss.hurtNum(Boss,"demo",1000000,))
    # print(Boss.hurtNum(Boss,"demo2",40000000))
    #
    # print(Player.read(Player,Player.fight_data))
    hurtNum = Boss.split_message(Boss,"完成 32141234")
    print(hurtNum)
    hurtNum, name = Boss.split_message(Boss,"代打@demo 1432421")
    print(hurtNum,name)
    print(Boss.set_boss_info(Boss,1,2,34))
