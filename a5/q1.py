import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    train = pd.read_csv("training.csv")
    test = pd.read_csv("testing.csv")
    data = train[["GLCM_pan", "Mean_Green", "Mean_Red", "Mean_NIR", "SD_pan"]].values

    sse = {}
    kmeans = KMeans(n_clusters=10, max_iter=100,n_init=1).fit(data)
    x = range(kmeans.n_iter_)
    y = kmeans.inertia_iteration
    plt.figure()
    plt.plot(x, y)
    plt.xlabel("Iteration")
    plt.ylabel("SSE")
    plt.show()

if __name__ == "__main__":
    main()