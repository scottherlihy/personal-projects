from Team import Team

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
