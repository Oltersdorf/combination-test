import random
import time

player = []
playerNumber = 41
rank = [1, 2, 3, 4]
games = []
partners = {}


for n in range(1, playerNumber + 1):
    player.append((n, random.choice(rank)))
print(player)

for p in player:
    partners[p] = []

playerRanks = [r for _,r in player]
for i in rank:
    print(f"rank {i}: {playerRanks.count(i)}")

for a in range(1, 11):
    seedPerformance = []
    timeMessureBefore = time.perf_counter_ns()
    for i in range(20000):
        seed = random.random()
        r = random.Random(seed)
        playerCopy = player.copy()
        gamesGenerated = []
        isInvalid = False

        for n in range(int(playerNumber / 4)):
            p1 = playerCopy[r.randint(0, len(playerCopy) - 1)]
            playerCopy.remove(p1)
            p1ValidPartners = [v for v in playerCopy if v not in partners[p1]]
            if len(p1ValidPartners) == 0:
                isInvalid = True
                break
            p2 = p1ValidPartners[r.randint(0, len(p1ValidPartners) - 1)]
            playerCopy.remove(p2)
            p3 = playerCopy[r.randint(0, len(playerCopy) - 1)]
            playerCopy.remove(p3)
            p3ValidPartners = [v for v in playerCopy if v not in partners[p3]]
            if len(p3ValidPartners) == 0:
                isInvalid = True
                break
            p4 = p3ValidPartners[r.randint(0, len(p3ValidPartners) - 1)]
            playerCopy.remove(p4)
            gamesGenerated.append(((p1, p2), (p3, p4)))

        performance = 0
        worstPerformance = 0
        for game in gamesGenerated:
            p = abs((game[0][0][1] + game[0][1][1]) - (game[1][0][1] + game[1][1][1]))
            performance = performance + p
            if p > worstPerformance:
                worstPerformance = p

        if not isInvalid:
            seedPerformance.append((seed, performance, worstPerformance))
        
    timeMessureAfter = time.perf_counter_ns()

    print(f"Round {a}:")
    print(f"time needed: {timeMessureAfter - timeMessureBefore}ns ({(timeMessureAfter - timeMessureBefore) / 1000000000}s)")
    bestPerformance = (0, 1000000, 10000000)
    invalidCounter = 20000 - len(seedPerformance)
    for sp in seedPerformance:
        if sp[2] < bestPerformance[2]:
            bestPerformance = sp
        elif sp[2] == bestPerformance[2] and sp[1] < bestPerformance[1]:
            bestPerformance = sp
        

    print(f"best performace of {bestPerformance[1]} with worst difference of {bestPerformance[2]})")
    print(f"Invalid runs: {invalidCounter}")

    r = random.Random(bestPerformance[0])
    playerCopy = player.copy()

    for n in range(int(playerNumber / 4)):
        p1 = playerCopy[r.randint(0, len(playerCopy) - 1)]
        playerCopy.remove(p1)
        p1ValidPartners = [v for v in playerCopy if v not in partners[p1]]
        p2 = p1ValidPartners[r.randint(0, len(p1ValidPartners) - 1)]
        playerCopy.remove(p2)
        p3 = playerCopy[r.randint(0, len(playerCopy) - 1)]
        playerCopy.remove(p3)
        p3ValidPartners = [v for v in playerCopy if v not in partners[p3]]
        p4 = p3ValidPartners[r.randint(0, len(p3ValidPartners) - 1)]
        playerCopy.remove(p4)
        games.append(((p1, p2), (p3, p4)))

    for p in player:
            partners[p] = []

    for g in games:
        partners[g[0][0]].append(g[0][1])
        partners[g[0][1]].append(g[0][0])
        partners[g[1][0]].append(g[1][1])
        partners[g[1][1]].append(g[1][0])

badGames = [g for g in games if (g[0][0][1] + g[0][1][1]) != (g[1][0][1] + g[1][1][1])]
print(badGames)
