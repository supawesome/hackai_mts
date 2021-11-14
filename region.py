import pandas as pd
import dbf
import json

data_folder = 'data_folder'
table = dbf.Table(filename='PIndx20.dbf')
table.open(dbf.READ_ONLY)
reg_dict = {}
for record in table:
    reg_dict[record.INDEX.strip()] = record.REGION.strip()
table.close()
train1 = pd.read_csv(f'{data_folder}\\train_1.csv', sep=';')
train1 = train1[train1['LOCATION_NAME'].notna()]
train2 = pd.read_csv(f'{data_folder}\\train_2.csv', sep=';')
test1 = pd.read_csv(f'{data_folder}\\test_1.csv', sep=';')
test1 = test1[test1['LOCATION_NAME'].notna()]
test2 = pd.read_csv(f'{data_folder}\\test_2.csv', sep=';')
data = pd.concat([train1, test1])
d2 = pd.concat([train2, test2])
d2 = d2.set_index('ID')
data = data.set_index('ID')
data = data[data['LOCATION_NAME'].notna()]
data['LOCATION_NAME'] = data['LOCATION_NAME'].apply(lambda x : x.split('\\')[-1].split( )[0])
data['LOCATION_NAME'] = data['LOCATION_NAME'].map(reg_dict)
data.dropna(inplace=True)

data['LOCATION_NAME'] = data['LOCATION_NAME'].apply(lambda x: x.lower())
data['reg'] = d2["REG_CODE"]
rd = {}
it_d = data.groupby('reg')['LOCATION_NAME'].value_counts().to_dict()
for i in it_d:
    if i[0] in rd.keys():
        continue
    rd[i[0]] = i[1]

with open('reg_code.json', 'w') as f:
    f.write(json.dumps(rd))

#перобразование
t2 = pd.read_csv(f'{data_folder}\\train_2.csv', sep=';')
