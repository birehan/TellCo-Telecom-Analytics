from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

def get_distortions_and_inertias(df: pd.DataFrame, num: int):
    distortions = []
    inertias = []
    K = range(1, num)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=0).fit(df)
        distortions.append(sum(
            np.min(cdist(df, kmeans.cluster_centers_, 'euclidean'), axis=1)) / df.shape[0])
        inertias.append(kmeans.inertia_)

    return (distortions, inertias)
