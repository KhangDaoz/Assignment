import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
df = df.drop(columns = ['Player', 'Nation', 'Team_x', 'Team_y'])

print(df.shape)

obj = (df.dtypes == 'object')
object_cols = list(obj[obj].index)
print("Categorical variables:",len(object_cols))
print(object_cols)
int_ = (df.dtypes == 'int')
num_cols = list(int_[int_].index)
print("Integer variables:",len(num_cols))

fl = (df.dtypes == 'float')
fl_cols = list(fl[fl].index)
print("Float variables:",len(fl_cols))

# df.to_csv('test.csv', encoding = 'utf-8-sig', index = False)