from Agent import Agent
import numpy as np
import random
from Cell2D import Cell2D
import math
from copy import deepcopy

class World(Cell2D):
	"""
	Represents a world of sick and healthy agents.
	"""

	def __init__(self, agent_array=None, **params):

		# Set up world params
		self.n = params.get("n", 10)
		self.num_population = params.get("num_agents", self.n**2)
		self.num_sick = params.get("num_sick", 1)

		# Initialize arrays to track array data
		self.healthy = []
		self.contagious = []
		self.sick = []

		# Set up the agent population
		if agent_array == None:
			# populate agent_array

			self.agent_array = [[None for x in range(self.n)] for y in range(self.n)]

			sick_list = [1 for _ in range(self.num_sick)]
			healthy_list = [0 for _ in range(self.n**2 - self.num_sick)]
			health_shuffle = sick_list + healthy_list
			random.shuffle(health_shuffle)

			for i in range(self.n):
				for j in range(self.n):
					self.agent_array[i][j] = Agent(health=health_shuffle[self.n * i + j])
		else:
			self.agent_array = agent_array

		# Set up occupancy grid to keep track of agent presence
		self.occupancy_grid = np.zeros((self.n, self.n))
		for x in range(self.n):
			for y in range(self.n):
				if self.agent_array[i][j] != None:
					self.occupancy_grid[i][j] = 1

		# Create an agent health visualization array
		self.array = np.zeros((self.n, self.n))
		for i in range(self.n):
			for j in range(self.n):
				self.array[i][j] = self.agent_array[i][j].health + 1
		#print(self.array)



	# Every step represents the change in one hour
	def step(self):

		# Loop through agent objects and update based on params
		new_agent_array = deepcopy(self.agent_array)

		for i in range(self.n):
			for j in range(self.n):
				if self.agent_array[i][j] != None:
					#print("Cell: " + str((i, j)))
					# Get list of neighbors health
					neighbors_health = []
					for a in range(i - 1, i + 2):
						for b in range(j - 1, j + 2):
							if (a, b) != (i, j):
								if a >= 0 and a < self.n and b >= 0 and b < self.n:
									neighbors_health.append(self.agent_array[a][b].health)

					# Get fraction of neighbors that are sick
					np.ceil(neighbors_health)
					neigh_health_frac = sum(neighbors_health) / 8

					# Update agent health
					# If sick (and contagious)
					if self.agent_array[i][j].health > 0.9:
						#print("I was sick")
						if random.randrange(0, 100) == 1:
							new_agent_array[i][j].health = 0

					# If health and contagious
					elif self.agent_array[i][j].health < 1 and self.agent_array[i][j].health > 0:
						#print("I was contagious")
						new_agent_array[i][j].health += 0.1

					# If healthy
					elif self.agent_array[i][j].health == 0:
						immunity = self.agent_array[i][j].immunity*100
						neigh_health_chance = math.floor(neigh_health_frac*100)
						health_chance = random.randrange(neigh_health_chance, 102)

						if neigh_health_chance == 0:
							new_agent_array[i][j].health = 0
						elif health_chance > immunity:
							new_agent_array[i][j].health = 0.1

		self.agent_array = deepcopy(new_agent_array)
		self.update_vis()
		return np.count_nonzero(self.array > 1)


	def update_vis(self):
		for i in range(self.n):
			for j in range(self.n):
				self.array[i][j] = deepcopy(self.agent_array[i][j].health) + 1

		# track numbers for each step
		self.healthy.append(np.count_nonzero(self.array == 1))
		self.contagious.append(np.count_nonzero((self.array > 1) & (self.array < 2)))
		self.sick.append(np.count_nonzero(self.array == 2))
