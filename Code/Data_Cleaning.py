import pandas as pd
import numpy as np
import re

from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv(r'./result_1.csv')
data.columns = ['name', 'sex', 'nation', 'age', 'native_place', 'address', 'degree', 'job', 'case_name', 'case_id',
                'court', 'charge', 'charge_type', 'charge_year', 'charge_month', 'charge_money']

# 处理性别，用众数（男）填充缺失值,1代表男，0代表女
data['sex'] = data['sex'].apply(lambda x: 0 if x == '女' else 1)

# 处理年龄，只保留出生日期的年份，再用2018减去年份得到年龄，用均值填充空值
data['age'].replace(np.nan, 0, inplace=True)
data['age'] = data['age'].astype(str)
data['age'] = data['age'].apply(lambda x: int(re.search(r'\d+', x).group()))
data['age'] = data['age'].apply(lambda x: 2018 - x if x > 100 else x)
data['age'].replace(0, int(data['age'].sum() / (2619 - 130)), inplace=True)

# 处理籍贯，如果为空，则用住址填充
data['native_place'].replace(np.nan, 0, inplace=True)
data['native_place'] = list(map(lambda x, y: y if x == 0 else x, data['native_place'], data['address']))

# 处理文化程度
data['degree'].replace('大学', '本科', inplace=True)
data['degree'].replace('大学本科', '本科', inplace=True)
data['degree'].replace('大学专科', '大专', inplace=True)
data['degree'].replace('专科', '大专', inplace=True)
data['degree'].replace('职业高中', '中专', inplace=True)
data['degree'].replace('职高', '中专', inplace=True)
data['degree'].replace('初中肄业', '初中', inplace=True)
data['degree'].replace('小学肄业', '小学', inplace=True)

# 处理职业，用无业填充空值
data['job'].replace(np.nan, '无业', inplace=True)

# 处理刑期
# 处理判刑类型特征：数据集中共有三种判刑方式（有期徒刑、拘役和空值），分别标记
data['charge_type'] = data['charge_type'].astype(str)
data['charge_type'] = list(map(lambda x: 1 if '有期徒刑' in x else (2 if '拘役' in x else 0), data['charge_type']))
# 处理刑期时间特征，以月为单位计算
data['charge_year'].replace(np.nan, 0, inplace=True)
data['charge_month'].replace(np.nan, 0, inplace=True)
data['charge_time'] = list(map(lambda x, y: 12 * x + y, data['charge_year'], data['charge_month']))

# 对非数值型特征进行labelEncoder编码
le = LabelEncoder()
data['native_place'] = data['native_place'].astype(str)
le.fit(data['native_place'])
data['native_place'] = le.transform(data['native_place'])

data['degree'] = data['degree'].astype(str)
le.fit(data['degree'])
data['degree'] = le.transform(data['degree'])

data['job'] = data['job'].astype(str)
le.fit(data['job'])
data['job'] = le.transform(data['job'])

data['case_id'] = data['case_id'].astype(str)
le.fit(data['case_id'])
data['case_id'] = le.transform(data['case_id'])

data['court'] = data['court'].astype(str)
le.fit(data['court'])
data['court'] = le.transform(data['court'])

data['charge'] = data['charge'].astype(str)
le.fit(data['charge'])
data['charge'] = le.transform(data['charge'])


# 删除不需要的特征
data.drop(['name', 'nation', 'address', 'case_name', 'charge_year', 'charge_month'], axis=1, inplace=True)

# 输出文件
data.to_csv(r'./data.csv', encoding='utf_8_sig', index=None)
