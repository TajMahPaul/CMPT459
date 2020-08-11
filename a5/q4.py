import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

  

def get_min_distance_to_closest_center(row, centers):
    distances = []
    x1 = np.array([row.GLCM_pan, row.Mean_Green, row.Mean_Red, row.Mean_NIR, row.SD_pan])
    for center in centers:
        distances.append(np.linalg.norm(x1-center))
    return np.square(min(distances))

def main():
    train = pd.read_csv("training.csv")
    test = pd.read_csv("testing.csv")
    data = train[["GLCM_pan", "Mean_Green", "Mean_Red", "Mean_NIR", "SD_pan"]].values
    sums = []
    for k in range(10,30):
        kmeans = KMeans(n_clusters=k, max_iter=100, n_init=10).fit(data)
        test['squared_distance'] = test.apply(lambda x: get_min_distance_to_closest_center(x, kmeans.cluster_centers_), axis=1)
        sums.append(np.sum(test['squared_distance']))
        

    plt.figure()
    plt.plot(range(10, 30), sums)
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    plt.show()

if __name__ == "__main__":
    main()