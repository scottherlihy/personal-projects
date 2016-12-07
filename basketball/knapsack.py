from GetPlayers import _
players = _()

AVAILABLE_PGS = [player for player in players if 'PG' in player.position]
AVAILABLE_SGS = [player for player in players if 'SG' in player.position]
AVAILABLE_PFS = [player for player in players if 'PF' in player.position]
AVAILABLE_SFS = [player for player in players if 'SF' in player.position]
AVAILABLE_CS = [player for player in players if 'C' in player.position]
AVAILABLE_GS = [player for player in players if 'PG' in player.position or 'SG' in player.position]
AVAILABLE_FS = [player for player in players if 'PF' in player.position or 'SF' in player.position]
AVAILABLE_UTILITIES = [player for player in players]

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

TEAM_SIZE = 8
POSITIONS = ['pg','sg','pf','sf','c','g','f','u']

class PopulationInitializer(object):
    def __init__(self):
        pass

    def CreatePopulation(self, count):
        """
        @param count The number of teams to add to the population
        @returns a list of dictionaries of the string representation of position to player
        """
        z = [self.CreateRandomTeam() for i in range(count)]
        print z[0]
        return z

    def CreateRandomTeam(self):
        """
        @returns a dictionary of the string representation of position to player
        """
        team = {
        'pg' : random.sample(AVAILABLE_PGS,1),
        'sg' : random.sample(AVAILABLE_SGS,1),
        'pf' : random.sample(AVAILABLE_PFS,1),
        'sf' : random.sample(AVAILABLE_SFS,1),
        'c' : random.sample(AVAILABLE_CS,1),
        'g' : random.sample(AVAILABLE_GS,1),
        'f' : random.sample(AVAILABLE_FS,1),
        'u' : random.sample(AVAILABLE_UTILITIES,1)
        }
        
        while True:
            team, noDuplicates = self.CheckNoDuplicates(team, team['g'][0], team['f'][0], team['u'][0])
            if noDuplicates == True:
                break
        return team

    def _alreadyOnTeam(self, player, team):
        for position in team:
            return position[0] == player

    def CheckNoDuplicates(self, team, guard, forward, utility):
        if self._alreadyOnTeam(utility, team):
            team['u'] = random.sample(utilities,1)
            return team, False
        elif self._alreadyOnTeam(guard, team):
            team['g'] = random.sample(gs,1)
            return team, False
        elif self._alreadyOnTeam(forward, team):
            team['f'] = random.sample(fs,1)
            return team, False
        return team, True


class TeamInterpreter(object):
    def __init__(self):
        pass

    def GetTeamPointTotal(self, team):
        total_points = 0
        for pos, players in team.iteritems():
            for player in players:
                total_points += player.points
        return total_points

    def GetTeamSalary(self, team):
        total_salary = 0
        for pos, players in team.iteritems():
            for player in players:
                total_salary += player.salary
        return total_salary


class Darwin(object):
    def __init__(self, writer=None, initializer=None, interpreter=None):
        self.consoleWriter = ConsoleWriter()
        self.initializer = PopulationInitializer()
        self.interpreter = TeamInterpreter()

    def Fitness(self, team):
        points = self.interpreter.GetTeamPointTotal(team)
        salary = self.interpreter.GetTeamSalary(team)
        values = team.values()
        if salary > 50000:  #should be unnecessary if create random team is guaranteed to return a valid team
            return 0
        return points

    def Grade(self, pop):
        """ Find average fitness for a population.
        """
        summed = reduce(add, (self.Fitness(team) for team in pop))
        return summed / (len(pop) * 1.0)

    def _listToTeam(self, players):
        return {'pg' : [players[0]],
                'sg' : [players[1]],
                'pf' : [players[2]],
                'sf' : [players[3]],
                'c' : [players[4]],
                'g' : [players[5]],
                'f' : [players[6]],
                'u' : [players[7]]
                }          

    def _getPlayersAtPositions(self, parent):
        """
        @returns a list of Players
        """
        allPlayers = [parent['pg'] + parent['sg'] + parent['pf'] + parent['sf'] + parent['c'] + parent['g'] + parent['f'] + parent['u']]
        return [item for sublist in allPlayers for item in sublist]

        return team  

    def Breed(self, mother, father):
        """
        @returns a list of Teams
        """
        motherList = self._getPlayersAtPositions(mother)
        fatherList = self._getPlayersAtPositions(father)

        index = random.choice(range(1, TEAM_SIZE))
        child1 = self._listToTeam(motherList[:index] + fatherList[index:])
        child2 = self._listToTeam(fatherList[:index] + motherList[index:])

        while True:
            child1, noDuplicates = self.initializer.CheckNoDuplicates(child1, child1['g'][0], child1['f'][0], child1['u'][0])
            if noDuplicates == True:
                break

        while True:
            child2, noDuplicates = self.initializer.CheckNoDuplicates(child2, child2['g'][0], child2['f'][0], child2['u'][0])
            if noDuplicates == True:
                break

        return[child1, child2] 

    def Mutate(self, team):      
        random_pos = random.choice(AVAILABLE_POSITIONS)
        if random_pos == 'pg':
            team['pg'][0] = random.choice(AVAILABLE_PGS)
        if random_pos == 'sg':
            team['sg'][0] = random.choice(AVAILABLE_SGS)
        if random_pos == 'pf':
            team['pf'][0] = random.choice(AVAILABLE_PFS)
        if random_pos == 'sf':
            team['sf'][0] = random.choice(AVAILABLE_SFS)
        if random_pos == 'c':
            team['c'][0] = random.choice(AVAILABLE_CS)
        if random_pos == 'g':
            team['g'][0] = random.choice(AVAILABLE_GS)
        if random_pos == 'f':
            team['f'][0] = random.choice(AVAILABLE_FS)
        if random_pos == 'u':
            team['u'][0] = random.choice(AVAILABLE_UTILITIES)
            
        while True:
            team, noDuplicates = self.initializer.CheckNoDuplicates(team, team['g'][0], team['f'][0], team['u'][0])
            if noDuplicates == True:
                break

    def Evolve(self, pop, retain=0.35, random_select=0.05, mutate_chance=0.005):
        graded = [ (self.Fitness(team), team) for team in pop]
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
                individual = self.Mutate(individual)

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
                babies = self.Breed(male,female)
                for baby in babies:
                    children.append(baby)
        parents.extend(children)
        return parents

    def EvolutionLoop(self):
        best_teams = []
        history = []
        p = self.initializer.CreatePopulation(10)
        fitness_history = [self.Grade(p)]
        for i in xrange(1):
            # for team in best_teams:
            #     if self.interpreter.GetTeamSalary(team) > 50000:
            #             print "~:{}".format(self.interpreter.GetTeamSalary(team))
            p = self.Evolve(p)
            fitness_history.append(self.Grade(p))
            valid_teams = [team for team in p if self.interpreter.GetTeamSalary(team) <= 50000]
            valid_teams = sorted(valid_teams, key=self.interpreter.GetTeamPointTotal, reverse=True)
            # for team in valid_teams:
            #     if self.interpreter.GetTeamSalary(team) > 50000:
            #             print self.interpreter.GetTeamSalary(team)
            if len(valid_teams) > 0:
                best_teams.append(valid_teams[0])
            # for team in best_teams:
            #     if self.interpreter.GetTeamSalary(team) > 50000:
            #             print self.interpreter.GetTeamSalary(team)
        for datum in fitness_history:
            history.append(datum)

        best_teams = sorted(best_teams, key=self.interpreter.GetTeamSalary, reverse=True)
        print 'Number of valid teams: {}'.format(str(len(valid_teams)))
        choice = best_teams[0]
        # self.consoleWriter.ShowOutput(choice)
        return choice

class ConsoleWriter(object):
    def __init__(self):
        self.interpreter = TeamInterpreter()

    def ShowOutput(self, team):
        print '\n' + '---------------------------------'

        self.printTeam(team)
        print self.interpreter.GetTeamSalary(team)
        print self.interpreter.GetTeamPointTotal(team)
        print '---------------------------------' + '\n'

    def printTeam(self, team):
        self.printPlayer(team['pg'][0])
        self.printPlayer(team['sg'][0])
        self.printPlayer(team['pf'][0])
        self.printPlayer(team['sf'][0])
        self.printPlayer(team['g'][0])
        self.printPlayer(team['f'][0])
        self.printPlayer(team['c'][0])
        self.printPlayer(team['u'][0])

    def printPlayer(self, p):
        print "Name:{}, Points:{}, Salary:{}, Position:{}, Value:{}".format(p.name, p.points, p.salary, p.position, p.value)



if __name__ == '__main__':
    the_best_teams = []
    algo = Darwin()
    for i in range(10):
        the_best_teams.append(algo.EvolutionLoop())

    consoleWriter = ConsoleWriter()
    interpreter = TeamInterpreter()
    best_team = sorted(the_best_teams, key=interpreter.GetTeamSalary, reverse=True)[0]
    consoleWriter.ShowOutput(best_team)


# TODO
# Get data better
# automate multiple times
# put in max number of retries
