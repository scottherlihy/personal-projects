#Team = namedtuple('Team', [position for position in POSITIONS])

from abc import ABCMeta, abstractmethod
from collections import defaultdict, namedtuple


class InvalidTeamException(Exception):
    pass

class TeamRequirementsNotSatisfiedException(InvalidTeamException):
    pass

class InvalidAllowanceException(InvalidTeamException):
    pass


# POSITIONS = ['PG','SG','PF','SF','C','G','F','U']
BaseAllowance = namedtuple('BaseAllowance', ['min', 'max'])
class Allowance(BaseAllowance):
    def __new__(cls, minimum, maximum=None):
        maximum = maximum or minimum
        if minimum > maximum:
            raise InvalidAllowanceException('Min must be greater than max')
        return super(Allowance, cls).__new__(cls, minimum, maximum)

# TODO supoort for 0 allowance
# no duplicates
class Team(object):
    __metaclass__ = ABCMeta
    def __init__(self, players, constraints): #TODO look into dymanic programming for constraint
        """
        @param players
        @param constraints Constraints are a dictionary that are a mapping of Position to Allowance
        """
        self.players = players
        self.positions = []
        for key in constraints.keys():
            setattr(self, key.__class__.__name__, defaultdict(Utility))
            self.positions.append(key)
        self.postitionRegistry = defaultdict(int)
        self.constraints = constraints
        self.numPositionsSatisfied = 0
        
        for player in self.players:    # can I do better than a nested loop?
            for position in self.positions:
                self._addPlayer(player, position)
                        
        if self.numPositionsSatisfied != len(self.positions):
            print self.numPositionsSatisfied
            print len(self.positions)
            raise TeamRequirementsNotSatisfiedException(
                'Team requirements not satisfied for every player {}'.format(self.__str__()))
        if not self._isValid():
            raise InvalidTeamException('This team has duplicate players')

    def _addPlayer(self, player, position):
        if isinstance(player.position, position):
            # print '\n'
            # print player.position
            # print position.__name__
            self.postitionRegistry[position.__name__] += 1
            # print self.postitionRegistry[position.__name__]
            if self.constraints[position].min == self.postitionRegistry[position.__name__]:
                self.numPositionsSatisfied += 1
            elif self.constraints[position].max < self.postitionRegistry[position.__name__]:
                raise TeamRequirementsNotSatisfiedException('Too many players for position {}'.format(position.__name__))

    #TODO(make this dynamic to more than just basketball teams)
    def _isValid(self):
        names = [p.name for p in players]
        return len(names) == len(set(names))

    def _alreadyOnTeam(self, player, team):
        for position in team:
            return position[0] == player

    def __str__(self):
        return '\n'.join([player.__str__() for player in self.players])

    def GetTeamPointTotal(self):
        return sum([player.points for player in self.players])

    def GetTeamSalary(self):
        return sum([player.salary for player in self.players])

    def ShowOutput(self):
        print '\n' + '---------------------------------'

        print self.GetTeamSalary()
        # print self.GetTeamPointTotal()
        print '---------------------------------' + '\n'


class DefaultBasketballTeam(Team):
    def __init__(self, players): #Check if the players are of a type that's not supported? else case in Team?
            constraints = {PointGuard : Allowance(1, 3),
                       ShootingGuard: Allowance(1, 3),
                       PowerForward: Allowance(1, 3),
                       SmallForward: Allowance(1, 3),
                       Center: Allowance(1, 3),
                       Guard: Allowance(3, 4),
                       Forward: Allowance(3, 4),
                       Utility: Allowance(8)}
            super(DefaultBasketballTeam, self).__init__(players, constraints)


#can positions be strings again? no because isinstance could maybe make tuples or something
class Utility(object):
    def __init__(self):
        pass

class Guard(Utility):
    pass


class Forward(Utility):
    pass


class PointGuard(Guard):
    pass


class ShootingGuard(Guard):
    pass


class PowerForward(Forward):
    pass


class SmallForward(Forward):
    pass


class Center(Utility):
    pass


from .GetPlayers import Player
pg =  Player(PointGuard(), 'name', 100)
sg =  Player(ShootingGuard(), 'name1', 100)
pf =  Player(PowerForward(), 'name2', 100)
sf =  Player(SmallForward(), 'name3', 100)
c =  Player(Center(), 'name4', 100)
g =  Player(PointGuard(), 'name5', 100)
f =  Player(SmallForward(), 'name6', 100)
u =  Player(PointGuard(), 'name7', 100)

players = [pg,sg,pf,sf,c,g,f,u]       
team = DefaultBasketballTeam(players)
print team
team.ShowOutput()