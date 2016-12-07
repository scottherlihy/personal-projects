from dk1 import _
players = _()

# # This csv contains our predictions and salaries for each player. 
# # We parse each row of the csv and convert it into a Player object.
# with open('DKSalaries.csv', 'r') as data:
#     reader = csv.reader(data)
#     reader.next()
#     players = []
#     for row in reader:
#         name = row[1]
#         position = row[0]
#         salary = int(row[2])
#         points = float(row[4])
#         value = points / salary  
#         player = Player(position, name, salary, points, value)
#         players.append(player)

import random
import math
from operator import add
import matplotlib.pyplot as plt
# %matplotlib inline

def CreateRandomTeam():    
    team = {
    'pg' : random.sample(pgs,1),
    'sg' : random.sample(sgs,1),
    'pf' : random.sample(pfs,1),
    'sf' : random.sample(sfs,1),
    'c' : random.sample(cs,1),
    'g' : random.sample(gs,1),
    'f' : random.sample(fs,1),
    'u' : random.sample(utilities,1)
    }
    
    while True:
        team, noDuplicates = _checkNoDuplicates(team, team['g'][0], team['f'][0], team['u'][0])
        if noDuplicates == True:
            break
    return team

def _alreadyOnTeam(player, team):
	for position in team:
		return position[0] == player

def _checkNoDuplicates(team, guard, forward, utility):
    if _alreadyOnTeam(utility, team):
        team['u'] = random.sample(utilities,1)
        return team, False
    elif _alreadyOnTeam(guard, team):
        team['g'] = random.sample(gs,1)
        return team, False
    elif _alreadyOnTeam(forward, team):
        team['f'] = random.sample(fs,1)
        return team, False
    return team, True

def GetTeamPointTotal(team):
    total_points = 0
    for pos, players in team.iteritems():
        for player in players:
            total_points += player.points
    return total_points

def GetTeamSalary(team):
    total_salary = 0
    for pos, players in team.iteritems():
        for player in players:
            total_salary += player.salary
    return total_salary

def printTeam(team):
    printPlayer(team['pg'][0])
    printPlayer(team['sg'][0])
    printPlayer(team['pf'][0])
    printPlayer(team['sf'][0])
    printPlayer(team['g'][0])
    printPlayer(team['f'][0])
    printPlayer(team['c'][0])
    printPlayer(team['u'][0])

def printPlayer(p):
	print "Name:{}, Points:{}, Salary:{}, Position:{}, Value:{}".format(p.name, p.points, p.salary, p.position, p.value)

def CreatePopulation(count):
    return [CreateRandomTeam() for i in range(0,count)]

def fitness(team):
    points = GetTeamPointTotal(team)
    salary = GetTeamSalary(team)
    values = team.values()
    if salary > 50000:
        return 0
    return points

def grade(pop):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(team) for team in pop))
    return summed / (len(pop) * 1.0)

def listToTeam(players):
    return {
    'pg' : [players[0]],
    'sg' : [players[1]],
    'pf' : [players[2]],
    'sf' : [players[3]],
    'c' : [players[4]],
    'g' : [players[5]],
    'f' : [players[6]],
    'u' : [players[7]]
}

def breed(mother, father):
    # positions = ['pg','sg','pf','sf','c','g','f','u']
    
    mother_lists = [mother['pg'] + mother['sg'] + mother['pf'] + mother['sf'] + mother['c'] + mother['g'] + mother['f'] + mother['u']]
    mother_list = [item for sublist in mother_lists for item in sublist]
    father_lists = [father['pg'] + father['sg'] + father['pf'] + father['sf'] + father['c'] + father['g'] + mother['f'] + mother['u']]
    father_list = [item for sublist in father_lists for item in sublist]

    index = random.choice(range(8))
    child1 = listToTeam(mother_list[0:index] + father_list[index:])
    child2 = listToTeam(father_list[0:index] + mother_list[index:])

    while True:
        child1, noDuplicates = _checkNoDuplicates(child1, child1['g'][0], child1['f'][0], child1['u'][0])
        if noDuplicates == True:
            break

    while True:
        child2, noDuplicates = _checkNoDuplicates(child2, child2['g'][0], child2['f'][0], child2['u'][0])
        if noDuplicates == True:
            break

    return[child1, child2] 

def mutate(team):
    positions = ['pg','sg','pf','sf','c','g','f','u']
      
    random_pos = random.choice(positions)
    if random_pos == 'pg':
        team['pg'][0] = random.choice(pgs)
    if random_pos == 'sg':
        team['sg'][0] = random.choice(sgs)
    if random_pos == 'pf':
        team['pf'][0] = random.choice(pfs)
    if random_pos == 'sf':
        team['sf'][0] = random.choice(sfs)
    if random_pos == 'c':
        team['c'][0] = random.choice(cs)
    if random_pos == 'g':
        team['g'][0] = random.choice(gs)
    if random_pos == 'f':
        team['f'][0] = random.choice(fs)
    if random_pos == 'u':
        team['u'][0] = random.choice(utilities)
        
    while True:
        team, noDuplicates = _checkNoDuplicates(team, team['g'][0], team['f'][0], team['u'][0])
        if noDuplicates == True:
            break

    return team            

def evolve(pop, retain=0.35, random_select=0.05, mutate_chance=0.005):
    graded = [ (fitness(team), team) for team in pop]
    graded = [ x[1] for x in sorted(graded, reverse=True)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random.random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate_chance > random.random():
            individual = mutate(individual)

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = random.randint(0, parents_length-1)
        female = random.randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            babies = breed(male,female)
            for baby in babies:
                children.append(baby)
    parents.extend(children)
    return parents

def ShowOutput(team):
    printTeam(team)
    print GetTeamSalary(team)
    print GetTeamPointTotal(team)


pgs = [player for player in players if 'PG' in player.position]
sgs = [player for player in players if 'SG' in player.position]
pfs = [player for player in players if 'PF' in player.position]
sfs = [player for player in players if 'SF' in player.position]
cs = [player for player in players if 'C' in player.position]
gs = [player for player in players if 'PG' in player.position or 'SG' in player.position]
fs = [player for player in players if 'PF' in player.position or 'SF' in player.position]
utilities = [player for player in players]

def EvolutionLoop():
    best_teams = []
    history = []
    p = CreatePopulation(10000)
    fitness_history = [grade(p)]
    for i in xrange(40):
        p = evolve(p)
        fitness_history.append(grade(p))
        valid_teams = [ team for team in p if GetTeamSalary(team) <= 50000]
        valid_teams = sorted(valid_teams, key=GetTeamPointTotal, reverse=True)
        if len(valid_teams) > 0:
            best_teams.append(valid_teams[0])
        for team in best_teams:
            if GetTeamSalary(team) > 50000:
                    print GetTeamSalary(team)
    for datum in fitness_history:
        history.append(datum)

    best_teams = sorted(best_teams, key=GetTeamSalary, reverse=True)
    choice = best_teams[0]
    # ShowOutput(choice)
    return choice

def GenerateBestTeam():
    the_best_teams = []
    for i in range(15):
        the_best_teams.append(EvolutionLoop())
    the_best_teams = sorted(the_best_teams, key=GetTeamSalary, reverse=True)
    # for team in best_teams:
    #     ShowOutput(team)

GenerateBestTeam()

# general clean everything up / good naming / etc
# teams over 50K
# Get data better
# automate multiple times