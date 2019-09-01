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
from cdice import parse as parseDice

#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def updateArr(grid_arr,entity_arr,player):	
	appended = 0
	i = 0		
	while i < len(entity_arr):	
		if entity_arr[i].x != player.x or entity_arr[i].y != player.y:
			#somthing in the entity array is not on the same grid as the players, move it to the other array
			grid_arr.append(entity_arr[i])
			del entity_arr[i]
			appended += 1
		else:
			#only incriment i if we do NOT want to remove an entity from the current node
			i += 1	
	if len(grid_arr)-appended <= 0:
		#theres nothing to update in the grid_array, we can skip out on a for loop!
		#actualy we have to or the while loop after this check would go on forever
		return True	
	#theres no need to check the entities we already appended	
	i = 0
	while i < len(grid_arr)-appended:	
		if grid_arr[i].x == player.x and grid_arr[i].y == player.y:
			print('[*] found a matching entity!')
			entity_arr.append(grid_arr[i])
			#remove the entity from the grid array after placing it into the entity array
			del grid_arr[i]
		else:
			i += 1	
	return True
def masterUpdateArrs(player):	
	updateArr(Entity.Town.ga,Entity.Town.ea,player)	
	updateArr(Entity.Bieng.ga,Entity.Bieng.ea,player)

def game(partyname):	
	#the grid array represents any entity not on the same node as the players
	#load the grid and the partyname
	cultures = parse.loadArr('saves/cultures.pkl')
	if not cultures:
		random.seed(get_mac())
		print('[*] generating cultures!')
		cultures = []
		for i in range(2,5):
			cultures.append(Entity.Culture())
		#this array should only be written to once, so we dont save it later in generation
		parse.saveArr(cultures,'saves/cultures.pkl')
	
	#grid_array will now represent an array of arrays, each of those arrays representing a different type of entity
	grid_arr = parse.loadArr('saves/grid.pkl')
	if grid_arr:
		#load how many of each entity exists from the array into their shared variables
		for arr in grid_arr:
			if len(arr) > 0:
				if type(arr[0]) == Entity.Town:
					Entity.Town.ga = arr
					Entity.Town.count = len(arr)
				elif type(arr[0]) == Entity.Bieng:
					Entity.Bieng.ga = arr 
				
	else:
		#we need to make cultures and then populate the world with cities
		print('[*] GENERATING THE GRID *^*')	
		grid_arr = []
		offset = 1

		random.seed(get_mac())
		for culture in cultures:
			Entity.Town(culture,random.randrange(1,21),random.randrange(1,21))
		
		#load the individual entity type grid arrays into the main grid array
		grid_arr.append(Entity.Town.ga)
		grid_arr.append(Entity.Bieng.ga)
	
	#the entity array represents entities in the same cords as the players
	entity_arr = parse.loadArr('saves/entity.pkl')
	if not entity_arr:
		print('[*] no entities found, eh')
		entity_arr = [Entity.Town.ea,Entity.Bieng.ea]
	else:
		for arr in entity_arr:
			if len(arr) > 0:
				if type(arr[0]) == Entity.Town:
					Entity.Town.ea = arr
					Entity.Town.count += len(arr)
				elif type(arr[0]) == Entity.Bieng:
					Entity.Bieng.ea = arr

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
		if split_i[0] == 'roll':
			if len(split_i) > 1:
				try:
					print('[networld] ' + str(parseDice(split_i[1])))
				except:
					print('[networld: ERROR] invalid dice expresion!')
			else:
				print('[networld: ERROR] dice expresion required')
		elif split_i[0] == 'check':
			if len(split_i) > 2:
				for player in party.players:
					if player.name == split_i[1]:
						print('[*] ' + player.name + ' rolled a ' + str(player.check(split_i[2])))
						break
				else:
					print('[networld: ERROR] player not found!')
			else:
				print('[networld: ERROR] player and stat to check required!')
		elif split_i[0] == 'town':
			if len(split_i) > 1:
				found = False
				for e in Entity.Town.ea:
					if e.name == split_i[1]:
						e.shell(entity_arr,party,cultures)
						found = True
						break
				if not found:
					print('[networld: ERROR] unrecognised town name')
			else:
				print('[networld: ERROR] town name required!')
			
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
				
				#update the arrays containing entities
				masterUpdateArrs(party)
				
				#update entities in the grids node only if the players leave their current node
				for arr in grid_arr:
					i = 0
					while i < len(arr):
						if arr[i].AI(party) == -1:
							del arr[i]
							#avoid incrimenting i when we delete an entity so that way we dont go over the desired index
							continue
						i += 1
			else:
				#we didnt leave the node that we are in, there is a chance that we will spawn an encounter
				#roll for that chance
				if random.randrange(1,101) < 45:
					print('[*] ' + node.enc())
				else:
					print('[*] you move onwards unobscured')
			#update entities in the players node no matter what	
			for arr in entity_arr:
				i = 0
				while i < len(arr):	
					if arr[i].AI(party) == -1:
						del arr[i]
						#dont incriment i as we just removed an entity from the array
						continue
					i += 1
		elif split_i[0] == 'list':
			if len(split_i) > 1:
				if split_i[1] == 'node':
					print(node.toString())
				elif split_i[1] == 'plants':
					print(node.strPlants())
				elif split_i[1] == 'animals':
					print(node.strAnimals())
				elif split_i[1] == 'biome':
					print(node.biome)
				if split_i[1] == 'members':
					print('[networld] listing party members')
					for player in party.players:
						print(player.name)
				if split_i[1] == 'towns':
					print('[networld] listing towns in your node')	
					for town in Entity.Town.ea:	
						print(town.name + ', a ' + town.culture.name + ' town')	
			else:
				print('[networld: ERROR] valid options are: node, plants, animals,biome,members and towns')
		elif split_i[0] == 'combat':
			combat.combat_wrapper(Entity.Bieng.ea+party.players,party,cultures)	
		elif split_i[0] == '?':
			print('[networld] list of valid commands')
			print('\t[w,a,s,d] 			move in the direction of the pointed letter')
			print('\t"list" [target]			list the specified entity')
			print('\t"check" <member> <stat>		run a check against the stat of the current member')
			print('\t"combat"			enter the combat shell')
			print('\t"town" [town]			enter the town of the given name (only works if there are towns in the node)')
			print('\t"save"				save the progress of the grid and current party without closing the game')
			print('\t"roll" <dice expresion>		roll a dice expresion')
			print('\t"q"				exit to the previous menu')
			print('\t"?"				print this list')
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
		
		#TODO: make this an actual thing
		#print('\t"party"   		        enter the the party management menu')
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
