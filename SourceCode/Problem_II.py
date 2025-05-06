import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from tabulate import tabulate

class FootballStatsAnalyzer:
    def __init__(self, input_file='SourceCode\\result.csv'):
        self.input_file = input_file
        self.df = pd.read_csv(self.input_file)

        # preprocess the DataFrame
        self.df['Age'] = self.df['Age'].apply(lambda x : float(f'{(int(x.split("-")[0]) + (int(x.split("-")[1]) / 365)):.2f}'))
        for headers in self.df.columns[4:]:
            self.df[headers] = pd.to_numeric(self.df[headers], errors='coerce')

    # identify the top 3 players with the highest and lowest scores for each statistic.
    def identify_the_top_3_each_statistic(self):
        # write the top 3 players with the highest and lowest scores for each statistic to a text file
        with open('SourceCode\\top_3.txt', 'w') as f:
            pass
        for header in self.df.columns[4:]:
            DF = self.df.copy()
            DF[header] = pd.to_numeric(DF[header], errors='coerce')
            DF = DF.dropna(subset=[header])
            largest = DF.nlargest(3, header)
            smallest = DF.nsmallest(3, header)
            with open('SourceCode\\top_3.txt', 'a', encoding='utf-8-sig') as f:
                f.write(f'Top 3 player with the highest {header}:\n')
                f.write(tabulate(largest[['Player', 'Nation', 'Team', 'Position', header]], headers='keys', tablefmt='grid', showindex=False))
                f.write('\n\n')
                f.write(f'Top 3 player with the lowest {header}:\n')
                f.write(tabulate(smallest[['Player', 'Nation', 'Team', 'Position', header]], headers='keys', tablefmt='grid', showindex=False))
                f.write('\n\n-------------------------------------------------------------------------\n\n')

    def find_median_mean_and_standard_each_statistic(self):
        # get headers
        headers = self.df.columns[4:]

        # calculate the median, mean and std all players of league
        all_team = self.df[headers].agg(['median', 'mean', 'std']).T

        # transpose dataframe to one row
        new_columns = ['Team']
        values = ['All']
        for col in all_team.index:
            for stat in ['median', 'mean', 'std']:
                new_columns.append(f'{stat} of {col}')
                values.append(all_team.loc[col, stat])
        all_team = pd.DataFrame([values], columns=new_columns)

        # calculate the median, mean and std for each team
        mapped_headers = {}
        for header in headers:
            mapped_headers[header] = ['median', 'mean', 'std']
        cal_df = self.df.groupby('Team').agg(mapped_headers).reset_index()

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
        cal_df = pd.concat([all_team, cal_df], axis=0)

        # round float values to 2 decimal places
        num_cols = cal_df.select_dtypes(include=['number']).columns
        cal_df[num_cols] = cal_df[num_cols].astype(float).round(2)

        # fill N/a values
        cal_df = cal_df.replace('', 'N/a').fillna('N/a').reset_index(drop=True)

        # write to csv file
        cal_df.to_csv('SourceCode\\result2.csv', encoding='utf-8-sig')

    def plot_histogram(self, filename='SourceCode\\histograms.pdf'):
        headers = ['Goals', 'Assists', 'G/sh', 'Tkl', 'Att', 'Blocks']

        with PdfPages(filename) as pdf:
            # all players in league
            for header in headers:
                df_copy = self.df[header].dropna()
                plt.figure()
                plt.hist(df_copy, bins=25, color='red', edgecolor='black')
                plt.title(f'Histogram of {header} Distribution for All')
                plt.xlabel('Value of ' + header)
                plt.ylabel('Frequency Players')
                plt.grid(axis='y', color='black', linestyle='--', linewidth=0.5)
                pdf.savefig()
                plt.close()

            # each team
            for team, dfteam in self.df.groupby('Team'):
                for header in headers:
                    df_copy = dfteam[header].dropna()
                    if not df_copy.empty:
                        plt.figure()
                        plt.hist(df_copy, bins=20, color='red', edgecolor='black')
                        plt.title(f'Histogram of {header} Distribution for {team}')
                        plt.xlabel('Value of ' + header)
                        plt.ylabel('Frequency Players')
                        plt.grid(axis='y', color='black', linestyle='--', linewidth=0.5)
                        pdf.savefig()
                        plt.close()

    def identify_team_with_highest_score(self):
        # get the teams and headers
        teams = sorted(self.df['Team'].unique())
        headers = self.df.columns[4:]

        # read the csv file
        data = pd.read_csv('SourceCode\\result2.csv', index_col=False)
        data = data.drop(index=0).reset_index(drop=True)

        # process the data to new dataframe
        new_df = pd.DataFrame(teams, columns=['Team'])
        for header in headers:
            new_df[header] = (data['mean of ' + header])

        # identify the team with the highest scores for each statistic.
        team_scores = {team: 0 for team in teams}
        for header in headers:
            idx = new_df[header].idxmax()
            team_scores[new_df['Team'][idx]] += 1
            print(f'{new_df["Team"][idx]} has the highest {header} score.')

        # find the team best team performing in the league
        best_team = max(team_scores, key=team_scores.get)
        print('-' * 70)
        print(f'-> {best_team} is performing the best in the 2024-2025 Premier League season.')

    def run(self):
        self.identify_the_top_3_each_statistic()
        self.find_median_mean_and_standard_each_statistic()
        self.plot_histogram()
        self.identify_team_with_highest_score()

if __name__ == '__main__':
    analyzer = FootballStatsAnalyzer()
    analyzer.run()