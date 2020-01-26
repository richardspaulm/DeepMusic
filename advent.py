from math import floor
import requests
# s = "87201 146745 99430 67664 67482 72598 114480 111866 146672 51465 59100 87507 106993 61427 97982 133329 133510 117352 58800 129228 102366 77934 149630 71567 139965 130271 53259 134032 54158 74679 148463 101585 51744 112537 59140 92980 83174 67797 58890 55849 50424 112780 104595 114465 90528 86503 51661 124689 101081 81478 124821 83420 108738 76506 111217 104897 133747 128808 81563 106688 67129 130968 75576 101197 129318 135015 149839 110182 104687 147803 140555 70447 63224 85143 146115 77789 64003 115257 61397 86873 143481 129785 68764 99388 91050 109136 101777 98104 103643 131374 83808 125949 147277 144448 112673 136408 75776 141630 116821 113349"
# s = s.split(" ")

# def calc_fuel(mass):
#     return floor(mass/3) - 2

# def extra_fuel(module):
#     fuel_sum = 0
#     fuel_weight = calc_fuel(module)
#     while fuel_weight > 0:
#         fuel_sum += fuel_weight
#         fuel_weight = calc_fuel(fuel_weight)
#     return fuel_sum


# s = [int(i) for i in s]
# fuel_reqs = [calc_fuel(i) for i in s]
# fuel_reqs = [i + extra_fuel(i) for i in fuel_reqs]
# print(fuel_reqs)
# ##### List of all fuel requirements for the module
# sm = sum(fuel_reqs)

# print(sm)


###### DAY 2 ############# ########### DAY5 ##########
######### Decode Intcode byte ########

class IntComputer:
    def __init__(self):
        self.intcode = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,65,39,225,2,14,169,224,101,-2340,224,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1001,144,70,224,101,-96,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,92,65,225,1102,42,8,225,1002,61,84,224,101,-7728,224,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,67,73,224,1001,224,-4891,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1102,54,12,225,102,67,114,224,101,-804,224,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,19,79,225,1101,62,26,225,101,57,139,224,1001,224,-76,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1102,60,47,225,1101,20,62,225,1101,47,44,224,1001,224,-91,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1,66,174,224,101,-70,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,226,224,102,2,223,223,1005,224,329,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,374,1001,223,1,223,1108,226,677,224,1002,223,2,223,1005,224,389,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,419,1001,223,1,223,1008,226,677,224,102,2,223,223,1005,224,434,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,108,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,569,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,584,101,1,223,223,1107,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,629,1001,223,1,223,107,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,677,224,102,2,223,223,1006,224,659,101,1,223,223,1008,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]
        self.pointer = 0
        self.input_code = 5 #int(input("Please enter the input code: "))
    def iterate_intcode(self):
        while self.pointer < len(self.intcode):
            self.process_intcode()
    def process_intcode(self):
        code = self.intcode[self.pointer]
        param1 = True
        param2 = True
        param3 = True
        code_str = str(code)
        if len(code_str) > 1:
            instruction = int(code_str[-2:])
            for i in range(-3, len(code_str) * -1 - 1, -1):
                if i == -3:
                    if code_str[i] != "0":
                        param1 = False
                if i == -4:
                    if code_str[i] != "0":
                        param2 = False
                if i == -5:
                    if code_str[i] != "0":
                        param3 = False
        else:
            instruction = code
        if instruction == 1:
            self.add_and_replace(param1, param2, param3)
        if instruction == 2:
            self.mult_and_replace(param1, param2, param3)
        if instruction == 3:
            self.insert_input()
        if instruction == 4:
            self.display_output()
        if instruction == 5:
            self.jump_if_true(param1, param2)
        if instruction == 6:
            self.jump_if_false(param1, param2)
        if instruction == 7:
            self.less_than(param1, param2, param3)
        if instruction == 8:
            self.equals(param1, param2, param3)
        if instruction == 99:
            print("Terminating Program")
            exit()
    def jump_if_true(self, param1, param2):
        pos1 = self.fetch_pos(param1, 1)
        pos2 = self.fetch_pos(param2, 2)
        if pos1 != 0:
            self.pointer = pos2
        else:
            self.pointer += 3
    def jump_if_false(self, param1, param2):
        pos1 = self.fetch_pos(param1, 1)
        pos2 = self.fetch_pos(param2, 2)
        if pos1 == 0:
            self.pointer = pos2
        else:
            self.pointer += 3        
    def less_than(self, param1, param2, param3):
        pos1 = self.fetch_pos(param1, 1)
        pos2 = self.fetch_pos(param2, 2)
        pos3 = self.fetch_pos(param3, 3)
        if pos1 < pos2:
            self.intcode[pos3] = 1
        else:
            self.intcode[pos3] = 0
        self.pointer += 4
    def equals(self, param1, param2, param3):
        pos1 = self.fetch_pos(param1, 1)
        pos2 = self.fetch_pos(param2, 2)
        pos3 = self.fetch_pos(param3, 3)
        if pos1 == pos2:
            self.intcode[pos3] = 1
        else:
            self.intcode[pos3] = 0
        self.pointer += 4        

    def display_output(self):
        pos = self.intcode[self.pointer + 1]
        print("OUTPUT:", str(self.intcode[pos]))
        self.pointer += 2
    def insert_input(self):
        pos = self.intcode[self.pointer + 1]
        self.intcode[pos] = self.input_code
        self.pointer += 2
    def add_and_replace(self, param1, param2, param3):
        pos1 = self.fetch_pos(param1, 1)
        pos2 = self.fetch_pos(param2, 2)
        replace_pos = self.intcode[self.pointer + 3]
        new_value = pos1 + pos2
        self.intcode[replace_pos] = new_value
        self.pointer += 4
    def mult_and_replace(self, param1, param2, param3):
        pos1 = self.fetch_pos(param1, 1)
        pos2 = self.fetch_pos(param2, 2)
        replace_pos = self.intcode[self.pointer + 3]
        new_value = pos1 * pos2
        self.intcode[replace_pos] = new_value
        self.pointer += 4
    def fetch_pos(self, param, param_num):
        if param:
            pos = self.intcode[self.intcode[self.pointer + param_num]]
        else:
            pos = self.intcode[self.pointer + param_num]
        return pos
ic = IntComputer()
ic.iterate_intcode()
########## DAY 3 ############
#Get source data and convert to array
# line1 = "R994,U598,L555,D997,R997,U529,L251,U533,R640,U120,L813,U927,L908,U214,L276,U306,L679,U187,R156,D654,L866,D520,R299,U424,R683,U49,R965,U531,R303,D4,L210,U425,R99,D892,R564,D671,L294,D908,L89,U855,R275,U790,R214,D588,L754,D873,R297,D97,R979,U850,L953,D281,L580,D254,L747,U115,L996,U641,R976,U585,L383,U498,L112,U329,R650,U772,L952,U325,L861,U831,R71,D853,R696,D812,R389,U456,L710,D116,R789,D829,L57,D940,R908,U569,R617,D832,L492,D397,R152,U898,L960,D806,L867,U928,L617,D281,L516,D214,R426,U530,R694,U774,L752,U215,L930,U305,R463,U774,R234,U786,R425,U470,R90,D383,R692,D626,L160,D588,L141,D351,R574,D237,L869,D499,R873,U856,R148,D919,L582,D804,L413,U201,L247,U907,L828,D279,L28,D950,L587,U290,R636,U344,L591,U118,L614,U203,R381,U634,L301,D197,R594,D373,L459,U504,L703,U852,L672,U613,R816,D712,R813,U97,R824,D690,L556,D308,L568,D924,L384,U540,R745,D679,R705,D808,L346,U927,R145,U751,L769,D152,L648,D553,L738,U456,R864,U486,R894,D923,R76,U211,L78,U145,R977,U297,R93,U200,L71,U665,L392,D309,L399,D594,R118,U552,L328,U317,R369,D109,L673,D306,R441,U836,L305,D59,L870,U648,L817,D381,R676,U711,R115,U344,L815,U286,R194,U526,R844,U106,L547,D312,L116,U783,R786,D390,L115,D483,R691,U802,R569,U13,R854,D90,R22,D819,L440,D13,R438,D640,L952,D394,R984,D825,R1,D554,R349,U746,L816,U301,L397,D85,R437,D746,L698,D75,L964,U155,L268,U612,R838,D338,L188,U38,R830,U538,L245,D885,R194,D989,R8,D69,L268,D677,R163,U784,L308,U605,L737,U919,R117,U449,R698,U547,L134,D860,L234,U923,R495,D55,R954,D531,L212"
# line2 = "L1005,D937,L260,D848,R640,U358,R931,U495,R225,U344,R595,U754,L410,D5,R52,D852,L839,D509,R755,D983,R160,U522,R795,D465,R590,U558,R552,U332,R330,U752,R860,D503,L456,U254,R878,D164,R991,U569,R44,U112,L258,U168,L552,U68,R414,U184,R458,D58,R319,U168,R501,D349,R204,D586,R241,U575,L981,D819,L171,D811,L960,U495,R192,D725,R718,D346,R399,D692,L117,D215,L390,U364,L700,D207,R372,U767,L738,D844,L759,D211,R287,U964,R328,D800,R823,U104,L524,D68,R714,D633,R565,D373,R883,U327,R222,D318,L58,D451,R555,D687,R807,U638,L717,U298,R849,D489,L159,D692,L136,U242,R884,U202,R419,U41,L980,U483,R966,D513,L870,D306,R171,D585,R71,D320,R914,U991,R706,U440,R542,D219,L969,U9,R481,U164,R919,U17,L750,U775,R173,U515,L191,D548,L515,U54,L132,U56,R203,U544,L796,D508,L321,D517,L358,U12,L892,D472,L378,U121,L974,U36,R56,D758,L680,D17,L369,D72,L926,D466,L866,U850,R300,D597,L848,U17,L890,D739,L275,U560,L640,U602,R238,U919,R636,D188,R910,D992,L13,U241,R77,U857,R453,U883,L881,D267,R28,U928,R735,U731,L701,D795,R371,U652,R416,D129,R142,D30,R442,U513,R827,U455,L429,D804,R966,D565,R326,U398,R621,U324,L684,D235,L467,D575,L200,D442,R320,D550,R278,U929,R555,U537,L416,U98,R991,D271,L764,U841,L273,D782,R356,D447,R340,U413,R543,U260,L365,D529,R721,U542,L648,U366,R494,U243,L872,U201,L440,U232,R171,D608,R282,U484,R81,D320,R274,D760,L250,U749,L132,D162,L340,D308,L149,D5,L312,U547,R686,D684,R133,D876,L531,U572,R62,D142,L218,U703,L884,U64,L889,U887,R228,U534,R624,D524,R522,D452,L550,U959,R981,U139,R35,U98,R212"
# line1 = line1.split(",")
# line2 = line2.split(",")


####Decode each item as direction and create coordinates

line1_points = list()
line2_points = list()

# line1_x = 0
# line1_y = 0
# line2_x = 0
# line2_y = 0
# for i in range(len(line1)):
#     instruction1 = line1[i]
#     direction1 = instruction1[0]
#     steps1 = int(instruction1[1:])    
#     instruction2 = line2[i]
#     direction2 = instruction2[0]
#     steps2 = int(instruction2[1:])    



# xPos = 0
# yPos = 0
# i = 0
# for instruction in line1:
#     direction = instruction[0]
#     steps = int(instruction[1:])
#     if direction == "R":
#         for step in range(steps):
#             i += 1
#             xPos += 1
#             line1_points.append({i : (xPos, yPos)})
#     if direction == "L":
#         for step in range(steps):
#             i += 1
#             xPos -= 1
#             line1_points.append({i : (xPos, yPos)})
#     if direction == "U":
#         for step in range(steps):
#             i += 1
#             yPos += 1
#             line1_points.append({i : (xPos, yPos)})
#     if direction == "D":
#         for step in range(steps):
#             i += 1
#             yPos -= 1
#             line1_points.append({i : (xPos, yPos)})
# xPos = 0
# yPos = 0
# i = 0
# for instruction in line2:
#     direction = instruction[0]
#     steps = int(instruction[1:])
#     if direction == "R":
#         for step in range(steps):
#             i += 1
#             xPos += 1
#             line2_points.append({i : (xPos, yPos)})
#     if direction == "L":
#         for step in range(steps):
#             i += 1
#             xPos -= 1
#             line2_points.append({i : (xPos, yPos)})
#     if direction == "U":
#         for step in range(steps):
#             i += 1
#             yPos += 1
#             line2_points.append({i : (xPos, yPos)})
#     if direction == "D":
#         for step in range(steps):
#             i += 1
#             yPos -= 1
#             line2_points.append({i : (xPos, yPos)})

# def calc_manhattan(point):
#     x = abs(point[0])
#     y = abs(point[1])
#     return x+y

# intersections = list()
# points1 = list()
# points2 = list()
# for i, pt in enumerate(line1_points):
#     points1.append(pt[i + 1])
# for i, pt in enumerate(line2_points):
#     points2.append(pt[i + 1])


# intersections = set(points2).intersection(set(points1))
# distances = [calc_manhattan(point) for point in intersections]

# print(intersections)

# distances2 = list()
# for intersection in intersections:
#     for steps in range(len(line1_points)):
#         if line1_points[steps][steps + 1] == intersection:
#             steps1 = steps
#     for steps in range(len(line2_points)):
#         if line2_points[steps][steps + 1] == intersection:
#             steps2 = steps
#     print(steps1 + steps2 - 2)



########## DAY 4 #########
# start = 109165
# end = 576723
# combinations = 0

# def has_double(num):
#     only_doubles = False
#     num_str = str(num)
#     char_counts = list()
#     for char in num_str:
#         count = 0
#         for char2 in num_str:
#             if char == char2:
#                 count += 1
#         char_counts.append(count)
#     if 2 in char_counts:
#         return True
#     return False


# def always_increase(num):
#     num_str = str(num)
#     for i in range(len(num_str) - 1):
#         if int(num_str[i]) > int(num_str[i + 1]):
#             return False
#     return True

# for i in range(start, end):
#     if has_double(i) and always_increase(i):
#         # print(i)
#         combinations += 1
# print(combinations)
