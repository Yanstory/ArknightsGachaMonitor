# -*- coding: utf-8 -*-
from flask import Flask, request
import json
import random
import os
from copy import deepcopy
from time import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

# 常量部分
# 保底数量(修改为0时无保底)
startAdd = 50
# 抽出概率，依次为：六星，六星保底概率增加，五星，四星
percentageSSSR = 2
percentageSSSRAdd = 2
percentageSSR = 8
percentageSR = 50
# 特殊UP活动,分别对应3、4、5、6
chanceUp = [[], [], [], []]
# 自定义抽卡数据，当此项设为True时随机抽卡功能无效
selfDefined = False
# 自定义的抽卡数据干员ID，可在127.0.0.1:5000/showDb中查询。一定要填满十个！
selfDefinedList = []
# 是否允许抽出特定干员，默认False表示不抽出
allowLimitOp = False
# 特定干员列表，包括公招限定、特别赠送、活动限定
limitOpList = ['estell', 'tiger', 'hpsts',
               'savage', 'amiya',
               'grani', 'ceylon', 'bison']

# 传输格式常量
dataResponse = {"gachaResultList": [], "playerDataDelta": {}}
gachaResultList = {"charInstId": -1, "charId": "", "isNew": 1, "itemGet": []}
itemGet = {"type": "", "id": "", "count": -1}
status = {"diamondShard": 10000, "hggShard": 0, "lggShard": 0}
playerDataDelta = {"modified": {}, "deleted": {}}
modified = {"status": {}, "troop": {}, "inventory": {}}  # , "dexNav": {}, "building": {}
troop = {"chars": {}, "curCharInstId": -1}
troopChar = {"instId": -1, "charId": "", "favorPoint": 0, "potentialRank": 0, "mainSkillLvl": 1,
             "skin": "char_290_vigna#1", "level": 1, "exp": 0, "evolvePhase": 0, "defaultSkillIndex": 0,
             "gainTime": -1, "skills": []}
verifyData = {"uid": "-1", "channelUid": "-1", "isGuest": 0, "platform": 1}

# 统计用变量
listR = [[], [], [], []]  # 干员列表
listName = [[], [], [], []]  # 干员名
listCount = [[], [], [], []]  # 抽取数量统计
total = 0  # 总抽取数量
save = 0  # 保底统计


def db_init():
    global listR, listCount
    print '[I] 从' + os.path.abspath('../constData') + '读取数据表。'
    with open(os.path.abspath('../constData') + '/character_table.json', 'r') as infile:
        js = json.loads(infile.read())
        for (key, value) in js.items():
            rarity = value["rarity"]
            if rarity > 1:
                if key.startswith('token'):  # 前缀检测，防止召唤物导致结果异常
                    continue
                if not(allowLimitOp):  # 禁止特定干员检测
                    flagFound = False
                    for op in limitOpList:
                        if key.endswith(op):    # 后缀检测
                            flagFound = True
                            break
                    if flagFound: continue
                '''
                if key.endswith('estell') or key.endswith('savage') or key.endswith('grani') or key.endswith(
                        'tiger') or key.endswith('hpsts') or key.endswith('amiya'):  # 后缀检测，去除公招限定
                    continue
                '''
                listR[rarity - 2].append(key)
                listName[rarity - 2].append(value['name'])
                listCount[rarity - 2].append(0)
    print('Database Inited')


def getChance():
    sssr_percentage = percentageSSSR
    if startAdd == 0:
        return sssr_percentage
    if save > startAdd:
        sssr_percentage += (save - startAdd) * percentageSSSRAdd
    return sssr_percentage


def getGachaItem(rarity):
    l1 = len(listR[rarity - 3])
    l2 = len(chanceUp[rarity - 3])
    if l2 != 0:
        if random.randrange(1, 3) == 1:
            return chanceUp[rarity - 3][random.randrange(0, l2)]
    return listR[rarity - 3][random.randrange(0, l1)]


def gachaGetList():
    global total, save
    gachaList = []
    for i in range(10):
        s = random.randrange(1, 101)
        chance = getChance()
        print 'S:{}, Chance:{}'.format(s, chance)
        if s <= chance:
            print('SSSR')
            total += 1
            save = 0
            gachaList.append(getGachaItem(6))
        elif s <= chance + percentageSSR:
            print('SSR')
            total += 1
            save += 1
            gachaList.append(getGachaItem(5))
        elif s <= chance + percentageSSR + percentageSR:
            print('SR')
            total += 1
            save += 1
            gachaList.append(getGachaItem(4))
        else:
            print('R')
            total += 1
            save += 1
            gachaList.append(getGachaItem(3))
    return gachaList


def dataTest():
    if selfDefined and len(selfDefinedList) != 10:
        print('[E] 检测到启用了自定义列表但列表中干员数目有误。')
        return False
    if startAdd < 0:
        print('[E] 检测到保底起始数目有误。')
        return False
    if percentageSSSR < 0 or percentageSSSR > 100:
        print('[E] 检测到概率超出范围。')
        return False
    if percentageSSSRAdd < 0:
        print('[E] 检测到保底概率超出范围。')
        return False
    return True


def generateData(charList):
    gacha_list = []
    troop_chars_dict = {}
    t = time()
    i = 15
    for char_info in charList:
        troop_data = deepcopy(troopChar)
        troop_data.update({'instId': '{}'.format(i), 'charId': char_info, 'skin': '{}#1'.format(char_info),
                           'gainTime': '{}'.format(int(t))})
        troop_chars_dict.update({'{}'.format(i): troop_data})
        gacha_data = deepcopy(gachaResultList)
        gacha_data.update({'charInstId': i, 'charId': char_info})
        gacha_list.append(gacha_data)
        i += 1
    player_data = deepcopy(playerDataDelta)
    modified_data = deepcopy(modified)
    troop_data_main = deepcopy(troop)
    troop_data_main.update({'curCharInstId': i, 'chars': troop_chars_dict})
    modified_data.update({'status': status, 'troop': troop_data_main})
    data_response = deepcopy(dataResponse)
    player_data.update({'modified': modified_data})
    data_response.update({'gachaResultList': gacha_list, 'playerDataDelta': player_data})
    return data_response


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/gacha/syncNormalGacha')
def syncGacha():
    return json.dumps({
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    })


@app.route('/account/syncData', methods=['POST', 'GET'])
def syncData():
    with open(os.path.abspath('../constData') + '/syncData.json', 'r') as sync_data_json:
        return sync_data_json.read()


@app.route('/u8/user/verifyAccount', methods=['POST'])
def verifyAccount():
    data = request.get_data()
    verify_data = json.loads(data.encode('utf-8'))
    uid = verify_data['uid']
    local_verify_data = deepcopy(verifyData)
    local_verify_data.update({'uid': uid})
    return json.dumps(local_verify_data)


@app.route('/showDb')
def print_db():
    output = '''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8" />
    <title>干员列表</title>
    </head>
    <body>

    '''
    rare_list = ['三星', '四星', '五星', '六星']
    for i in range(4):
        output += ('<center style="font-size:18px;color:#FF0000">' + rare_list[i] + '</center>\n<center>')
        for j in range(len(listR[i])):
            output += (listName[i][j] + ' : ' + listR[i][j] + '<br/>')
        output += '</center>'
    output += '''
    </body>
    </html>
    '''
    return output


@app.route('/gacha/tenAdvancedGacha', methods=['POST', 'GET'])
def gacha():
    if selfDefined:
        return json.dumps(generateData(selfDefinedList))
    else:
        return json.dumps(generateData(gachaGetList()))


db_init()
if __name__ == '__main__':
    if dataTest():
        app.run()
