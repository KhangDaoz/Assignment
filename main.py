import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def find_correlation(df):
  # computing standard correlation coefficient
  corr_matrix = df.corr()
  # fetch and return attribute correlates 
  # with the median housing value
  return corr_matrix["Transfer Value"].sort_values(
    ascending=False)

def process_transfer_values(value):
    value = value[1::]
    n = len(value)
    value = value[:n - 1:]
    return float(value)

# read data
df = pd.read_csv('result.csv')
df_transfer = pd.read_csv('player_transfer_values.csv')

# preprocess to merge
df = df[df['Minutes'] > 900]
df['Age'] = df['Age'].apply(lambda x : float(f'{(int(x.split('-')[0]) + (int(x.split('-')[1]) / 365)):.2f}'))
df_transfer['Player'] = df_transfer['Player'].replace('Igor Júlio', 'Igor')
df_transfer['Transfer Value'] = df_transfer['Transfer Value'].apply(process_transfer_values)


# merge dataframe
df = pd.merge(df, df_transfer, how = 'left', on = ['Player']).dropna().reset_index(drop = True)
df = df.drop(columns = ['Player', 'Nation', 'Team_x', 'Team_y', 'GA90', 'Save%', 'CS%', 'Penalty Kicks Save%'])
df = df.replace('N/a', 0)
df = df.astype({
    'SoT%' : 'float',
    'G/sh' : 'float', 
    'Dist' : 'float', 
    'Long Pass completion' : 'float',
    'Succ%' : 'float',
    'Tkld%' : 'float',
    'Won%' : 'float'
})


# obj = (df.dtypes == 'object')
# object_cols = list(obj[obj].index)
# print("Categorical variables:",len(object_cols))
# print(object_cols)
# int_ = (df.dtypes == 'int')
# num_cols = list(int_[int_].index)
# print("Integer variables:",len(num_cols))

# fl = (df.dtypes == 'float')
# fl_cols = list(fl[fl].index)
# print("Float variables:",len(fl_cols))

# numerical_dataset = df.select_dtypes(include=['number'])

# plt.figure(figsize=(50, 30))
# sns.heatmap(numerical_dataset.corr(),
#             cmap = 'BrBG',
#             fmt = '.2f',
#             linewidths = 2,
#             annot = True)
# plt.savefig('CoV.png', dpi=300, bbox_inches='tight')

'''
df = df.drop(columns = ['Position', 'Yellow Cards', 'Red Cards', 'SoT%', 'G/sh', 'Dist', 'Passes Completed', 'Pass Completion', 'TotDist', 'Short Pass completion', 'Medium Pass completion', 'Long Pass completion', 'CrsPA', 'Tkl', 'TklW', 'Att', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int', 'Touches', 'Def Pen', 'Def 3rd', 'Succ%', 'Tkld%', 'Won', 'Miscellaneous Stats Lost'])

X = df.drop(['Transfer Value'], axis=1)
Y = df['Transfer Value']

X_train, X_valid, Y_train, Y_valid = train_test_split(
    X, Y, train_size=0.8, test_size=0.2, random_state=0)
# df.to_csv('test.csv', encoding = 'utf-8-sig', index = False)

model_RFR = RandomForestRegressor(n_estimators=10)
model_RFR.fit(X_train, Y_train)
Y_pred = model_RFR.predict(X_valid)

print(mean_absolute_percentage_error(Y_valid, Y_pred))

model_LR = LinearRegression()
model_LR.fit(X_train, Y_train)
Y_pred = model_LR.predict(X_valid)

print(mean_absolute_percentage_error(Y_valid, Y_pred))
'''

# print(df.info())

# df = df.drop(columns = 'Position')
# cor_coef = find_correlation(df)
# # print("Correlation Coefficient::", cor_coef)
# plt.figure(figsize=(8, 5))
# # df.plot(kind = 'scatter', x = 'Age', y = 'Transfer Value', alpha = 0.1)
# df.hist(column='Age', 
#              bins=50, figsize=(9,6))
# plt.savefig('DF.png', dpi=300, bbox_inches='tight')
# print(df.shape)


df = df.drop(columns = ['Position', 'Yellow Cards', 'Red Cards', 'SoT%', 'G/sh', 'Dist', 'Passes Completed', 'Pass Completion', 'TotDist', 'Short Pass completion', 'Medium Pass completion', 'Long Pass completion', 'CrsPA', 'Tkl', 'TklW', 'Att', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int', 'Touches', 'Def Pen', 'Def 3rd', 'Succ%', 'Tkld%', 'Won', 'Miscellaneous Stats Lost'])
# Nhóm tuổi phù hợp với histogram của bạn
bins = [17, 22, 25, 28, 31, 35, 100]
labels = [1, 2, 3, 4, 5, 6]

df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

# Kiểm tra phân phối sau khi chia nhóm
print(df['AgeGroup'].value_counts())
X = df.drop(['Transfer Value'], axis=1)
y = df['Transfer Value']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    stratify=df['AgeGroup'],
    test_size=0.2,
    random_state=0
)
# print("Train set:")
# print(X_train['AgeGroup'].value_counts(normalize=True))
# print("\nTest set:")
# print(X_test['AgeGroup'].value_counts(normalize=True))

model = RandomForestRegressor(
    n_estimators=100,      # số lượng cây, 100 là đủ ổn cho bài này
    max_depth=None,        # để tự động grow
    random_state = 42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

print(f'MAE: {mae:.2f}')
print(f'MAPE: {mape*100:.2f}%')

# Tạo và huấn luyện mô hình Linear Regression
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)

# Dự đoán trên dữ liệu test
y_pred_lr = model_lr.predict(X_test)

# Tính toán MAE và MAPE cho Linear Regression
mae_lr = mean_absolute_error(y_test, y_pred_lr)
mape_lr = mean_absolute_percentage_error(y_test, y_pred_lr)

# In kết quả
print(f'Linear Regression MAE: {mae_lr:.2f}')
print(f'Linear Regression MAPE: {mape_lr*100:.2f}%')