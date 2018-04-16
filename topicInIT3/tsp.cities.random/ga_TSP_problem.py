from random import random, shuffle, randint, choice
import csv
from copy import deepcopy, copy
import numpy as np
import matplotlib.pyplot as plt
import time

LENGTH = 0  # DNA's length
N = 64  # population
Mprob = 0.1
Cprob = 1.0
GENERATION = 3000
cityInf = []
# cityDistance = [[0 for i in range(LENGTH)] for j in range(LENGTH)]


def rand_idx(N): return randint(0, N - 1)


def coin(p=0.5): return 1 if (random() < p) else 0


def random_individual(LENGTH=LENGTH):
    temp = [i for i in range(LENGTH)]
    shuffle(temp)
    return temp


def initial_population(N=N, LENGTH=LENGTH): return [
    random_individual(LENGTH) for i in range(N)]


def distance(indOne, indTwo):
    # for city in cityInf:
    #     if city[0] == indOne:
    #         x1 = city[1]
    #         y1 = city[2]
    #     if city[0] == indTwo:
    #         x2 = city[1]
    #         y2 = city[2]
    # assert cityDistance[indOne][indTwo] == ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return cityDistance[indOne][indTwo]


def fitness(indivial):
    distanceList = []
    for i in range(LENGTH - 1):
        distanceList.append(distance(indivial[i], indivial[i + 1]))
    return -1 * sum(distanceList)


def selection(population):
    newPopulation = []
    for k in range(N):
        c1 = choice(population)
        c2 = choice(population)
        c12 = c1
        if fitness(c1) < fitness(c2):
            c12 = c2
        newPopulation.append(c12)
    return newPopulation


def crossover(population):
    newPopulation = []
    for i in range(N / 2):
        nc1 = c1 = copy(population[2 * i])
        nc2 = c2 = copy(population[2 * i + 1])
        if random() < Cprob:
            k1 = k2 = 0
            while k1 == k2:
                k1 = randint(1, LENGTH - 2)
                k2 = randint(1, LENGTH - 2)
            if k1 > k2:
                k1, k2 = k2, k1
            middle1 = c1[k1:k2]
            middle2 = c2[k1:k2]
            for k in middle1:
                c2.remove(k)
            for k in middle2:
                c1.remove(k)
            nc1 = c2[:k1] + middle1[:] + c2[k1:]
            nc2 = c1[:k1] + middle2[:] + c1[k1:]
        # assert len(nc1) == 30
        # assert len(nc2) == 30
        # assert sum(nc1) == 435
        # assert sum(nc2) == 435
        newPopulation.append(nc1)
        newPopulation.append(nc2)
    return newPopulation


def mutation(population):
    for i in range(N):
        if coin(Mprob):
            k1 = k2 = 0
            while k1 == k2:
                k1 = rand_idx(LENGTH)
                k2 = rand_idx(LENGTH)
            population[i][k1], population[i][
                k2] = population[i][k2], population[i][k1]
    return population


def check_stop(fitness_population):
    if echo > GENERATION:
        return True
    else:
        return False


def sum_population(fitness_population):
    summerOne = 0
    for i in fitness_population:
        summerOne += fitness(i)
    return summerOne


def sum_population(fitness_population): return sum(
    map(fitness, fitness_population))


def show(population):
    print ('The echo is: %d' % (echo))
    # for i in population:
    #     print i
    print ('The percentage of sum is: %f' % (sum_population(population) / float(N) / LENGTH))
    maxFitness = 0
    for i in population:
        if maxFitness < fitness(i):
            maxFitness = fitness(i)
    print ('The max is: %f' % (maxFitness))
    print ('')


def best_fit(population):
    fitness_values = map(fitness, population)
    bf = max(fitness_values)
    bf_idx = fitness_values.index(bf)
    return bf, population[bf_idx]


def show(population): print ("[G %03d]" % echo, best_fit(population))


def showGraph(population):
    _, bestPopulation = best_fit(population)
    a = 0
    b = bestPopulation[0]
    for i, _ in enumerate(bestPopulation):
        if i == LENGTH - 1:
            break
        a = b
        b = bestPopulation[i + 1]
        # print '%d, %d' % (a, b)
        for city in cityInf:
            if city[0] == a:
                x1 = city[1]
                y1 = city[2]
            if city[0] == b:
                x2 = city[1]
                y2 = city[2]
        x = np.linspace(x1, x2, 128, endpoint=True)
        if(float(x1 -x2) == 0):
            plt.vlines(x1, y1, y2)
        else:
            k = (y1 - y2) / float(x1 - x2)
            bias = y1 - k * x1
            y = k * x + bias
            plt.plot(x, y)
    # closeFigure(2)
    plt.show()
    return 0

def closeFigure(waitTime):
    time.sleep(waitTime)
    plt.close()


def run():
    population = initial_population(N, LENGTH)
    showGraph(population)
    exit()
    global echo
    echo = 0
    while True:
        print ('The echo is %d' % echo)
        population = selection(population)
        population = crossover(population)
        population = mutation(population)
        show(population)
        echo += 1
        if check_stop(population):
            showGraph(population)
            break


def readCSV(directory):
    global cityInf
    global cityDistance
    global LENGTH
    with open(directory, 'r') as f:
        reader = csv.reader(f)  # , delimiter=',', quoting=csv.QUOTE_NONE)
        next(reader)
        next(reader)
        for row in reader:
            row = n, x, y = int(row[0]), float(row[1]), float(row[2])
            cityInf.append(row)
            LENGTH += 1
        print ('The number of city is %d' % LENGTH)
        cityDistance = [[0 for i in range(LENGTH)] for j in range(LENGTH)]
        for cityOne in range(LENGTH):
            for cityTwo in range(LENGTH):
                x1 = cityInf[cityOne][1]
                y1 = cityInf[cityOne][2]
                x2 = cityInf[cityTwo][1]
                y2 = cityInf[cityTwo][2]
                cityDistance[cityOne][cityTwo] = (
                    (x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


if __name__ == '__main__':
    # readCSV('/Users/irvine/Dropbox/Programming/topicInIT3/tsp.cities/tsp.cities.csv')
    readCSV('/Users/irvine/Dropbox/Programming/topicInIT3/tsp.cities.random/tsp.cities.csv2')
    run()
