import numpy as np
import matplotlib.pyplot as plt

from enums import NewFields, NewFieldsIndex

numerical_pairs = [
    [NewFields.gamesPlayed, NewFieldsIndex.gamesPlayed],
    [NewFields.minutesPerGame, NewFieldsIndex.minutesPerGame],
    [NewFields.pointsPerGame, NewFieldsIndex.pointsPerGame],
    [NewFields.reboundsPerGame, NewFieldsIndex.reboundsPerGame],
    [NewFields.assistsPerGame, NewFieldsIndex.assistsPerGame],
    [NewFields.blocksPerGame, NewFieldsIndex.blocksPerGame],
    [NewFields.stealsPerGame, NewFieldsIndex.stealsPerGame],
]


def get_data():
    return np.genfromtxt(
        "./tableA.transformed.csv",
        delimiter=",",
        dtype=str,
        skip_header=True,
    )


def get_min_single_field(field):
    file_data = get_data()
    data = file_data[:, field].astype(float)

    min = data[0]
    for item in data:
        if item < min:
            min = item

    return min


def get_max_single_field(field):
    file_data = get_data()
    data = file_data[:, field].astype(float)

    max = data[0]
    for item in data:
        if item > max:
            max = item

    return max


def count_zeroes_single_field(field):
    file_data = get_data()
    data = file_data[:, field].astype(float)

    count = 0
    for item in data:
        if item == 0:
            count = count + 1

    return count


def count_zeroes_all_fields():
    for pairs in numerical_pairs:
        print(f"Total zeroes in {pairs[0]}: {count_zeroes_single_field(pairs[1])}")
    print()


def get_min_all_fields():
    for pairs in numerical_pairs:
        print(f"Minimum value for {pairs[0]}: {get_min_single_field(pairs[1])}")
    print()


def get_max_all_fields():
    for pairs in numerical_pairs:
        print(f"Maximum value for {pairs[0]}: {get_max_single_field(pairs[1])}")
    print()


def confirm_all_years():
    file_data = get_data()
    data = file_data[:, NewFieldsIndex.statsYear].astype(str)

    for item in data:
        if item not in ["2024", "2025", "2026"]:
            raise Exception()

    print(f"Confirmed that all {NewFields.statsYear} fields are 2024/25/26")
    print()


def get_text_info(field=NewFieldsIndex.playerName, fieldName=NewFields.playerName):
    file_data = get_data()
    data = file_data[:, field].astype(str)

    names = {}
    min = len(data[0])
    max = len(data[0])
    total = 0.0
    for item in data:
        item_len = len(item)
        total = total + item_len

        if item_len > max:
            max = item_len
        if item_len < min:
            min = item_len

        if names.get(item):
            names[item] = names[item] + 1
        else:
            names[item] = 1

    duplicates = 0
    for item in names.values():
        if item > 1:
            duplicates = duplicates + 1

    print(f"Minimum length of {fieldName}: {min}")
    print(f"Maximum length of {fieldName}: {max}")
    print(f"Average length of {fieldName}: {round(total / len(data), 2)}")
    print(f"Total duplicate values for {fieldName}: {duplicates}")
    print()


def plot_field(field, fieldName):
    file_data = get_data()
    data = file_data[:, field].astype(float)

    plt.hist(data, bins=20, edgecolor="black")
    plt.xlabel(fieldName)
    plt.ylabel("Count")
    plt.title(f"{fieldName} Distribution")
    plt.show()


def plot_numeric_fields():
    for pairs in numerical_pairs:
        plot_field(pairs[1], pairs[0])


def get_leaders_numeric_fields():
    file_data = get_data()
    data = file_data[
        :, NewFieldsIndex.gamesPlayed : NewFieldsIndex.stealsPerGame + 1
    ].astype(float)

    gamesPlayed = []
    minutesPerGame = []
    pointsPerGame = []
    reboundsPerGame = []
    assistsPerGame = []
    blocksPerGame = []
    stealsPerGame = []
    for row in data:
        gamesPlayed.append(float(row[NewFieldsIndex.gamesPlayed - 3]))
        minutesPerGame.append(float(row[NewFieldsIndex.minutesPerGame - 3]))
        pointsPerGame.append(float(row[NewFieldsIndex.pointsPerGame - 3]))
        reboundsPerGame.append(float(row[NewFieldsIndex.reboundsPerGame - 3]))
        assistsPerGame.append(float(row[NewFieldsIndex.assistsPerGame - 3]))
        blocksPerGame.append(float(row[NewFieldsIndex.blocksPerGame - 3]))
        stealsPerGame.append(float(row[NewFieldsIndex.stealsPerGame - 3]))

    gamesPlayed.sort(reverse=True)
    print(f"Top 3 for {NewFields.gamesPlayed}: {gamesPlayed[:3]}")
    minutesPerGame.sort(reverse=True)
    print(f"Top 3 for {NewFields.minutesPerGame}: {minutesPerGame[:3]}")
    pointsPerGame.sort(reverse=True)
    print(f"Top 3 for {NewFields.pointsPerGame}: {pointsPerGame[:3]}")
    reboundsPerGame.sort(reverse=True)
    print(f"Top 3 for {NewFields.reboundsPerGame}: {reboundsPerGame[:3]}")
    assistsPerGame.sort(reverse=True)
    print(f"Top 3 for {NewFields.assistsPerGame}: {assistsPerGame[:3]}")
    blocksPerGame.sort(reverse=True)
    print(f"Top 3 for {NewFields.blocksPerGame}: {blocksPerGame[:3]}")
    stealsPerGame.sort(reverse=True)
    print(f"Top 3 for {NewFields.stealsPerGame}: {stealsPerGame[:3]}")


def main():
    # count_zeroes_all_fields()
    # get_min_all_fields()
    # get_max_all_fields()
    # confirm_all_years()
    # get_text_info()
    # get_leaders_numeric_fields()
    plot_numeric_fields()


if __name__ == "__main__":
    main()
