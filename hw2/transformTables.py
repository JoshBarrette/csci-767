from enums import TableAFields, TableBFields
import numpy as np
import pandas as pd


def main():
    table_a = np.genfromtxt(
        "../hw1/tableA.csv",
        delimiter=",",
        dtype=str,
        skip_header=True,
    )
    table_a_rows = []
    for row in table_a:
        team = row[TableAFields.playerTeam]
        # If a player has been on more than 1 team then they will have multiple rows.
        # Need to filter out the "total" row that contains the sum of their stats from all teams.
        if team >= "2" and team[0] <= "9":
            continue

        games_played_float = float(row[TableAFields.gamesPlayed])
        table_a_rows.append(
            {
                "id": row[TableAFields.id],
                "statsYear": row[TableAFields.statsYear],
                "playerName": row[TableAFields.playerName],
                "gamesPlayed": row[TableAFields.gamesPlayed],
                "minutesPerGame": round(
                    float(row[TableAFields.minutesPlayed]) / games_played_float, 2
                ),
                "pointsPerGame": round(
                    float(row[TableAFields.points]) / games_played_float, 2
                ),
                "reboundsPerGame": round(
                    float(row[TableAFields.totalRebounds]) / games_played_float, 2
                ),
                "assistsPerGame": round(
                    float(row[TableAFields.assists]) / games_played_float, 2
                ),
                "blocksPerGame": round(
                    float(row[TableAFields.blocks]) / games_played_float, 2
                ),
                "stealsPerGame": round(
                    float(row[TableAFields.steals]) / games_played_float, 2
                ),
            }
        )
    data_frame_b = pd.DataFrame(table_a_rows)
    data_frame_b.to_csv("tableA.transformed.csv", index=False)

    table_b = np.genfromtxt(
        "../hw1/tableB.csv",
        delimiter=",",
        dtype=str,
        skip_header=True,
    )
    table_b_rows = []
    for row in table_b:
        table_b_rows.append(
            {
                "id": row[TableBFields.id],
                "statsYear": row[TableBFields.statsYear],
                "playerName": row[TableBFields.playerName],
                "gamesPlayed": row[TableBFields.gamesPlayed],
                "minutesPerGame": row[TableBFields.minutesPerGame],
                "pointsPerGame": row[TableBFields.pointsPerGame],
                "reboundsPerGame": row[TableBFields.reboundsPerGame],
                "assistsPerGame": row[TableBFields.assistsPerGame],
                "blocksPerGame": row[TableBFields.blocksPerGame],
                "stealsPerGame": row[TableBFields.stealsPerGame],
            }
        )
    data_frame_b = pd.DataFrame(table_b_rows)
    data_frame_b.to_csv("tableB.transformed.csv", index=False)


if __name__ == "__main__":
    main()
