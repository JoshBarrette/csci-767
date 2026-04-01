import numpy as np
import pandas as pd
import time


def findMaxAndMin():
    maxUser = 0
    maxMovie = 0
    minMovieRating = 1000

    rawTrainingData = np.genfromtxt(
        "./ratings_small_training-1.csv",
        delimiter=",",
        dtype=float,
        skip_header=True,
    )

    for row in rawTrainingData:
        if row[0] > maxUser:
            maxUser = row[0]
        if row[1] > maxMovie:
            maxMovie = row[1]
        if row[2] < minMovieRating:
            minMovieRating = row[2]

    print(f"User: {maxUser}")  # 671
    print(f"Movie: {maxMovie}")  # 163949
    print(f"Min movie rating: {minMovieRating}")  # 0.5


def getSignificanceWeight(
    user1Ratings: list[float], user2Ratings: list[float]
) -> int | float:
    coRatedItemsCount = 0
    for i in range(len(user1Ratings)):
        if user1Ratings[i] == 0.0 and user2Ratings[i] == 0.0:
            coRatedItemsCount = coRatedItemsCount + 1

    if coRatedItemsCount > 50:
        return 1
    else:
        return coRatedItemsCount / 50


def getCovariance(user1Ratings: list[float], user2Ratings: list[float]) -> float:
    user1RatingsMean = np.mean([rating for rating in user1Ratings if rating != 0])
    user2RatingsMean = np.mean([rating for rating in user2Ratings if rating != 0])
    totalRatings = len(user1Ratings)

    currentSum = 0
    for i in range(totalRatings):
        currentSum = currentSum + (
            (user1Ratings[i] - user1RatingsMean) * (user2Ratings[i] - user2RatingsMean)
        )

    return currentSum / totalRatings


def getPearsonCorrelationCoefficient(
    user1Ratings: list[float], user2Ratings: list[float]
) -> float:
    numerator = getCovariance(user1Ratings, user2Ratings)
    denominator = np.std(user1Ratings) * np.std(user2Ratings)

    return numerator / denominator


def getWeighting(user1Ratings: list[float], user2Ratings: list[float]) -> float:
    return getPearsonCorrelationCoefficient(
        user1Ratings, user2Ratings
    ) * getSignificanceWeight(user1Ratings, user2Ratings)


def getRatingPrediction(
    activeUserRatings: list[float],
    neighbors: list[tuple[float, list[float]]],
    movieId: int,
) -> float:
    activeUserAverage = np.mean([rating for rating in activeUserRatings if rating != 0])

    numerator = 0
    denominator = 0
    for neighbor in neighbors:
        neighborAverageRating = np.mean(
            [rating for rating in neighbor[1] if rating != 0]
        )
        neighborRatingOfMovie = neighbor[1][movieId]

        numerator = numerator + (
            neighbor[0] * (neighborRatingOfMovie - neighborAverageRating)
        )
        denominator = denominator + neighbor[0]

    return activeUserAverage + (numerator / denominator)


def main():
    totalUsers = 671
    totalMovies = 163949

    baseMatrix = np.zeros(totalUsers, dtype=np.ndarray)
    for index in range(len(baseMatrix)):
        baseMatrix[index] = np.zeros(totalMovies, dtype=np.float32)

    rawTrainingData = np.genfromtxt(
        "./ratings_small_training-1.csv",
        delimiter=",",
        dtype=float,
        skip_header=True,
    )
    for row in rawTrainingData:
        userIndex = int(row[0]) - 1
        movieId = int(row[1]) - 1
        movieRating = row[2]

        baseMatrix[userIndex][movieId] = movieRating

    testData = np.genfromtxt(
        "./ratings_small_test-1.csv",
        delimiter=",",
        dtype=int,
        skip_header=True,
    )

    newRows = []
    for row in testData:
        userIndex = row[0] - 1
        movieId = row[1] - 1

        start = time.time()
        userWeights = []
        for i in range(len(baseMatrix)):

            if i == userIndex:
                continue

            if baseMatrix[i][movieId] != 0:

                userWeights.append(
                    [getWeighting(baseMatrix[userIndex], baseMatrix[i]), baseMatrix[i]]
                )

        neighbors = sorted(userWeights, key=lambda tup: tup[0], reverse=True)[:20]
        ratingPrediction = getRatingPrediction(
            baseMatrix[userIndex], neighbors, movieId
        )

        print(
            f"Finished user {userIndex + 1} in {int(time.time() - start)} seconds with a prediction of {ratingPrediction}"
        )
        newRows.append(
            {
                "user_id": userIndex + 1,
                "movie_id": movieId + 1,
                "predicted_rating": ratingPrediction,
            }
        )

    dataFrame = pd.DataFrame(newRows)
    dataFrame.to_csv("ratings_small_test.transformed.csv", index=False)


if __name__ == "__main__":
    main()
    # findMaxAndMin()
