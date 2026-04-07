import numpy as np
import random
import copy
import math
from typing import Callable


class FieldIndex:
    State = 0
    Murder = 1
    Assault = 2
    UrbanPop = 3
    Rape = 4


class HierarchicalDistances:
    def getMinDistance(cluster1: list[list], cluster2: list[list]) -> float:
        minDistance = float("inf")

        for node1 in cluster1:
            for node2 in cluster2:
                currentDistance = getEuclideanDistance(node1, node2)
                if currentDistance < minDistance:
                    minDistance = currentDistance
        return minDistance

    def getMaxDistance(cluster1: list[list], cluster2: list[list]) -> float:
        maxDistance = 0.0

        for node1 in cluster1:
            for node2 in cluster2:
                currentDistance = getEuclideanDistance(node1, node2)
                if currentDistance > maxDistance:
                    maxDistance = currentDistance
        return maxDistance

    def getMeanDistance(cluster1: list[list], cluster2: list[list]) -> float:
        distances = []

        for node1 in cluster1:
            for node2 in cluster2:
                distances.append(getEuclideanDistance(node1, node2))
        return float(np.mean(distances))


def getData() -> list[list]:
    rawData = np.genfromtxt(
        "./USArrests-1.csv",
        delimiter=",",
        dtype=str,
        skip_header=True,
    )

    data = []
    for row in rawData:
        data.append(
            [
                str(row[FieldIndex.State]),
                float(row[FieldIndex.Murder]),
                float(row[FieldIndex.Assault]),
                float(row[FieldIndex.UrbanPop]),
                float(row[FieldIndex.Rape]),
            ]
        )

    return data


def scaleData(data: list[list]):
    murder = {}
    assault = {}
    urbanPop = {}
    rape = {}

    for index, dict in [
        (FieldIndex.Murder, murder),
        (FieldIndex.Assault, assault),
        (FieldIndex.UrbanPop, urbanPop),
        (FieldIndex.Rape, rape),
    ]:
        fieldList = list(map(lambda row: row[index], data))
        dict["mean"] = np.mean(fieldList)
        dict["std"] = np.std(fieldList)

    for row in data:
        row[FieldIndex.Murder] = float(
            (row[FieldIndex.Murder] - murder["mean"]) / murder["std"]
        )
        row[FieldIndex.Assault] = float(
            (row[FieldIndex.Assault] - assault["mean"]) / assault["std"]
        )
        row[FieldIndex.UrbanPop] = float(
            (row[FieldIndex.UrbanPop] - urbanPop["mean"]) / urbanPop["std"]
        )
        row[FieldIndex.Rape] = float(
            (row[FieldIndex.Rape] - rape["mean"]) / rape["std"]
        )

    return


def getEuclideanDistance(row1: list, row2: list) -> float:
    return math.sqrt(
        pow(row1[FieldIndex.Murder] - row2[FieldIndex.Murder], 2)
        + pow(row1[FieldIndex.Assault] - row2[FieldIndex.Assault], 2)
        + pow(row1[FieldIndex.UrbanPop] - row2[FieldIndex.UrbanPop], 2)
        + pow(row1[FieldIndex.Rape] - row2[FieldIndex.Rape], 2)
    )


def getClusterMean(cluster: list[list]) -> list:
    return [
        "ClusterMean",
        float(
            np.mean(list(map(lambda stateRow: stateRow[FieldIndex.Murder], cluster)))
        ),
        float(
            np.mean(list(map(lambda stateRow: stateRow[FieldIndex.Assault], cluster)))
        ),
        float(
            np.mean(list(map(lambda stateRow: stateRow[FieldIndex.UrbanPop], cluster)))
        ),
        float(np.mean(list(map(lambda stateRow: stateRow[FieldIndex.Rape], cluster)))),
    ]


def kMeans(data: list[list], k: int = 4, maxIterations: int = 100):
    centroids = copy.deepcopy(random.sample(data, k))
    for centroid in centroids:
        centroid[FieldIndex.State] = "ClusterMean"
    clusters = []

    for i in range(maxIterations):
        clusters = [[] for _ in range(k)]

        for stateRow in data:
            distances = [
                getEuclideanDistance(stateRow, centroid) for centroid in centroids
            ]

            clusters[distances.index(min(distances))].append(stateRow)

        newCentroids = []
        for cluster in clusters:
            newCentroids.append(getClusterMean(cluster))

        if sorted(newCentroids) == sorted(centroids):
            print(f"Convergence reached on iteration {i + 1}, breaking out of loop...")
            break

        centroids = newCentroids

    print("K Means Completed")
    return centroids, clusters


def hierarchicalClustering(
    data: list[list],
    distanceMethod: Callable[[list[list], list[list]], float],
    desiredClusters: int = 4,
):
    clusters = [[stateRow] for stateRow in data]

    while len(clusters) > desiredClusters:
        minDistance = float("inf")
        minPair = 0, 0

        for left in range(len(clusters) - 1):
            for right in range(left + 1, len(clusters)):
                currentDistance = distanceMethod(clusters[left], clusters[right])
                if currentDistance < minDistance:
                    minDistance = currentDistance
                    minPair = left, right

        leftIndex, rightIndex = minPair
        newCluster = clusters[leftIndex] + clusters[rightIndex]

        clusters.pop(rightIndex)
        clusters.pop(leftIndex)
        clusters.append(newCluster)

    print("Hierarchical Clustering Completed")
    return clusters


def main():
    data = getData()
    scaleData(data)

    centroids, clusters = kMeans(data)
    print("K Means")
    print(f"Centroids:\n{centroids}")
    print(f"Clusters:\n{clusters}")

    print("\nHierarchical Clustering")
    print("Min distance clustering")
    print(hierarchicalClustering(data, HierarchicalDistances.getMinDistance))

    print("\nMax distance clustering")
    print(hierarchicalClustering(data, HierarchicalDistances.getMaxDistance))

    print("\nMean distance clustering")
    print(hierarchicalClustering(data, HierarchicalDistances.getMeanDistance))


if __name__ == "__main__":
    main()
