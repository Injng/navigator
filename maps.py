from classes import *
from initialize import *

# Identifier conventions
# 10000-50000 : Rooms
# 50000-90000 : Structures
# 100-900 : Stations
# even numbers: not controlled
# odd numbers: controlled

# Maps for structures
# a, b, c, d : entrances
# p : platform
# t : transfer corridor 
# s : security check
# z : empty space

dongchangan_street = [[False, False, False, False, False, False, False],
                      [False, False, 20010, False, 20012, False, False],
                      [False, 20000, 20002, 20004, 20006, 20008, False],
                      [False, False, 20016, False, 20014, False, False],
                      [False, False, False, False, False, False, False]]

xichangan_street = [[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                    [False, False, False, False, 30028, False, 30030, False, False, False, False, False, False, False, False, False],
                    [False, 30000, 30002, 30004, 30006, 30008, 30010, 30012, 30014, 30016, 30018, 30020, 30022, 30024, 30026, False],
                    [False, False, False, False, 30032, False, False, False, False, False, False, False, False, False, False, False],
                    [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]]

tiananmendong_station = [[False, False, False, False, False, False],
                         [False, 10004, False, False, 10006, False],
                         [False, 10000, 10001, 10003, 10002, False],
                         [False, 10010, False, False, 10008, False],
                         [False, False, False, False, False, False]]

tiananmenxi_station = [[False, False, False, False, False, False],
                       [False, 10016, False, False, 10018, False],
                       [False, 10012, 10005, 10007, 10014, False],
                       [False, 10020, False, False, False, False],
                       [False, False, False, False, False, False]]

# Room declarations
# East Changan Street

x4e20 = Room("东长安街", (2, 1), dongchangan_street, 5, [], 20000)
x4e22 = Room("东长安街", (2, 2), dongchangan_street, 5, [], 20002)
x4e24 = Room("东长安街", (2, 3), dongchangan_street, 5, [], 20004)
x4e26 = Room("东长安街", (2, 4), dongchangan_street, 5, [], 20006)
x4e28 = Room("东长安街", (2, 5), dongchangan_street, 5, [], 20008)
x4e2a = Room("天安门东A入口", (1, 2), dongchangan_street, 1, [Sign("北京地铁天安门东")], 20010, [-1, [tiananmendong_station], [(1, 1)]])
x4e2c = Room("天安门东B入口", (1, 4), dongchangan_street, 1, [Sign("北京地铁天安门东")], 20012, [-1, [tiananmendong_station], [(1, 4)]])
x4e2e = Room("天安门东C入口", (3, 4), dongchangan_street, 1, [Sign("北京地铁天安门东")], 20014, [-1, [tiananmendong_station], [(3, 4)]])
x4e30 = Room("天安门东D入口", (3, 2), dongchangan_street, 1, [Sign("北京地铁天安门东")], 20016, [-1, [tiananmendong_station], [(3, 2)]])

# West Changan Street


x7530 = Room("西长安街", (2, 1), xichangan_street, 5, [], 30000)
x7532 = Room("西长安街", (2, 2), xichangan_street, 5, [], 30002)
x7534 = Room("西长安街", (2, 3), xichangan_street, 5, [], 30004)
x7536 = Room("西长安街", (2, 4), xichangan_street, 5, [], 30006)
x7538 = Room("西长安街", (2, 5), xichangan_street, 5, [], 30008)
x753a = Room("西长安街", (2, 6), xichangan_street, 5, [], 30010)
x753c = Room("西长安街", (2, 7), xichangan_street, 5, [], 30012)
x753e = Room("西长安街", (2, 8), xichangan_street, 5, [], 30014)
x7540 = Room("西长安街", (2, 9), xichangan_street, 5, [], 30016)
x7542 = Room("西长安街", (2, 10), xichangan_street, 5, [], 30018)
x7544 = Room("西长安街", (2, 11), xichangan_street, 5, [], 30020)
x7546 = Room("西长安街", (2, 12), xichangan_street, 5, [], 30022)
x7548 = Room("西长安街", (2, 13), xichangan_street, 5, [], 30024)
x754a = Room("西长安街", (2, 14), xichangan_street, 5, [], 30026)
x754c = Room("天安门西A入口", (1, 4), xichangan_street, 1, [Sign("北京地铁天安门西")], 30028, [-1, [tiananmenxi_station], [(1, 1)]])
x754e = Room("天安门西B入口", (1, 6), xichangan_street, 1, [Sign("北京地铁天安门西")], 30030, [-1, [tiananmenxi_station], [(1, 4)]])
x7550 = Room("天安门西C入口", (3, 4), xichangan_street, 1, [Sign("北京地铁天安门西")], 30032, [-1, [tiananmenxi_station], [(3, 1)]])

# Tiananmen Dong Station
# Station #100


x2714 = Room("天安门东A入口", (1, 1), tiananmendong_station, 1, [Sign("天安门东A入口")], 10004, [1, [dongchangan_street], [(1, 2)]])
x2716 = Room("天安门东B入口", (1, 4), tiananmendong_station, 1, [Sign("天安门东B入口")], 10006, [1, [dongchangan_street], [(1, 4)]])
x2718 = Room("天安门东C入口", (3, 4), tiananmendong_station, 1, [Sign("天安门东C入口")], 10008, [1, [dongchangan_street], [(3, 4)]])
x271a = Room("天安门东D入口", (3, 1), tiananmendong_station, 1, [Sign("天安门东D入口")], 10010, [1, [dongchangan_street], [(3, 2)]])
x2710 = Room("安检", (2, 1), tiananmendong_station, 3, [Sign(security_check_string)], 10000)
x2712 = Room("安检", (2, 4), tiananmendong_station, 3, [Sign(security_check_string)], 10002)
x2711 = Room("天安门东地铁站", (2, 2), tiananmendong_station, 4, [Sign("天安门东")], 10001)
x2713 = Room("天安门东地铁站", (2, 3), tiananmendong_station, 4, [Sign("天安门东")], 10003)

# Tiananmen Xi Station
# Station #101

x2720 = Room("天安门西A入口", (1, 1), tiananmenxi_station, 1, [Sign("天安门西A入口")], 10016, [1, [xichangan_street], [(1, 4)]])
x2722 = Room("天安门西B入口", (1, 4), tiananmenxi_station, 1, [Sign("天安门西B入口")], 10018, [1, [xichangan_street], [(1, 6)]])
x2724 = Room("天安门西C入口", (3, 1), tiananmenxi_station, 1, [Sign("天安门西C入口")], 10020, [1, [xichangan_street], [(3, 4)]])
x271c = Room("安检", (2, 1), tiananmenxi_station, 3, [Sign(security_check_string)], 10012)
x271e = Room("安检", (2, 4), tiananmenxi_station, 3, [Sign(security_check_string)], 10014)
x2715 = Room("天安门西地铁站", (2, 2), tiananmenxi_station, 4, [Sign("天安门西")], 10005)
x2717 = Room("天安门西地铁站", (2, 3), tiananmenxi_station, 4, [Sign("天安门西")], 10007)

