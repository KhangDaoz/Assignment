import pandas 
import matplotlib.pyplot as plt

# Identify the top 3 players with the highest and lowest scores for each statistic.
def identify_the_top_3_each_statistic(df):
    # Write the top 3 players with the highest and lowest scores for each statistic to a text file
    for header in df.columns[4:]:
        DF = df
        DF[header] = pandas.to_numeric(DF[header], errors='coerce')
        DF = DF.dropna(subset = [header])
        largest = DF.nlargest(3, header)
        smallest = DF.nsmallest(3, header)
        with open('top_3.txt', 'a', encoding = 'utf-8-sig') as f:
            f.write(f'Top 3 player with the highest {header}:\n')
            f.write(largest[['Player', 'Nation', 'Team', 'Position', header]].to_string(index = False))
            f.write('\n\n')
            f.write(f'Top 3 player with the lowest {header}:\n')
            f.write(smallest[['Player', 'Nation', 'Team', 'Position', header]].to_string(index = False))
            f.write('\n\n-------------------------------------------------------------------------\n\n')

def find_median_mean_and_standard_each_statistic(df):
    # get headers
    headers = df.columns[4:]

    # calculate the median, mean and std all players of league
    all_team = df[headers].agg(['median', 'mean', 'std']).T

    # transpose dataframe to one row
    new_columns = ['Team']    
    values = ['All']
    for col in all_team.index:
        for stat in ['median', 'mean', 'std']:
            new_columns.append(f'{stat} of {col}')
            values.append(all_team.loc[col, stat])
    all_team = pandas.DataFrame([values], columns=new_columns)

    # calculate the median, mean and std for each team
    mapped_headers = {}
    for header in headers:
        mapped_headers[header] = ['median', 'mean', 'std']
    cal_df = df.groupby('Team').agg(mapped_headers).reset_index()

    # rename the columns
    headers = cal_df.columns
    new_headers = []
    for x in headers:
        if x[0] == 'Team':
            new_headers.append(x[0])
        else:
            new_headers.append(x[1] + ' of ' + x[0])
    cal_df.columns = new_headers

    # merge the all_team dataframe with the cal_df dataframe
    cal_df = pandas.concat([all_team, cal_df], axis = 0)

    # round float values to 2 decimal places
    num_cols = cal_df.select_dtypes(include=['number']).columns
    cal_df[num_cols] = cal_df[num_cols].astype(float).round(2)

    # fill N/a values
    cal_df = cal_df.replace('', 'N/a').fillna('N/a').reset_index(drop = True)

    # write to csv file
    cal_df.to_csv('result2.csv', encoding = 'utf-8-sig')

def plot_histogram(df):
    # all players of league
    headers = df.columns[4:]    
    for header in headers:
        df_copy = df[header].dropna()
        plt.hist(df_copy, bins = 30, color = 'red', edgecolor = 'black')
        plt.title(f'Histogram of {header} Distribution')
        plt.xlabel('Value of ' + header)
        plt.ylabel('Frequency Players')
        plt.grid(axis = 'y', color = 'black', linestyle = '--', linewidth = 0.5)
        plt.show()  

    # players of each team
    for team, dfteam in df.groupby('Team'):
        for header in headers:
            df_copy = dfteam[header].dropna()
            plt.hist(df_copy, bins = 30, color = 'red', edgecolor = 'black')
            plt.title(f'Histogram of {header} Distribution for {team}')
            plt.xlabel('Value of ' + header)
            plt.ylabel('Frequency Players')
            plt.grid(axis = 'y', color = 'black', linestyle = '--', linewidth = 0.5)
            plt.show()

def identify_team_with_highest_score(df):
    # get the teams and headers
    teams = sorted(df['Team'].unique())
    headers = df.columns[4:]

    # read the csv file
    data = pandas.read_csv('result2.csv', index_col = False)
    data = data.drop(index = 0).reset_index(drop = True)

    # process the data to new dataframe
    new_df = pandas.DataFrame(teams, columns = ['Team'])
    for header in headers:
        new_df[header] = (data['mean of ' + header])
    
    # identify the team with the highest scores for each statistic.
    dict = {}
    for team in teams:
        dict[team] = 0
    for header in headers:
        idx = new_df[header].idxmax()
        dict[new_df['Team'][idx]] += 1
        print(f'{new_df["Team"][idx]} has the highest {header} score.')
    
    # find the team best team performing in the league
    best_team = max(dict, key = dict.get)
    print('-' * 70)
    print(f'-> {best_team} is performing the best in the 2024-2025 Premier League season.')

if __name__ == '__main__':
    # Read the CSV file into a DataFrame
    df = pandas.read_csv('result.csv')
    # Preprocess the DataFrame
    df['Age'] = df['Age'].apply(lambda x : float(f'{(int(x.split('-')[0]) + (int(x.split('-')[1]) / 365)):.2f}'))
    for headers in df.columns[4:]:
        df[headers] = pandas.to_numeric(df[headers], errors='coerce')

    identify_the_top_3_each_statistic(df)
    find_median_mean_and_standard_each_statistic(df)
    plot_histogram(df)
    identify_team_with_highest_score(df)
