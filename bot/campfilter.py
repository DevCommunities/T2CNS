from camp_parser import camphub_parser
import json
from os.path import join, dirname
import re

def get_recent_camp():
    camp = camphub_parser('https://www.camphub.in.th/computer/')
    return camp.info

def iscamp_update(test=False):
    camp = get_recent_camp()
    # if camp is the same as ./database/camp.json then return
    # else update ./database/camp.json (open in utf8)

    if test:
        database = './database/dummy.json' # Use this for testing
    else:
        database = './database/camp.json'
   
    with open(join(dirname(__file__), database), 'r', encoding='utf8') as f:
        old_camp = json.load(f)

    if camp == old_camp:
        return (False, camp, 0) # Change, camp, how much change(n camp)
    else:
        # check how much changes in camp
        changes = 0
        for i in range(len(camp)):
            if camp[i] != old_camp[i]:
                changes += 1

        data = json.dumps(camp, indent=4, ensure_ascii=False)
        # update json database
        with open(join(dirname(__file__), 'database', 'camp.json'), 'w', encoding='utf-8') as f:
            f.write(data)

        return (True, camp, changes) # Change, camp, how much change(n camp)

def recommend(camp):
    blacklist = ['Change Education', 'BASIC HUB', 'MarianOnilne', 'Hamster Hub', 'นั่งเดฟไอทีแคมป์', 'Learning Code Camp', 'Seek Activity Co., Ltd.', 'Learning Code Station', 'Zero to Hero Activity', 'rhythm of arts creative learning centre', 'ONCEs Thailand', 'Lighthouse Workshop', 'JTCA Co., Ltd.', 'The Explorer', 'SPHERE (สะ-เฟียร์) : Area of Learning', 'ONCEs Thailand  วันซ์ ไทยแลนด์ : พื้นที่เรียนรู้สำหรับเยาวชนไทย']
    def cost2num(x):
        x = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", x) # return list (can return more than one number such as ['1,450', '1,250'])
        x = [int(i.replace(',', '')) for i in x] # remove comma and convert to int
        return x

    # Reason empty by default
    if camp['costs'] == 'ฟรี':
        return True , ''

    # check for bullshit organizer
    elif camp['organizer'] in blacklist:
        return False, ''
    # overpriced
    elif float(cost2num(camp['costs'])[0]) > 500:
        return False, ''

    else:
        return None, ''
    