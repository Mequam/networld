#TODO:need to make an inventory system for the players
#TODO:need to add more entities to the game that can spawn
#TODO:need to work on the network aspect of the game and allow for pcs to travel computers
#TODO:need to work on the corruption
import random
import menu
import GramGen
import make_node
import entity as Entity
import pickle
import parse
import combat
from math import floor
from uuid import getnode as get_mac

#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def updateArrs(grid_arr,entity_arr,player):
	try:
		appended = 0
		for i in range(0,len(entity_arr)):
			if entity_arr[i].x != player.x and entity_arr[i].y != player.y:
				#somthing in the entity array is not on the same grid as the players, move it to the other array
				grid_arr.append(entity_arr[i])
				del entity_arr[i]
				appended += 1	
		for i in range(0,len(grid_arr)-appended):	
			if grid_arr[i].x == player.x and grid_arr[i].y == player.y:
				print('[*] found a matching entity!')
				entity_arr.append(grid_arr[i])
				#remove the entity from the grid array after placing it into the entity array
				del grid_arr[i]
		return True
	except:
		return False	
def game(partyname):	
	#the grid array represents any entity not on the same node as the players
	#load the grid and the partyname
	grid_arr = parse.loadArr('saves/grid.pkl')
	if not grid_arr:
		#we need to make cultures and then populate the world with cities
		print('[*] GENERATING THE GRID *^*')	
		grid_arr = []
		offset = 1

		random.seed(get_mac())
		cultures = []
		for i in range(2,5):
			cultures.append(Entity.Culture())
		for culture in cultures:
			grid_arr.append(Entity.Town(culture,random.randrange(1,21),random.randrange(1,21)))
		#for town in grid_arr:
		#	print('[*] Town at ' + str(town.x) + ' ' + str(town.y))
	
	#the entity array represents entities in the same cords as the players
	entity_arr = parse.loadArr('saves/entity.pkl')
	if not entity_arr:
		print('[*] no entities found, eh')
		entity_arr = []

	party = Entity.Party() 
	party.load('saves/parties/'+partyname + '.pkl')


	#this variable stores the node that the party is currently at, so that way we dont have to re-compute the node EVERY
	#time we need to access a variable inside of it


	node = make_node.node(party.x,party.y)

	inputs = 'blah'
	while inputs != 'q':
		inputs = input('(networld)> ')
		if inputs == 'l':
			inputs = last
		else:
			last = inputs
		
		split_i = inputs.split(' ')
		
		#this is where we actualy runn the game
		if split_i[0] == 'list' and len(split_i) > 1:
			if split_i[1] == 'members':
				print('[networld] listing party members')
				for player in party.players:
					print(player.name)
			if split_i[1] == 'towns':
				print('[networld] listing towns in your node')	
				for e in entity_arr:	
					if type(e) is Entity.Town:
						print(e.name + ', a ' + e.culture.name + ' town')
		elif split_i[0] == 'town':
			if len(split_i) > 1:
				found = False
				for e in entity_arr:
					if type(e) == Entity.Town and e.name == split_i[1]:
						e.shell(entity_arr,party)
						found = True
						break
				if not found:
					print('[networld] ERROR: unrecognised town name')
			else:
				print('[networld] ERROR: town name required!')
						
			
		elif split_i[0] in ['w','a','s','d']:	
			#TODO:make a movement function that takes wasd as inputs and spits out
			#really directions as outputs
			if split_i[0] == 'w':
				party.suby += 1
			elif split_i[0] == 'a':
				party.subx -= 1
			elif split_i[0] == 's':
				party.suby -= 1
			elif split_i[0] == 'd':
				#this could be an else statement, but were going to leave it as elif for readability
				party.subx += 1
			
			#they have performed a movement action, now see if that action is enough to move them out of the node that
			#they are in
			moved = False
			if party.subx > node.size[0]:
				moved = party.move(1,0,True)	
			elif party.subx < 0:
				moved = party.move(-1,0,True)
			elif party.suby > node.size[1]:
				moved = party.move(0,1,True)
			elif party.suby < 0:
				moved = party.move(0,-1,True)
			if moved:
				#first update the loaded node
				node = make_node.node(party.x,party.y)
				print('[networld] leaving node!')
				print('[*] ' + node.desc())
				#set the parties sub x and y to the middle of that node
				party.suby = floor(node.size[1]/2)
				party.subx = floor(node.size[0]/2)
				
				#update the entity arrays to load all of the entities from the grid array that match the players current poss
				#are loaded correctly
				updateArrs(grid_arr,entity_arr,party)

				#update entitiys in the grids node only if the players leave their current node
				i = 0
				while i < len(grid_arr):
					spawn = grid_arr[i].AI(party)
					#if spawn == -1:
					#	del grid_arr[i]
						#avoid incrimenting i when we delete an entity so that way we dont go over the desired index
					#	continue
					#elif spawn != None:
					#	grid_arr.append(spawn)
					i += 1
			else:
				#we didnt leave the node that we are in, there is a chance that we will spawn an encounter
				#roll for that chance
				if random.randrange(1,101) < 45:
					print('[*] ' + node.enc())
				else:
					print('[*] you move onwards unobscured')
			#update entities in the players node no matter what	
			for i in range(0,len(entity_arr)):
				spawn = entity_arr[i].AI(party)
				if spawn == -1:
					del entity_arr[i]
				elif spawn != None:
					entity_arr.append(spawn)
		elif split_i[0] == 'show' and len(split_i) > 1:
			if split_i[1] == 'all':
				print(node.toString())
			elif split_i[1] == 'plants':
				print(node.strPlants())
			elif split_i[1] == 'animals':
				print(node.strAnimals())
			elif split_i[1] == 'biome':
				print(node.biome)
		elif split_i[0] == 'tp' and len(split_i) > 2:
			#this command is for development ONLY
			try:
				party.x = int(split_i[1])
				party.y = int(split_i[2])
				node = make_node.node(party.x,party.y)
				print(node.desc())
			except:
				return False
		elif split_i[0] == 'combat':
			#load all of the entites that are on the parties current grid and are biengs
			#into the bieng arr, as well as all of the players
			bieng_arr = []
			for entity in entity_arr:
				if type(entity) is Entity.Bieng:
					bieng_arr.append(Bieng)
			for player in party.players:	
				bieng_arr.append(player)
			#send the party and the loaded bieng array to the combat menu
			combat.combat_wrapper(bieng_arr,party,cultures)	
		elif split_i[0] == 'save':
			#save everything!!!
			print('[networld] saving!')
			party.save()
			if not parse.saveArr(entity_arr,'saves/entity.pkl'):
				print('[networld: ERROR] could not save the entity array!')
			if not parse.saveArr(grid_arr,'saves/grid.pkl'):
				print('[networld: ERROR] could not save the grid array!')	
	print('[networld] saving and exiting to the main menu!')
	party.save()
	parse.saveArr(entity_arr,'saves/entity.pkl')
	parse.saveArr(grid_arr,'saves/grid.pkl')	
	return True
		
@menu.menu('main menu')
def main(inputs):
	split_i = inputs.split(' ')
	if split_i[0].lower() == '?':
		print('[main menu] list of commands')
		print('\t"start" [party name]		start the game as the given party')
		print('\t"party"   		        enter the the party management menu')
		print('\t"q"       			exit the game')
		print('\t"new"				start a new party')
	elif split_i[0] == 'new':
		i = parse.selectPrompt('[main menu] are you sure that you would like to start a new party?\n(y/n)> ',['y','n'])
		if i == 'y':
			p = Entity.Party()
			p.prompt()
	elif split_i[0] == 'party':
		#need to work on this input
		party()
	elif len(split_i) > 1 and split_i[0] == 'start':
		game(split_i[1])
	else:
		return False
	return True
print('[*] welcome to networld, at any time type \'?\' for a list of commands')
main()	
