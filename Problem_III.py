import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# read dateframe from csv file
df = pd.read_csv('result.csv')

# preprocess the data
df['Age'] = df['Age'].apply(lambda x : float(f'{(int(x.split('-')[0]) + (int(x.split('-')[1]) / 365)):.2f}'))
df = df.replace('N/a', 0)
headers = df.columns[4:]
headers_scaled = [x + '_scaled' for x in headers]
scaler = StandardScaler()
df[headers_scaled] = scaler.fit_transform(df[headers])

# find the best k value for KMeans
means = []
itertias = []
for k in range(2, 75):
    kmeans = KMeans(n_clusters = k, random_state = 0)
    kmeans.fit(df[headers_scaled])
    means.append(k)
    itertias.append(kmeans.inertia_)

sil_score = []
for k in range(2, 75):
    kmeans = KMeans(n_clusters=k, random_state = 0)
    labels = kmeans.fit_predict(df[headers_scaled])
    score = silhouette_score(df[headers_scaled], labels)
    sil_score.append(score)

# plot
fig, axs = plt.subplots(1, 2, figsize=(14, 5))

axs[0].plot(means, itertias, 'o-')
axs[0].set_xlabel('Number of clusters')
axs[0].set_ylabel('Inertia')
axs[0].set_title('Elbow Method')
axs[0].axvline(x = 8, color = 'r', linestyle = '--')

axs[1].plot(means, sil_score, 'o-')
axs[1].set_xlabel('Number of clusters')
axs[1].set_ylabel('Silhouette Score')
axs[1].set_title('Silhouette Method')
axs[1].axvline(x = 8, color = 'r', linestyle = '--')

plt.grid(True)
plt.tight_layout()
plt.show() 

# based on plot I see the best k = 8
kmeans = KMeans(n_clusters = 8, random_state = 0)
kmeans.fit(df[headers_scaled])
df['Labels of Players'] = kmeans.labels_

print(df[['Player', 'Labels of Players']])