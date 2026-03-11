class Fields:
    id = "id"
    statsYear = "statsYear"
    playerName = "playerName"
    gamesPlayed = "gamesPlayed"
    minutesPerGame = "minutesPerGame"
    pointsPerGame = "pointsPerGame"
    reboundsPerGame = "reboundsPerGame"
    assistsPerGame = "assistsPerGame"
    blocksPerGame = "blocksPerGame"
    stealsPerGame = "stealsPerGame"


class FieldsIndex:
    id = 0
    statsYear = 1
    playerName = 2
    gamesPlayed = 3
    minutesPerGame = 4
    pointsPerGame = 5
    reboundsPerGame = 6
    assistsPerGame = 7
    blocksPerGame = 8
    stealsPerGame = 9


class FieldsTolerance:
    statsYear = 0  # Must be exact as there are only 3 possible values
    playerName = 80  # 80% match
    gamesPlayed = 4  # 5% of the range of values rounded to nearest int
    minutesPerGame = 1.918  # 5% of the range of values
    pointsPerGame = 1.7345  # 5% of the range of values
    reboundsPerGame = 0.6945  # 5% of the range of values
    assistsPerGame = 0.579  # 5% of the range of values
    blocksPerGame = 0.2  # 5% of the range of values
    stealsPerGame = 0.1505  # 5% of the range of values
