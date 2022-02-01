import random
import itertools
import datetime


def createGroupsFromTeams(teams):
    groups = [[], [], [], []]

    for group in groups:
        while len(group) != 4:
            canAddTeams = [i for i in itertools.filterfalse(lambda x: x in itertools.chain(*groups), teams)]
            group.append(canAddTeams[random.randint(0, len(canAddTeams) - 1)])

    return groups


def printCalendarForTeams(teams):
    gameDate = datetime.datetime(2022, 9, 14, 22, 45)
    twoWeek = datetime.timedelta(weeks=2)

    for i in range(0, int(len(teams) / 2)):
        print(gameDate.strftime("%d/%m/%Y,%H:%M"))
        gameDate += twoWeek


teams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

print(createGroupsFromTeams(teams))
print()
printCalendarForTeams(teams)
