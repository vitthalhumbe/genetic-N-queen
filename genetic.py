
import matplotlib.pyplot as plt
import random


DNA = list
def generate_DNA(length):
    return random.choices(range(1, 8), k=length)

population = list
def generate_population(size, DNA_length):
    return [generate_DNA(DNA_length) for _ in range(size)]


def crossover(a, b):
    length = len(a)
    if length < 2:
        return a, b
    
    p = random.randint(1, length -1)
    return a[0:p] + b[p:], b[0:p]+a[p:]

def mutation(DNA, numbers=1, prob=0.5):
    for _ in range(numbers):
        random_index = random.randint(0, len(DNA) -1 )

        if random.random() > prob:
            return DNA
        else:
            DNA[random_index] = random.choice([i for i in range(1, 9)if i != DNA[random_index]])
    
    return DNA

def fitness(DNA):
    score = 0
    for i in range (len(DNA)):
        for j in range(i+1, len(DNA)):
            if (DNA[i] != DNA[j] and abs(DNA[i] - DNA[j]) != abs(i - j)):
                score += 1
    return score

def selection(population):
    population_fitness = sum([fitness(dna) for dna in population])
    probablities = [fitness(i) / population_fitness for i in population]

    return random.choices(population=population, weights=probablities, k=2)

def sort_population(population):
    return sorted(population, key=fitness, reverse=True)


def DNA_to_str(DNA):
    return "".join(map(str, DNA))



fitness_limit = 28
generation_limit = 1000

n=8

best_fitness = -1
stagnation = 0
STAGNATION_LIMIT = 10

mutation_rate = 0.02
MAX_MUTATION = 0.3

population = generate_population(100, n)
greatest_fitness_history = []
avg_fitness_history = []
for i in range(generation_limit):
    population = sorted(population, key=lambda dna:fitness(dna), reverse=True)

    print(f"\rGeneration {i} | Best Fitness: {fitness(population[0])}",end="",flush=True)


    if fitness(population[0]) >= fitness_limit:
        print(f"\n\nPopulation {i}")
        print("Best : ", DNA_to_str(population[0]), " | Fitness : ", fitness(population[0]))
        break
    
    greatest_fitness_history.append(fitness(population[0]))
    avg_fitness = sum(fitness(g) for g in population) / len(population)
    avg_fitness_history.append(avg_fitness)

    next_generation = population[0:2]
    current_best = fitness(population[0])
    if current_best > best_fitness:
        best_fitness = current_best
        stagnation = 0
        mutation_rate = 0.5  
    else:
        stagnation += 1


    if stagnation >= STAGNATION_LIMIT:
        mutation_rate = min(mutation_rate * 1.5, MAX_MUTATION)

    for j in range(int(len(population) / 2) - 1):
        parents = selection(population=population)
        offspring1, offspring2 = crossover(parents[0], parents[1])
        offspring1 = mutation(offspring1, prob=mutation_rate)
        offspring2 = mutation(offspring2, prob=mutation_rate)

        next_generation += [offspring1, offspring2]

    population = next_generation




plt.plot(greatest_fitness_history, label="greatest Fitness")
plt.plot(avg_fitness_history, label="average fitness")
plt.legend()
plt.show()
