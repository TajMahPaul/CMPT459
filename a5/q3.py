import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    train = pd.read_csv("training.csv")
    test = pd.read_csv("testing.csv")
    data = train[["GLCM_pan", "Mean_Green", "Mean_Red", "Mean_NIR", "SD_pan"]].values

    average_purities = []
    for k in [10, 20, 30, 50]:
        new_df = train.copy()
        kmeans = KMeans(n_clusters=k, max_iter=100, n_init=10).fit(data)
        new_df['cluster_label'] = kmeans.labels_
        new_df = new_df.groupby(['cluster_label', 'class'])['GLCM_pan'].count().reset_index(name='counts')
        new_df = new_df.pivot(index='cluster_label', columns='class', values='counts').fillna(0)
        new_df['total'] = new_df['n'] + new_df['w']
        new_df['max'] = new_df[["n", "w"]].max(axis=1)
        new_df['purity'] = new_df["max"] / new_df['total']
        print(new_df)
        average_purities.append(np.average(new_df['purity']))

    plt.figure()
    plt.plot([10, 20, 30, 50], average_purities)
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    plt.show()

if __name__ == "__main__":
    main()