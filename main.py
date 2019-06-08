import menu
import GramGen
import make_node
import entity

#we need to select random nodes to spawn nests

#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def game():
	#this is an array containing entities that exist at any point inside of the grid
	grid_arr = []
	#this is an array containing entities that are in the same node as the party
	entity_arr = []
	
	@menu.menu('networld')
	def game_menu(inputs):
		split_i = inputs.split(' ')
		#this is where we actualy runn the game
@menu.menu('main menu')
def main(inputs):
	split_i = inputs.split(' ')
	if split_i[0].lower() == 'h':
		print('[main menu] list of commands')
		print('\t"start"   enter the game world')
		print('\t"party"   enter the the party management menu')
		print('\t"q"       exit the game')
	elif split_i[0] == 'start':
		game()
	elif split_i[0] == 'party':
		party()
	else:
		return False
	return True
print('[*] welcome to networld, at any time type \'?\' for a list of commands')
main()	
