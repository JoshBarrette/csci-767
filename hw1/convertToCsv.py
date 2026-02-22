from bs4 import BeautifulSoup
import pandas as pd

years = [2024, 2025, 2026]


def reference():
    currentId = 1
    outputRows = []
    for year in years:
        file = open(f"./reference.{year}.out.html").read()
        soup = BeautifulSoup(file, "html.parser")

        for i in range(9999):
            row = soup.find("tr", attrs={"data-row": f"{i}"})
            if not row:
                break

            cells = row.find_all("td")
            # Account for junk rows
            if len(cells) == 0 or cells[0].get_text() == "League Average":
                continue

            ID = currentId
            currentId = currentId + 1
            playerName = cells[0].get_text()
            playerAge = cells[1].get_text()
            playerTeam = cells[2].get_text()
            statsYear = year
            position = cells[3].get_text()
            gamesPlayed = cells[4].get_text()
            gamesStarted = cells[5].get_text()
            minutesPlayed = cells[6].get_text()
            fieldGoals = cells[7].get_text()
            fieldGoalAttempts = cells[8].get_text()
            fieldGoalPercent = cells[9].get_text()
            threePointersMade = cells[10].get_text()
            threePointAttempts = cells[11].get_text()
            threePointPercent = cells[12].get_text()
            twoPointersMade = cells[13].get_text()
            towPointAttempts = cells[14].get_text()
            twoPointPercent = cells[15].get_text()
            effectiveFieldGoalPercentage = cells[16].get_text()
            freeThrowsMade = cells[17].get_text()
            freeThrowAttempts = cells[18].get_text()
            freeThrowPercent = cells[19].get_text()
            offensiveRebounds = cells[20].get_text()
            defensiveRebounds = cells[21].get_text()
            totalRebounds = cells[22].get_text()
            assists = cells[23].get_text()
            steals = cells[24].get_text()
            blocks = cells[25].get_text()
            turnovers = cells[26].get_text()
            personalFouls = cells[27].get_text()
            points = cells[28].get_text()
            tripleDoubles = cells[29].get_text()

            outputRows.append(
                {
                    "ID": ID,
                    "playerName": playerName,
                    "playerAge": playerAge,
                    "playerTeam": playerTeam,
                    "statsYear": statsYear,
                    "position": position,
                    "gamesPlayed": gamesPlayed,
                    "gamesStarted": gamesStarted,
                    "minutesPlayed": minutesPlayed,
                    "fieldGoals": fieldGoals,
                    "fieldGoalAttempts": fieldGoalAttempts,
                    "fieldGoalPercent": fieldGoalPercent,
                    "threePointersMade": threePointersMade,
                    "threePointAttempts": threePointAttempts,
                    "threePointPercent": threePointPercent,
                    "twoPointersMade": twoPointersMade,
                    "towPointAttempts": towPointAttempts,
                    "twoPointPercent": twoPointPercent,
                    "effectiveFieldGoalPercentage": effectiveFieldGoalPercentage,
                    "freeThrowsMade": freeThrowsMade,
                    "freeThrowAttempts": freeThrowAttempts,
                    "freeThrowPercent": freeThrowPercent,
                    "offensiveRebounds": offensiveRebounds,
                    "defensiveRebounds": defensiveRebounds,
                    "totalRebounds": totalRebounds,
                    "assists": assists,
                    "steals": steals,
                    "blocks": blocks,
                    "turnovers": turnovers,
                    "personalFouls": personalFouls,
                    "points": points,
                    "tripleDoubles": tripleDoubles,
                }
            )

        print(f"finished reference {year}")

    dataFrame = pd.DataFrame(outputRows)
    dataFrame = dataFrame.replace("", 0).fillna(0)
    dataFrame.to_csv("tableA.csv", index=False)


def espn():
    currentId = 1
    outputRows = []
    for year in years:
        file = open(f"./espn.{year}.out.html").read()
        soup = BeautifulSoup(file, "html.parser")

        for i in range(9999):
            rows = soup.find_all("tr", attrs={"data-idx": f"{i}"})
            if not rows:
                break

            playerData = rows[0].find_all("td")
            ID = currentId
            currentId = currentId + 1
            playerName = playerData[1].find("a").get_text()
            playerTeam = playerData[1].find("span").get_text()

            playerStats = rows[1].find_all("td")
            statsYear = year
            position = playerStats[0].get_text()
            gamesPlayed = playerStats[1].get_text()
            minutesPerGame = playerStats[2].get_text()
            pointsPerGame = playerStats[3].get_text()
            fieldGoalsPerGame = playerStats[4].get_text()
            fieldGoalAttemptsPerGame = playerStats[5].get_text()
            fieldGoalPercentage = playerStats[6].get_text()
            threePointersPerGame = playerStats[7].get_text()
            threePointAttemptsPerGame = playerStats[8].get_text()
            threePointPercentage = playerStats[9].get_text()
            freeThrowsPerGame = playerStats[10].get_text()
            freeThrowAttemptsPerGame = playerStats[11].get_text()
            freeThrowPercentage = playerStats[12].get_text()
            reboundsPerGame = playerStats[13].get_text()
            assistsPerGame = playerStats[14].get_text()
            stealsPerGame = playerStats[15].get_text()
            blocksPerGame = playerStats[16].get_text()
            turnoversPerGame = playerStats[17].get_text()
            doubleDoubles = playerStats[18].get_text()
            tripleDoubles = playerStats[19].get_text()

            outputRows.append(
                {
                    "ID": ID,
                    "playerName": playerName,
                    "playerTeam": playerTeam,
                    "statsYear": statsYear,
                    "position": position,
                    "gamesPlayed": gamesPlayed,
                    "minutesPerGame": minutesPerGame,
                    "pointsPerGame": pointsPerGame,
                    "fieldGoalsPerGame": fieldGoalsPerGame,
                    "fieldGoalAttemptsPerGame": fieldGoalAttemptsPerGame,
                    "fieldGoalPercentage": fieldGoalPercentage,
                    "threePointersPerGame": threePointersPerGame,
                    "threePointAttemptsPerGame": threePointAttemptsPerGame,
                    "threePointPercentage": threePointPercentage,
                    "freeThrowsPerGame": freeThrowsPerGame,
                    "freeThrowAttemptsPerGame": freeThrowAttemptsPerGame,
                    "freeThrowPercentage": freeThrowPercentage,
                    "reboundsPerGame": reboundsPerGame,
                    "assistsPerGame": assistsPerGame,
                    "stealsPerGame": stealsPerGame,
                    "blocksPerGame": blocksPerGame,
                    "turnoversPerGame": turnoversPerGame,
                    "doubleDoubles": doubleDoubles,
                    "tripleDoubles": tripleDoubles,
                }
            )

        print(f"finished espn {year}")

    dataFrame = pd.DataFrame(outputRows)
    dataFrame = dataFrame.replace("", 0).fillna(0)
    dataFrame.to_csv("tableB.csv", index=False)


if __name__ == "__main__":
    reference()
    espn()
