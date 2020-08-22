from boss import Boss as Boss
from player import Player


# import re
#
# roleNormal = r'^(\w+)\s+(\d+)$'
# roleUnnormal = r'^(\w)@(\w)\s+(\d)$'
#
# m = re.match(roleNormal,"完成 12341234324")
#
# print(m)
#
# m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
#
# print(m)
import datetime
import threading
fight_data = {"三川":[[1,1,34535535,False],[1,2,43535,False]],"四川":[[1,1,353535,True],
                                                                             [1,2,45235,True]]}



def timerClear_fight_data():
    print("start")
    if datetime.datetime.now().minute == 22:
        fight_data.clear()
        print("fight_data")
        print(fight_data)
    global t1
    t1 = threading.Timer(15,timerClear_fight_data)
    t1.start()


timer = threading.Timer(15,timerClear_fight_data)

timer.start()