import menu
import GramGen
import make_node
import entity
import pickle
def selectPrompt(prompt,options):
	i = input(prompt)
	while i not in options:
		i = input('('+GramGen.squish(options,'/')+')> ')
	return i

def loadArr(filename):
	try:
		f = open(filename,'rb')
		arr = pickle.load(f)
		f.close()
		return arr
	except:
		return False
def saveArr(arr,filename):
	try:
		f = open(filename,'wb')
		pickle.dump(arr,f,pickle.HIGHEST_PROTOCOL)
		f.close()
		return True
	except:
		return False

#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def game(partyname):
	#load the grid and the partyname
	grid_arr = loadArr('saves/grid.pkl')
	if not grid_arr:
		print('GENERATE THE GRID *^*')	
	entity_arr = loadArr('saves/entity.pkl')
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
	saveArr(grid_arr,'saves/grid.pkl')
	saveArr(entity_arr,'saves/entity.pkl')	
@menu.menu('main menu')
def main(inputs):
	split_i = inputs.split(' ')
	if split_i[0].lower() == 'h':
		print('[main menu] list of commands')
		print('\t"start"		start a new game')
		print('\t"party"   		enter the the party management menu')
		print('\t"q"       		exit the game')
	elif split_i[0] == 'start':
		
		i = selectPrompt('[main menu] are you sure that you would like to start a new party?\n(y/n)> ',['y','n'])
		if i == 'y':
			#the user wants to start a new party, so prompt them for the desired information
			p = entity.Party(input('what should the parties name be?\n(name)> '))
			inp = selectPrompt('[main menu] are you sure thats what you want the parties name to be?\n(y/n)> ',['y','n'])
			while inp != 'y':
				p = entity.Party(input('what should the parties name be?\n(name)> '))
				inp = selectPrompt('[main menu] are you sure thats what you want the parties name to be?(y/n)> \n(y/n)',['y','n'])
			print('[main menu] set party name to ' + p.name)
			print('\n[main menu] now we add players to the party!')
			while True:
				charic = entity.Player()
				charic.prompt()
				p.addPlayer(charic)
				if selectPrompt('[main menu] want to stop making charicters?\n(y/n)> ',['y','n']) == 'y':
					break
			print('[main menu] saving the party!')
			try:
				p.save('saves/parties/'+p.name)
			except:
				print('[main menu] OH NO, unable to save the party :(')	
	elif split_i[0] == 'party':
		party()
	else:
		return False
	return True
print('[*] welcome to networld, at any time type \'?\' for a list of commands')
main()	
