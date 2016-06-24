import random, math
import numpy as np
import matplotlib.pyplot as plt

encoding = {
        '0000' : '0',
        '0001' : '1',
        '0010' : '2',
        '0011' : '3',
        '0100' : '4',
        '0101' : '5',
        '0110' : '6',
        '0111' : '7',
        '1000' : '8',
        '1001' : '9',
        '1010' : '+',
        '1011' : '*',
        '1100' : '-',
        '1101' : '/',
        '1110' : '1', #extra encodings for 0, 1
        '1111' : '2',
}
operators = ['+','-', '/', '*'];
operands = ['1','2', '3', '4', '5','6','7','8','9', '0'];

population = {};
target = 55;
    
history = [];
iterations = [];
def plot():
    plt.plot(iterations,history, 'b-');
    plt.show();

def startExp():
    createStartingPool(500, 9);
    for i in range(0, 100000):
        history.append(iterateGeneration(i));
        iterations.append(i)
    plot();

def iterateGeneration(i):
    #weight parameters
    global population
    temppopulation={};
    total = sum(population.values());
    if total ==0:
        print("SIMULATION FAILED: ENTIRE POPULATION DEAD");
        plot();
        input("Press Enter to continue...");
        quit();

    for s in population:
        population[s] /= total;
    for j in range(0, len(population), 2):
        p1 = np.random.choice(list(population.keys()),p=list(population.values()));
        p2 = np.random.choice(list(population.keys()),p=list(population.values()));

        offspring1, offspring2 = breedOffspring(p1,p2);
        temppopulation[offspring1] = evaluateChromosome(offspring1);
        temppopulation[offspring2] = evaluateChromosome(offspring2);

    population =temppopulation;

    print("Iteration " + str(i) + ": Best bitstring and value are");
    
    bitstring = max(population, key=lambda x: population[x]);
    print(bitstring);
    print([encoding[bitstring[i:i+4]] for i in range(0, len(bitstring), 4)]);
    print(population[bitstring]);
    return population[bitstring];


def createStartingPool(popSize, expLength):
    #generate random int and convert to binary string
    for i in range(0,popSize):
        s = bin(random.randint(0, math.pow(2, 4*expLength)))[2:].zfill(4*expLength);
        population[s] = evaluateChromosome(s);

def breedOffspring(parent1, parent2):
    offspring1, offspring2= "","";
    crossoverPoint = 0;
    crossoverRate = 0.7;
    mutationRate = 0.001;

    if random.random() < crossoverRate:
        crossoverPoint = random.randint(0, len(parent1));
        offspring1 = parent1[:crossoverPoint] + parent2[crossoverPoint:];
        offspring2 = parent2[:crossoverPoint] + parent1[crossoverPoint:];

        for i in range(crossoverPoint, len(parent1)):
            if random.random() < mutationRate:
                list1 = list(offspring1);
                list1[i] = '1' if offspring1[i] == '0' else '0';
                offspring1 = "".join(list1);

            if random.random() < mutationRate:
                list2 = list(offspring2);
                list2[i] = '1' if offspring2[i] == '0' else '0';
                offspring2 = "".join(list2);
    else:
        offspring1 = parent1;
        offspring2 = parent2;
    return (offspring1, offspring2);
    
def evaluateChromosome(bitstring):
    expression = [encoding[bitstring[i:i+4]] for i in range(0, len(bitstring), 4)];

    if expression[0] in operators or expression[-1] in operators:
        return 0;

    #making the stacks
    numbers=[];
    operations=[];
    numString="";
    needOperand=False;

    for c in expression:
        if needOperand and c in operators:
            return 0;
        elif needOperand and c in operands:
            needOperand = False;

        if c in operands:
            numString+=c;
        else:
            needOperand = True;
            operations.append(c);
            if len(numString) != 0:
                numbers.append(int(numString));
            numString = "";

    if len(numString) != 0:
        numbers.append(int(numString));

    #evaluating the stacks
    while len(operations)!=0:
        num1 = numbers.pop(0);
        num2 = numbers.pop(0);
        op=operations.pop(0);

        if op == '+':
            numbers.insert(0, num1+num2);
        elif op == '*':
            numbers.insert(0, num1*num2);
        elif op == '-':
            numbers.insert(0, num1-num2);
        elif op == '/':
            if num2 == 0:
                return 0;
            numbers.insert(0, num1/num2);

    if numbers[0] == target:
        print("FOUND EXPRESSION:  "  + "".join(expression));
        plot();
        input("Press Enter to continue...");
        quit();

    return abs(1/(target-numbers[0]));

if __name__ == '__main__':
    startExp();
