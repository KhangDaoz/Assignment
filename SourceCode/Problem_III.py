import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

class KMeansPlayerClustering:
    def __init__(self):
        # read dateframe from csv file
        self.df = pd.read_csv('SourceCode\\result.csv')

        # preprocess the data
        self.df['Age'] = self.df['Age'].apply(lambda x : float(f'{(int(x.split("-")[0]) + (int(x.split("-")[1]) / 365)):.2f}'))
        self.df = self.df.replace('N/a', 0)
        self.headers = self.df.columns[4:]
        self.headers_scaled = [x + '_scaled' for x in self.headers]
        scaler = StandardScaler()
        self.df[self.headers_scaled] = scaler.fit_transform(self.df[self.headers])

    def evaluate_k(self, k_range=range(2, 75)):
        # find the best k value for KMeans

        # elbow method
        means = []
        itertias = []
        for k in k_range:
            kmeans = KMeans(n_clusters = k, random_state = 0)
            kmeans.fit(self.df[self.headers_scaled])
            means.append(k)
            itertias.append(kmeans.inertia_)

        # silhouette method
        sil_score = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state = 0)
            labels = kmeans.fit_predict(self.df[self.headers_scaled])
            score = silhouette_score(self.df[self.headers_scaled], labels)
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

        return range(6, 10)

    def run_kmeans_and_plot(self):
        # based on plot I see the best k in range(6, 10)
        k_values = self.evaluate_k()
        
        # prepare the figure
        num_k = len(k_values)
        fig, axs = plt.subplots(1, num_k, figsize=(6 * num_k, 6)) 

        for idx, k in enumerate(k_values):
            kmeans = KMeans(n_clusters=k, random_state=0)
            kmeans.fit(self.df[self.headers_scaled])

            # PCA for 2D projection
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(self.df[self.headers_scaled])

            scatter = axs[idx].scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis')
            axs[idx].set_title(f'KMeans with k = {k}')
            axs[idx].set_xlabel('PC 1')
            axs[idx].set_ylabel('PC 2')

        plt.tight_layout()
        plt.show()
        
        k = 9
        kmeans = KMeans(n_clusters = k, random_state = 0)
        kmeans.fit(self.df[self.headers_scaled])

        # use PCA 
        pca = PCA(n_components = 2)
        X_pca = pca.fit_transform(self.df[self.headers_scaled])

        plt.figure(figsize = (8, 6))
        plt.scatter(x = X_pca[:, 0], y = X_pca[:, 1], c = kmeans.labels_)
        plt.xlabel('PC 1')
        plt.ylabel('PC 2')
        plt.title(f'KMeans with k = {k}')
        plt.colorbar(label='Target')
        plt.show()

if __name__ == '__main__':
    clustering = KMeansPlayerClustering()
    clustering.run_kmeans_and_plot()