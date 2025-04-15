import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

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

# elbow method
means = []
itertias = []
for k in range(2, 75):
    kmeans = KMeans(n_clusters = k, random_state = 0)
    kmeans.fit(df[headers_scaled])
    means.append(k)
    itertias.append(kmeans.inertia_)

# silhouette method
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

axs[1].plot(means, sil_score, 'o-')
axs[1].set_xlabel('Number of clusters')
axs[1].set_ylabel('Silhouette Score')
axs[1].set_title('Silhouette Method')

plt.grid(True)
plt.tight_layout()
plt.show() 

# based on plot I see the best k in range(6, 11)
# Use the K-means algorithm to classify players into groups based on their statistics. 
for k in range(6, 10):
    kmeans = KMeans(n_clusters = k, random_state = 0)
    kmeans.fit(df[headers_scaled])

    # use PCA 
    pca = PCA(n_components = 2)
    X_pca = pca.fit_transform(df[headers_scaled])

    plt.figure(figsize = (8, 6))
    plt.scatter(x = X_pca[:, 0], y = X_pca[:, 1], c = kmeans.labels_)
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.title(f'KMeans with k = {k}')
    plt.colorbar(label='Target')
    plt.show()
