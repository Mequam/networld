import menu
import GramGen
#import make_node
import entity
import pickle
import parse
#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def game(partyname):
	
	#the grid array represents any entity not on the same node as the players
	#load the grid and the partyname
	grid_arr = parse.loadArr('saves/grid.pkl')
	if not grid_arr:
		#we need to make cultures and then populate the world with cities
		print('[*] GENERATING THE GRID *^*')	
	
	#the entity array represents entities in the same cords as the players
	entity_arr = parse.loadArr('saves/entity.pkl')
	if entity_arr:
		print('no entities found, eh')
		entity_arr = []

	party = entity.Party().load('saves/parties/'+partyname + '.pkl')

	#this is how much longer the party has until it can move OUT of the node that it currently finds itself in
	speed = 0

	#this variable stores the node that the party is currently at, so that way we dont have to re-compute the node EVERY
	#time we need to access a variable inside of it


	node = make_node.node(1,1)

	@menu.menu('networld')
	def game_menu(inputs):
		split_i = inputs.split(' ')
		
		#this is where we actualy runn the game
		if split_i[0] == 'list members':
			for player in party.players:
				print(player.name)
		if split_i[0] in ['w','a','s','d']:
			#the players want to leave the node that they are in!
			#each node has a size, decriment the players speed var
			if speed == 0:
				#TODO:make a movement function that takes wasd as inputs and spits out
				#really directions as outputs
				if split_i[0] == 'w':
					party.move(0,1)
				elif split_i[0] == 'a':
					party.move(-1,0)
				elif split_i[0] == 's':
					party.move(0,-1)
				elif split_i[0] == 'd':
					#this could be an else statement, but were going to leave it as elif for readability
					party.move(1,0)
			else:
				#their speed is non zero, so decriment it
				#this needs to describe the new enviorment that they will be walking into
				node.desc()

	#exit the main loop of the game
	parse.saveArr(grid_arr,'saves/grid.pkl')
	parse.saveArr(entity_arr,'saves/entity.pkl')	

@menu.menu('main menu')
def main(inputs):
	split_i = inputs.split(' ')
	if split_i[0].lower() == 'h':
		print('[main menu] list of commands')
		print('\t"start"		start a new game')
		print('\t"party"   		enter the the party management menu')
		print('\t"q"       		exit the game')
	elif split_i[0] == 'start':
		i = parse.selectPrompt('[main menu] are you sure that you would like to start a new party?\n(y/n)> ',['y','n'])
		if i == 'y':
			p = entity.Party()
			p.prompt()
	elif split_i[0] == 'party':
		party()
	else:
		return False
	return True
print('[*] welcome to networld, at any time type \'?\' for a list of commands')
main()	
