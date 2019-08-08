import pandas as pd
import numpy as np
import random
import copy
import seaborn as sns
import matplotlib.pyplot as plt

def initialize(zeros,n):
    #creating graph
    graph= np.zeros((n,n))
    #its a symmetric graph 
    for i in range(n):
        for j in range(i):
            if random.random()>zeros:
                graph[i][j] = random.random()*100
                graph[j][i] = graph[i][j]

    return graph





def newMember(graph):
    #creates a new solution
    n=len(graph)
    route=np.zeros(0,dtype=int)
    go = 1
    i=1

    #taking the non zero values of the graph - points to go for 
    possible_values= np.nonzero(graph)
    possible_values=np.array([np.unique(possible_values)], dtype=int)

    while go:
        #selecting one of the possible values randomly
        proposed_value= random.randint(0,len(possible_values[0])-1)
        if possible_values[0][proposed_value]!=-1:          
            route = np.append(route,possible_values[0][proposed_value])
            possible_values[0][proposed_value]=-1
        
        if len(route)==len(possible_values[0]):
            go=0
        else:
            i+=1
    route=np.append(route,route[0])
    #print(route)

    return route




def mutate(route,probability,graph):
    #predefined probabilty of the child's dna to mutate (swap in this case)
    new_route = copy.deepcopy(route)
    for i in range(1,len(new_route)-1):
        if random.random()<probability:
            if i+1 <len(new_route)-2:
                new_route[i],new_route[i+1] = new_route[i+1],new_route[i]
            else:
                new_route[i],new_route[i-1] = new_route[i-1],new_route[i]
    return new_route


def startingPopulation(size, graph):
    #initial population i.e we create new members and add them to population
    population = []
    
    for i in range(size):
        population.append(newMember(graph))
        
    return population

def crossover(a,b):
    #crossing two parents
    length=len(a)

    #selecting two random cutpoints
    cut_point_1=random.randint(1,length-4)
    cut_point_2=random.randint(cut_point_1+1,length-2)

    #selecting a strand from parent "a"
    copystrand=copy.deepcopy(a[cut_point_1:cut_point_2])
    new_child=[-1]*length

    # child now has the strand of dna cut from "a" in the same indexes
    # and then taking the elements from "b" which are already not present in the copy strand
    # in the order that they are present in "b"
    new_child[cut_point_1:cut_point_2] = copy.deepcopy(copystrand)
    for i in range(0,length-1):
        for j in range(0,length-1):
            if new_child[j]==-1:
                if b[i] in new_child:
                    pass
                else:
                    new_child[j]=b[i]
                i+=1

            else:
                j+=1
    new_child[length-1]=new_child[0]

    return new_child

def fitness(route,graph):
    score = 0
    
    for i in range(1, len(route)):
        if (graph[route[i-1]][route[i]] == 0) and i != len(graph)-1:
            print(route)

            print("invalid route")
            print(route[i-1],route[i])
        score = score + graph[route[i-1]][route[i]]
            

    return score
def populationScore(population,graph):
    scores=[]
    for i in range(len(population)):
        scores+= [fitness(population[i],graph)]
    return scores


def heatmap(graph, route, iteration_number):
    #plotting the heatmap
    ax = sns.heatmap(graph)

    x=[0.5] + [x + 0.5 for x in route[0:len(route)-1]] + [len(graph) - 0.5]
    y=[0.5] + [x + 0.5 for x in route[1:len(route)]] + [len(graph) - 0.5]
    
    plt.plot(x, y, marker = 'o', linewidth=4, markersize=12, linestyle = "-", color='white')
    plt.savefig('images/new1000plot_%i.png' %(iteration_number), dpi=300)
    plt.show()


def pairing(scores):
    array = np.array(scores)
    temp = array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(array))

    fitness = [len(ranks) - x for x in ranks]
    
    cum_scores = copy.deepcopy(fitness)
    
    for i in range(1,len(cum_scores)):
        cum_scores[i] = fitness[i] + cum_scores[i-1]
        
    probs = [x / cum_scores[-1] for x in cum_scores]
    
    rand = random.random()
    
    for i in range(0, len(probs)):
        if rand < probs[i]:
            
            return i
def main():
    iterations=10000
    population_size=30
    last_distance = 1000000000
    new_generation=10
    winners=3

    graph=initialize(0,10)
    population=startingPopulation(population_size,graph)

    couples=int((population_size-new_generation)/2)

    for i in range(iterations):
        scores=populationScore(population,graph)
        new_population=[]

        best = population[np.argmin(scores)]
        number_of_moves = len(best)
        distance = fitness(best, graph)
        if distance != last_distance:

            print('Iteration %i: distance: %f' % (i, distance))
            print("Best found route= ",best)
            #remove the comment tag below to plot the heatmap
            heatmap(graph, best, i)

        
        for j in range(couples):
            new_1 = crossover(population[pairing(scores)], population[pairing(scores)])

            new_population += [new_1]

        for j in range(len(new_population)):
            new_population[j] = np.copy(mutate(new_population[j],0.05,graph))

        new_population += [population[np.argmin(scores)]]

        for j in range(1,winners):
            keeper=pairing(scores)
            new_population += [population[keeper]]

        while len(new_population)<population_size:
            new_population+=[newMember(graph)]
        population=copy.deepcopy(new_population)
        last_distance=distance




    

main()



