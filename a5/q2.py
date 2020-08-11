import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    train = pd.read_csv("training.csv")
    test = pd.read_csv("testing.csv")
    data = train[["GLCM_pan", "Mean_Green", "Mean_Red", "Mean_NIR", "SD_pan"]].values

    sse = {}
    for k in [2, 5, 10, 20]:
        kmeans = KMeans(n_clusters=k, max_iter=100,n_init=10).fit(data)
        sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
    print(data)
    plt.figure()
    plt.plot(list(sse.keys()), list(sse.values()))
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    plt.show()

if __name__ == "__main__":
    main()