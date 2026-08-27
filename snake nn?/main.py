import pygame as py
import random
#model stuff
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
import numpy
resolution = (740,440)
if not hasattr(torch, "uint64"):
    torch.uint64 = torch.long

if not hasattr(torch, "uint32"):
    torch.uint32 = torch.int

if not hasattr(torch, "uint16"):
    torch.uint16 = torch.short
from sklearn.model_selection import train_test_split
length = 0

x = 30; y = 30
def get_length(listt):
	length = len(listt)
	return length
class Model (nn.Module):
	def __init__(self,in_features=7,h1=32,h2=32,h3=32,out_features=4):
		super().__init__()
		print(f"\033[1;31mBrain Size: {in_features+h1+h2+h3+out_features}\033[0m")
		self.fc1 = nn.Linear(in_features,h1)
		self.fc2 = nn.Linear(h1,h2)
		self.fc3 = nn.Linear(h2,h3)
		self.fc4 = nn.Linear(h3,out_features)
	def forward(self, x):
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = F.relu(self.fc3(x))
		x = self.fc4(x)
		return x
model = Model(in_features=343,out_features=4)
optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
torch.manual_seed(41)
games = 500000
#model stuff
py.init()
clock = py.time.Clock()
screen = py.display.set_mode((resolution[0],resolution[1]))
py.display.set_caption("Snake with Neural Network test")
class Snake:
	def __init__(self,gridX,gridY):
		self.gridSize = (gridX,gridY)
		self.width = int(resolution[0]/gridX)
		self.height = int(resolution[1]/gridY)
		self.display = (resolution[0]/gridX,resolution[1]/gridY)
		self.food = [0,0]
		self.score = 0
		self.player = [self.width/2,self.height/2]
		self.snake = []
		self.snake.append(self.player)
		self.create_food_position()
		self.direction = [0,0]
	def create_food_position(self):
		foodX = random.randint(0,self.width)
		foodY = random.randint(0,self.height)
		self.food[0] = foodX
		self.food[1] = foodY
	def food_collision(self):
		if self.player[0] ==  self.food[0] and self.player[1] == self.food[1]:
			self.create_food_position()
			self.score += 1
			self.snake.append([self.player[0]-self.direction[0],self.player[1]-self.direction[1]])
	def snake_collision(self):
		for i in range(1,len(self.snake)):
			if self.snake[i][0] == self.player[0] and self.snake[i][1] == self.player[1]:
				return True
		if self.player[0] > self.width or self.player[0] < 0:
			return True
		if self.player[1] > self.height or self.player[1] < 0:
			return True
		return False
	def update_game(self):
		for i in reversed(range(1,len(self.snake))):
			self.snake[i][0] = self.snake[i-1][0]
			self.snake[i][1] = self.snake[i-1][1]
		keys = py.key.get_pressed()
		if keys[py.K_w] and self.direction[1] != 1:
			self.direction = [0,-1]
		elif keys[py.K_s] and self.direction[1] != -1:
			self.direction =[0,1]
		elif keys[py.K_d] and self.direction[0] != -1:
			self.direction = [1,0]
		elif keys[py.K_a] and self.direction[0] != 1:
			self.direction = [-1,0]
		self.player[0] += self.direction[0]
		self.player[1] += self.direction[1]
		self.food_collision()
		dead = self.snake_collision()
		if dead is True:
			#print(f"died. Score was: {self.score}")
			return True
	def display_game(self):
		gs = (self.gridSize[0],self.gridSize[1])
		py.draw.rect(screen,(255,0,0),(self.food[0]*gs[0],self.food[1]*gs[1],gs[0],gs[1]))
		for i in range(len(self.snake)):
			py.draw.rect(screen,(0,255,0),(self.snake[i][0]*gs[0],self.snake[i][1]*gs[1],gs[0],gs[1]))
	def compute_direction_from_NN(self,dir):
		if dir == 0 and dir != 2:
			self.direction = [0,-1]
		elif dir == 2 and dir != 0:
			self.direction =[0,1]
		elif dir == 3 and dir != 1:
			self.direction = [1,0]
		elif dir == 1 and dir != 3:
			self.direction = [-1,0]


game = Snake(x,y)
#okay, what the hell do i do?
speed = 10000
interval = 0
game_over = False
best_score = 0
average_of_ten = 0
best_game = 0
scores = []
for i in range(games):
	#please help me
	interval += 1
	training_game = Snake(x,y)
	log_probs = []
	rewards = []
	prev_score = 0
	loss = 0
	reward = 0
	game_over = False
	pdistance = 100000
	frames = 0
	while game_over is False:
		frames += 1
		get_length
		clock.tick(speed)
		py.event.get()
		keys = py.key.get_pressed()
		if keys[py.K_c]:
			speed = 60
			screen.fill((0,0,0))
			training_game.display_game()
			py.display.flip()
		else:
			speed = 10000
		dead = training_game.update_game()
		dx = max(training_game.food[0], training_game.player[0]) - min(training_game.food[0], training_game.player[0])
		dy = max(training_game.food[1], training_game.player[1]) - min(training_game.food[1], training_game.player[1])
		distance = abs(dx) + abs(dy)
		reward = 0
		deadThing = 0
		if dead is True:
			deadThing = 1
		else:
			deadThing = 0
		tempo_grid = []
		for localY in range(int(resolution[1]/y)):
		    row = []
		    for localX in range(int(resolution[0]/x)):
		        if training_game.food[0] == localX and training_game.food[1] == localY:
		            row.append(1.0)
		        elif any(segment[0] == localX and segment[1] == localY for segment in training_game.snake):
		            row.append(0.5)
		        else:
		            row.append(0.0)
		    tempo_grid.append(row)
		flat_map = [cell for row in tempo_grid for cell in row]
		scaled_foodX = round(training_game.food[0]/(resolution[0]/x),1)
		scaled_foodY = round(training_game.food[1]/(resolution[1]/y),1)
		scaled_playerX = round(training_game.player[0]/(resolution[0]/x),1)
		scaled_playerY = round(training_game.player[1]/(resolution[1]/y),1)
		state = [scaled_playerX,scaled_playerY,scaled_foodX,scaled_foodY,dx,dy,deadThing] + flat_map
		state_ten = torch.FloatTensor(state)
		thing = model(state_ten)
		dist = Categorical(logits=thing)
		action = dist.sample()
		training_game.compute_direction_from_NN(action.item())
		if training_game.score > prev_score:
			prev_score = training_game.score
			reward = 100
			frames = 0
		elif dead is True:
			reward = -10
			game_over = True
		elif distance < pdistance:
			reward = 1
		elif frames >= 200:
			reward = -40
			game_over = True
		else:
			reward = -0.01
		log_prob = dist.log_prob(action)
		log_probs.append(log_prob)
		rewards.append(reward)
		pdistance = distance
		if training_game.score > best_score:
			best_score = training_game.score
			best_game = i
	scores.append(prev_score)
	if interval >= 10:
		a = 0
		for i in range(len(scores)):
			a += scores[i]
		average_of_ten = a/(len(scores)+1)
		interval = 0
		scores = []
	gamma = 0.9
	G = 0
	discounted_rewards = []
	for r in reversed(rewards):
	    G = r + gamma * G
	    discounted_rewards.insert(0, G)

	discounted_rewards = torch.FloatTensor(discounted_rewards)
	discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)
	loss = 0
	for log_prob, G in zip(log_probs, discounted_rewards):
	    loss += -log_prob * G

	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	print(f"\r\033[1;34mScore was: {prev_score}. Generation is: {i}. Best score is: {best_score}. Best game was at Game: {best_game}. Previous Interval AO10: {average_of_ten}",end="")

#here
input(f"\033[1;32mFinished training... \033[0m")
while True:
	clock.tick(10)
	screen.fill((0,0,0))
	for event in py.event.get():
		if event.type == py.QUIT:
			py.quit()
			exit()

	death = game.update_game()
	game.display_game()
	py.display.flip()
	if death is True:
		game = Snake(x,y)