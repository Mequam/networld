import menu
import GramGen
#import make_node
import entity
import pickle
import parse
#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def game(partyname):
	#load the grid and the partyname
	grid_arr = parse.loadArr('saves/grid.pkl')
	if not grid_arr:
		#we need to make cultures and then populate the world with cities
		print('[main menu] GENERATING THE GRID *^*')	
	entity_arr = parse.loadArr('saves/entity.pkl')
	if entity_arr:
		print('no entities found, eh')
		entity_arr = []

	party = entity.Party().load('saves/parties/'+partyname + '.pkl')
	
	@menu.menu('networld')
	def game_menu(inputs):
		split_i = inputs.split(' ')
		#this is where we actualy runn the game
		if split_i[0] == 'listMembers':
			for player in party.players:
				print(player.name)
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
