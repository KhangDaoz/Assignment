import pandas 

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

    # calculate the median, mean and std all 
    all_team = df[headers].agg(['median', 'mean', 'std']).T

    # transpose dataframe to one row
    new_columns = []    
    values = []
    for col in all_team.index:
        for stat in ['median', 'mean', 'std']:
            new_columns.append(f'{stat} of {col}')
            values.append(all_team.loc[col, stat])
    all_team = pandas.DataFrame([values], columns=new_columns)
    all_team.index = ['All']

    # calculate the median, mean and std for each team
    mapped_headers = {}
    for header in headers:
        mapped_headers[header] = ['median', 'mean', 'std']
    cal_df = df.groupby('Team').agg(mapped_headers)

    # rename the columns
    headers = cal_df.columns
    new_headers = []
    for x in headers:
        new_headers.append(x[1] + ' of ' + x[0])
    cal_df.columns = new_headers

    # merge the all_team dataframe with the cal_df dataframe
    cal_df = pandas.concat([all_team, cal_df], axis = 0)

    # round float values to 2 decimal places
    cal_df = cal_df.astype(float).round(2)

    # write to csv file
    cal_df.to_csv('result2.csv', encoding = 'utf-8-sig')

if __name__ == '__main__':
    # Read the CSV file into a DataFrame
    df = pandas.read_csv('result.csv')
    # Preprocess the DataFrame
    df['Age'] = df['Age'].apply(lambda x : float(f'{(int(x.split('-')[0]) + (int(x.split('-')[1]) / 365)):.2f}'))
    for headers in df.columns[4:]:
        df[headers] = pandas.to_numeric(df[headers], errors='coerce')

    identify_the_top_3_each_statistic(df)
    find_median_mean_and_standard_each_statistic(df)

