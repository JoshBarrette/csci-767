import numpy as np
import pandas as pd
from rapidfuzz import fuzz
from enums import FieldsIndex, FieldsTolerance


def matchYear(tableAYear: str, tableBYear: str):
    return tableAYear == tableBYear


def matchName(tableAName: str, tableBName: str):
    return fuzz.ratio(tableAName, tableBName) > FieldsTolerance.playerName


def matchNumericalStats(tableAStats: list[float], tableBStats: list[float]):
    tolerances = [
        FieldsTolerance.gamesPlayed,
        FieldsTolerance.minutesPerGame,
        FieldsTolerance.pointsPerGame,
        FieldsTolerance.reboundsPerGame,
        FieldsTolerance.assistsPerGame,
        FieldsTolerance.blocksPerGame,
        FieldsTolerance.stealsPerGame,
    ]
    for i in range(len(tolerances)):
        if abs(tableAStats[i] - tableBStats[i]) > tolerances[i]:
            return False
    return True


def main():
    tableA = np.genfromtxt(
        "./tableA.transformed.csv",
        delimiter=",",
        dtype=str,
        skip_header=True,
    )
    tableALength = len(tableA)
    tableAYears: list[str] = tableA[:, FieldsIndex.statsYear]
    tableANames: list[str] = tableA[:, FieldsIndex.playerName]
    tableANumericalFields: list[list[float]] = tableA[
        :, FieldsIndex.gamesPlayed : FieldsIndex.stealsPerGame + 1
    ].astype(float)
    tableASet = set()
    for row in tableA:
        tableASet.add(",".join(list(row)))
    print(f"Table A has {len(tableASet)} unique rows")

    tableB = np.genfromtxt(
        "./tableB.transformed.csv",
        delimiter=",",
        dtype=str,
        skip_header=True,
    )
    tableBLength = len(tableB)
    tableBYears: list[str] = tableB[:, FieldsIndex.statsYear]
    tableBNames: list[str] = tableB[:, FieldsIndex.playerName]
    tableBNumericalFields: list[list[float]] = tableB[
        :, FieldsIndex.gamesPlayed : FieldsIndex.stealsPerGame + 1
    ].astype(float)
    tableBSet = set()
    for row in tableB:
        tableBSet.add(",".join(list(row)))
    print(f"Table B has {len(tableBSet)} unique rows")

    currentId = 1
    matches = []
    tableCSet = set()
    for tableAIndex in range(tableALength):
        for tableBIndex in range(tableBLength):
            tableCSet.add(
                f"{",".join(list(tableA[tableAIndex]))},{",".join(list(tableB[tableBIndex]))}"
            )
            if (
                matchYear(tableAYears[tableAIndex], tableBYears[tableBIndex])
                and matchName(tableANames[tableAIndex], tableBNames[tableBIndex])
                and matchNumericalStats(
                    tableANumericalFields[tableAIndex],
                    tableBNumericalFields[tableBIndex],
                )
            ):
                matches.append(
                    {
                        "id": currentId,
                        "ltable_id": tableA[tableAIndex][FieldsIndex.id],
                        "rtable_id": tableB[tableBIndex][FieldsIndex.id],
                        "ltable_playerName": tableA[tableAIndex][
                            FieldsIndex.playerName
                        ],
                        "rtable_playerName": tableB[tableBIndex][
                            FieldsIndex.playerName
                        ],
                        "ltable_pointsPerGame": tableA[tableAIndex][
                            FieldsIndex.pointsPerGame
                        ],
                        "rtable_pointsPerGame": tableB[tableBIndex][
                            FieldsIndex.pointsPerGame
                        ],
                    }
                )
                currentId = currentId + 1

    frame = pd.DataFrame(matches)
    frame.to_csv("tableC.csv", index=False)
    print(f"Table C has {len(tableCSet)} unique rows")


if __name__ == "__main__":
    main()
