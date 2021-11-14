import pandas as pd
import json


def regCode_rzp(data):
    with open('reg_zp.ini', 'rb') as f:
        rzp = f.read().decode('utf-8')
    rzp = rzp.split('\r')
    rzp_d = {}
    for i in rzp:
        t = i.split('\t')
        if len(t) == 2:
            rzp_d[t[0].replace('\n', '').strip().lower()] = t[1]

    with open('reg_code.json', 'rb') as f:
        t = json.loads(f.read())
    data['REG_CODE'] = data['REG_CODE'].fillna('0')
    data['REG_ZP'] = data['REG_CODE'].astype(str)
    data['REG_CODE'] = data['REG_CODE'].astype(int)
    data['REG_ZP'] = data['REG_ZP'].map(t)
    data['REG_ZP'] = data['REG_ZP'].map(rzp_d)

    mzp_rf = '51344'
    data['REG_ZP'] = data['REG_ZP'].fillna(mzp_rf)
    data.to_csv('t12323123.csv', sep=';')
    data['REG_ZP'] = data['REG_ZP'].astype(int)

def new_income(data):
    data["INCOME_MAIN_AMT"] = data['INCOME_MAIN_AMT'].fillna(data['REG_ZP'])
    data['INCOME_MAIN_AMT'] = data['INCOME_MAIN_AMT'].apply(lambda x: str(x).replace(',','.')).astype(float)
    data['NEW_INC'] = data['INCOME_MAIN_AMT'] / (data['DEPENDANT_CNT'] + 1)

def sr_inc(data):
    data['srinc'] = data['NEW_INC'] >= (data['REG_ZP'] / (data['DEPENDANT_CNT'] + 1) )
    data["srinc"] = data['srinc'].astype(int)


def change(data):
    regCode_rzp(data)
    new_income(data)
    sr_inc(data)

