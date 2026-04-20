import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

trainingData = [
    np.array([int(value) for value in row.split(" ")[:-1]])
    for row in open("./face_train_data_960.txt").read().split("\n")
]
trainingLabels = [
    int(row.split(" ")[-1])
    for row in open("./face_train_data_960.txt").read().split("\n")
]


testingData = [
    np.array([int(value) for value in row.split(" ")[:-1]])
    for row in open("./face_test_data_960.txt").read().split("\n")
]
testingLabels = [
    int(row.split(" ")[-1])
    for row in open("./face_test_data_960.txt").read().split("\n")
]


dummyData = [
    np.array([int(value) for value in row.split(" ")[:-1]])
    for row in open("./x.txt").read().split("\n")
]


def centerData(data: list[list[int]]):
    centeredData: list[list[float]] = []
    for row in data:
        newRow: list[float] = []
        rowMean = float(np.mean(row))

        for i in range(len(row)):
            newRow.append(row[i] - rowMean)
        centeredData.append(newRow)
    return centeredData


def myPCA(data: list[list[int]]):
    variableCount = len(data[0])
    centeredData = centerData(data)

    covarianceMatrix: list[list[float]] = []
    for leftIdx in range(variableCount):
        newCovarianceRow: list[float] = []
        for rightIdx in range(variableCount):
            newSum = 0.0
            for i in range(len(centeredData)):
                newSum = newSum + (centeredData[i][leftIdx] * centeredData[i][rightIdx])
            newCovarianceRow.append(newSum / (variableCount - 1))
        covarianceMatrix.append(newCovarianceRow)

    eigenResult = np.linalg.eig(covarianceMatrix)
    combinedEigenResult = []
    for i in range(len(eigenResult.eigenvectors)):
        combinedEigenResult.append(
            [
                float(eigenResult.eigenvalues[i]),
                [float(x) for x in eigenResult.eigenvectors[i]],
            ]
        )
    combinedEigenResult.sort(key=lambda pair: pair[0], reverse=True)

    return (
        np.array([row[0] for row in combinedEigenResult]),  # values
        np.array([np.array(row[1]) for row in combinedEigenResult]),  # vectors
    )


def eigenfaces(data: list[list[int]]):
    latent, coeff = myPCA(data)
    fig, ax = plt.subplots(1, 5)

    for i in range(5):
        eigenface = coeff[:, i].reshape(30, 32)
        ax[i].imshow(eigenface, cmap="gray")
        ax[i].axis("off")
    plt.show()


def proportionOfVariance(data: list[list[int]]):
    latent, coeff = myPCA(data)
    overallTotal = np.sum(latent)
    cumulativeFunction: list[tuple[float, float]] = []

    foundK = -1
    runningTotal = 0
    for i in range(len(latent)):
        runningTotal = runningTotal + latent[i]
        currentVariance = (runningTotal / overallTotal) * 100
        cumulativeFunction.append((i, currentVariance))
        if currentVariance >= 90 and foundK == -1:
            foundK = i

    plt.scatter(
        [item[0] for item in cumulativeFunction],
        [item[1] for item in cumulativeFunction],
    )
    plt.axvline(x=foundK, color="red")
    plt.axhline(y=90, color="red")
    plt.title(f"90% variance reached at K = {foundK + 1}")
    plt.show()


def partD(data: list[list[int]]):
    latent, coeff = myPCA(data)

    for k in [1, 3, 5, 7]:
        projectedTrainingData = centerData(trainingData) @ coeff[:, :24]
        projectedTestingData = centerData(testingData) @ coeff[:, :24]

        knn = KNeighborsClassifier(k)
        knn.fit(projectedTrainingData, trainingLabels)
        y_pred = knn.predict(projectedTestingData)
        accuracy = np.mean(y_pred == testingLabels)
        print(f"K:{k} accuracy is {accuracy}")


def partE(data: list[list[int]]):
    latent, coeff = myPCA(data)

    for k in [50, 100]:
        projectedTrainingData = centerData(trainingData) @ coeff[:, :k]
        reconstructedTrainingData = projectedTrainingData @ np.transpose(coeff[:, :k])
        fullyReconstructedTrainingData = reconstructedTrainingData + np.mean(
            trainingData
        )

        fig, ax = plt.subplots(1, 5)
        fig.suptitle(f"Reconstructed images for k: {k}")
        for i in range(5):
            eigenface = fullyReconstructedTrainingData[i].reshape(30, 32)
            ax[i].imshow(eigenface, cmap="gray")
            ax[i].axis("off")
        plt.show()


def main():
    eigenfaces(trainingData)
    proportionOfVariance(trainingData)
    partD(trainingData)
    partE(trainingData)


if __name__ == "__main__":
    main()
