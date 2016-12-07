import csv

class RankingsQueue(object):
	def __init__(self, league):
		self.league = league
		self.players = []

	def SortPlayers(self):
		for player in self.league.GetPlayers():
			self._insert(player)

	def _insert(self, player):
		if not self.players:
			self.players.append(player)
			return

		for i,j in enumerate(self.players):
			if player.points > j.points or i == len(self.players):
				self.players.insert(i, player)
				return

	def GetRankings(self):
		for p in self.players:
			# print "Name:{}, Points:{}, Salary:{}, Position:{}, Value:{}".format(p.name, p.points, p.salary, p.position, p.value)
			pass

	def GetPlayers(self):
		return self.league


class League(object):
	def __init__(self, players):
		self.players = players

	# Name needs to be "First Last"
	def GetPlayer(self, name):
		for player in self.players:
			if name == player.name:
				return player

	def GetPlayers(self):
		return [player for player in self.players if hasattr(player, 'points')]


class Player(object):
	def __init__(self, position, name, salary, gameInfo):
		if '/' in position:
			self.position = position.split('/')
		else:
			self.position = [position]
		self.name = name
		self.salary = float(salary)
		self.gameInfo = gameInfo

	def UpdateWithProjections(self, row):
		self.team = row[3]
		self.p_games = float(row[5])
		self.p_mg = float(row[6])
		self.p_ppg = float(row[7])
		self.p_threespg = float(row[8])
		self.p_rpg = float(row[9])
		self.p_apg = float(row[10])
		self.p_spg = float(row[11])
		self.p_bpg = float(row[12])
		self.p_topg = float(row[13])
		self.p_ddpg = float(row[14])
		self.p_tdpg = float(row[15])

	def CalculateProjectedPoints(self):
		self.points = (1 * self.p_ppg +
						.5 * self.p_threespg +
						1.25 * self.p_rpg +
						1.5 * self.p_apg + 
						2 * self.p_spg + 
						2 * self.p_bpg -
						.5 * self.p_topg + 
						1.5 * self.p_ddpg + 
						3 * self.p_tdpg)
		self.value = self.points/self.salary

	# def calculatePoints(self):
	# 	self.points = 	1 * self.ppg +
	# 					.5 * self.threes +
	# 					1.25 * self.rebounds +
	# 					1.5 * self.assists + 
	# 					2 * self.steals + 
	# 					2 * self.blocks -
	# 					.5 * self.turnovers + 
	# 					1.5 * self.doubleDoubles + 
	# 					3 * self.tripleDoubles

def _():
	players = set()
	with open('DKSalaries.csv', 'r') as f:
		# data = [row for row in csv.reader(f.read().splitlines())]
		for row in csv.reader(f.read().splitlines()):
			if row[1] == 'Name':
				continue
			players.add(Player(row[0], row[1], row[2], row[3]))
	league = League(players)

	# TODO(sherlihy) named tuple unpacking
	with open('pandaProjections.csv', 'r') as f:
		# Data = namedtuple("Data", next(reader))
		for row in csv.reader(f.read().splitlines()):
			# print row
			name = row[1]
			if name == "Name":
				continue
			player = league.GetPlayer(name)
			if player is not None: # Player plays tonight
				player.UpdateWithProjections(row)
				player.CalculateProjectedPoints()

	rankingsQueue = RankingsQueue(league)
	# rankingsQueue.SortPlayers()
	# rankingsQueue.GetRankings()
	return rankingsQueue.GetPlayers() 
