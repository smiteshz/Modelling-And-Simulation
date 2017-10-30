import numpy as np
import time
# Global Arrays
# Available_Cars [cars_object]
# Cars Object:
# car_index=a,car_capacity=passengers,current_position=[x,y],available=True/False
INDEX = 0
PINDEX = 0
P_CAP = [0.05,0.05,0.4,0.3,0.15,0.05]
P_MEM = [0.6,0.25,0.1,0.05]
DROP_P = [0.015625,0.015625,0.015625,0.1875,0.015625,0.015625,0.015625,0.1875,0.015625,0.015625,0.015625,0.1875,0.015625,0.015625,0.015625,0.1875,0.015625,0.015625,0.015625,0.015625]
Time = 0
av_cars = list()
use_cars = list()
EL = list(list())
HEAD = 0
TYPE = ["CAR","PASSENGER","ENVIRONMENT"]
def search (cen,rad):
	positions = list(list())
	position = list()
	flag = True
	i = 0
	while(i<=rad):
		#print(i)
		#Itself
		if(i==0):
			position.append(cen[0])
			position.append(cen[1])
			positions.append(position)
			position = list()
			i+=1
			continue
		#Top
		if(cen[1]+i<=19):
			position.append(cen[0])
			position.append(cen[1]+i)
			positions.append(position)
			position = list()
		#Bottom
		if(cen[1]-i>=0):
			position.append(cen[0])
			position.append(cen[1]-i)
			positions.append(position)
			position = list()
		#Left
		if(cen[0]-i>=0):
			position.append(cen[0]-i)
			position.append(cen[1])
			positions.append(position)
			position = list()
		if(cen[0]+1<=19):
		#Right
			position.append(cen[0]+i)
			position.append(cen[1])
			positions.append(position)
			position = list()
		if(cen[0]+i<=19 and cen[1]+i<=19):	
		#Top-Right
			position.append(cen[0]+i)
			position.append(cen[1]+i)
			positions.append(position)
			position = list()
		if(cen[0]-i>=0 and cen[1]+i<=19):
		#Top-Left
			position.append(cen[0]-i)
			position.append(cen[1]+i)
			positions.append(position)
			position = list()
		if(cen[0]-i>=0 and cen[1]-i>=0):
		#Bottom-Left
			position.append(cen[0]-i)
			position.append(cen[1]-i)
			positions.append(position)
			position = list()
		if(cen[0]+i<=19 and cen[1]-i>=0):
		#Bottom-Right
			position.append(cen[0]+i)
			position.append(cen[1]-i)
			positions.append(position)
			position = list()
		#print(i)
		i+=1
	return (positions)
class Car:
	def __init__(self):
		global INDEX,P_CAP
		self.type = "CAR"
		self.id=INDEX+1
		self.capacity= 6#np.random.choice(np.array([1,2,3,4,5,6]),p=P_CAP)
		self.position = np.array([np.random.choice(np.arange(1,21)),np.random.choice(np.arange(1,21))])
		self.arrive = 0
		self.threshold = 7200
		self.available = True
		self.occupants = np.array([])
		INDEX = INDEX + 1
		return

	def drive(self,destination,clock=0):
		while(self.position[0]!=destination[0] or self.position[1]!=destination[1]):
			if(destination[0]<self.position[0]):
				self.position[0]-=1
			elif(destination[0]>self.position[0]):
				self.position[0]+=1
			if(destination[1]>self.position[1]):
				self.position+=1
			elif(destination[1]<self.position[1]):
				self.position[1]-=1
		return

	def pickup(passenger):
		np.append(self.occupants,passenger.index)
		self.capacity = self.capacity-passenger.member
		if(passenger.carpool):
			self.available = True
		else:
			self.available = False
		return

class Passenger:
	def __init__(self,arrival):
		global PINDEX 
		self.type = "PASSENGER"
		self.id = PINDEX+1
		self.member = np.random.choice(np.array([1,2,3,4]),p=P_MEM)
		if(self.member == 1):
			self.carpool = np.random.choice([True,False])
		elif(self.member == 2):
			self.carpool = np.random.choice([True,False],p=[0.65,0.35])
		elif(self.member == 3):
			self.carpool = np.random.choice([True,False],p=[0.45,0.55])
		else:
			self.carpool = np.random.choice([True,False],p=[0.30,0.70])
		self.start_position = np.array([np.random.choice(np.arange(1,21)),np.random.choice(np.arange(1,21))])
		self.end_position = np.array([np.random.choice(np.arange(1,21)),np.random.choice(np.arange(1,21),p=DROP_P)])
		self.driver = None
		self.arrival = arrival
		self.threshold = 900+arrival
		return

class Environment:
	def __init__(self):
		self.GRID = np.zeros([20,20])


	def find_available_cars(self,passenger):
		car_found = False
		search_center = passenger.start_position
		print("Start Position = ",search_center)
		radius = 0
		search_list = list()
		carlist = list()
		while(car_found == False and radius<=20):
			search_list = search(search_center,radius)
			for i in search_list:
				for j in av_cars:
					if(i[0]==j.position[0] and i[1]==j.position[1]): #and j.capacity>=passenger.member):
						car_found = True
						carlist.append(j)
			radius += 1
		return(carlist)

def setup():
	global Time,av_cars,use_cars,EL
	N_CARS = 5#int(input("Enter the number of Cars in the System:"))
	for i in range(N_CARS):
		av_cars.append(Car())
	trigger = np.array([1])
	while(trigger[-1]<7200):
		trigger = np.append(trigger,trigger[-1]+int(np.random.exponential(scale=30)+1))
	trigger = np.delete(trigger,obj = -1)
	trigger = np.delete(trigger,obj = 0)
	for i in trigger:
		a = Passenger(i)
		EL.append([i,a])
	env = Environment()
	for i in av_cars:
		 print(i.position)
	print(env.find_available_cars(Passenger(1)))
	# print(EL)

def run():
	global Time,av_cars,use_cars,HEAD,EL
	Time +=1
	"""For Every every time increment check if we have something in the Future Event List.
	The format of the Future Event List will be [[Object_Type,Object_ID,Arrival_Time]]"""
	if(HEAD<len(EL) and Time == EL[HEAD][0]):
		pass


setup()
# while(True):
# 	if (Time > 7200):
# 		break
# 	run()
# print("Time = ",Time)
# print("Head = ",HEAD)
#Events
# Spawn Passenger <Dynamic, continously called thru the mainloop>
# 	The passenger will have a spawnpoint at a random location and will also have a destination point sampled
# 	Spawn Passenger will call the Reservation Event for which the area around him will be searched for 
#   any available cars. 
#
#
#
# Spawn Cars <Spawn x amount of cars at random location on the map>
# 