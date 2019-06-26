#this file contains the combat menu and the combat parsing system
import menu
from cdice import parse as parseDice

#command is a split command where each index of the array is a different word in the command
#need to add the dice parser here

def parse_num(word,var_dict):
	if word in var_dict:
		#return the value of the variable in question, but decriment the number of times it can be called
		var_dict[word][1] -= 1
		num = var_dict[word][0]

		if var_dict[word][1] <= 0:
			#they have run out of calls to use the variable, delete it
			del var_dict[word]
			print('[combat] ' + word + ' has run out of calls')
	else:
		try:
			num = parseDice(word)	
		except:	
			return None
	return num
def findBiengIndex(bieng_arr,name):
	for i in range(0,len(bieng_arr)):
		if bieng_arr[i].name == name:
			return i
	return None
	
def parse_target(target,bieng_arr,caster):
	#this function asks the user to target a specific entity using the target criteria
	#basicaly it lets the DM take over
	if target == 'self':
		name = caster
	else:
		print('[combat] who does the player want to target with ' + target + '?')
		print('[combat] if the player cannot target anyone, type n')
		name = input('(combat) name to target > ')
		while name == 'l':
			for bieng in bieng_arr:
				print(bieng.name)
			name = input('(combat) name to target > ')
		if name == 'n':
			return None
	return findBiengIndex(bieng_arr,name)
#TODO:	need to make a file parser to run through a file and run this function on each line of the file
#that way the players can make their own spells 
def parse_command(command,var_dict,bieng_arr,caster):
	def addStat(string,num,target,bieng_arr):
		#this function takes a string and adds the given number to the correct bieng stat
		if string == 'hp':
			bieng_arr[target].hp += num
			stat = bieng_arr[target].hp
		elif string == 'ac':
			bieng_arr[target].ac += num
			stat = bieng_arr[target].ac
		elif string == 'thaco':
			bieng_arr[target].thaco += num
			stat = bieng_arr[target].thaco
		else:
			try:
				bieng_arr[target].stats[string] += num
				stat = bieng_arr[target].stats[string]
			except:
				#TODO: it might be possible to make the program add a new stat when it detects one that does
				#not already exist
				print('[combat] ERROR: invalid stat detected!')
				return None		
		#alert the user that the bieng has been updated
		print('[combat] set ' + bieng_arr[target].name + ' ' + string + ' to ' + str(stat))
	
	def getTarget(bieng_arr,cmd,caster):
		if cmd != 'self':
			#they are not targeting themselfs
			target = findBiengIndex(bieng_arr,cmd)
			if target == None:
				#they are not targeting anyone else, so run the target routine
				target = parse_target(cmd,bieng_arr,caster)
		else:
			#they want to target themselfs, so set the index to target the caster
			target = findBiengIndex(bieng_arr,caster)
		return target
	
	if command[0] == 'Add':
		#get the number that they want to use in the modifictation
		num = parse_num(command[1],var_dict)
		if num == None:
			print('[combat] ERROR, invalid number!')	
			return None		
		#get the target that they want to use
		target = getTarget(bieng_arr,command[3],caster)
		if target == None:
			#we were given an invalid target
			return None

		#actualy perform the modification of the stat
		addStat(command[4],num,target,bieng_arr)	
	elif command[0] == 'Sub':
		#get the number that they want to use in the modifictation
		num = parse_num(command[1],var_dict)
		if num == None:
			print('[combat] ERROR, invalid number!')	
			return None		
		#get the target that they want to use
		target = getTarget(bieng_arr,command[3],caster)
		if target == None:
			#we were given an invalid target
			return None	
		
		#perform the given operation on the target bieng
		addStat(command[4],-1*num,target,bieng_arr)		
	elif command[0] == 'Adv':
		num = parse_num(command[1],var_dict)
		if num == None:
			return None
		target = getTarget(bieng_arr,command[3],caster)
		if target == None:
			return None
		bieng_arr[target].addAdv(command[4],num)
	elif command[0] == 'Dis':
		num = parse_num(command[1],var_dict)
		if num == None:
			return None
		target = getTarget(bieng_arr,command[3],caster)
		if target == None:
			return None
		bieng_arr[target].addAdv(command[4],-1*num)
	elif command[0] == 'Set':
		num = parse_num(command[3],var_dict)
		if num == None:
			#switch to the target parser
			num = parse_target(command[3],bieng_arr,caster)
			if num == None:
				#they did not give us a valid number or target, complain
				print('[combat] ERROR: invalid target or number')
			else:
				print('[combat] setting ' + command[1] + ' to ' + num.name)
		else:
			print('[combat] setting ' + command[1] + ' to ' + str(num))
		var_dict[command[1]] = [num,int(command[5])]
def checkname(bieng_arr,name):
	for bieng in bieng_arr:
		if bieng.name == name:
			return False
	return True

def combat_wrapper(bieng_arr,party):
	#TODO: figure out a way to make sure that only biengs are contained inside of the bieng arr
	#this function is a wrapper function containing the variables for the combatMenu below it	
	
	#sort the bieng_arr based on initiative
	def keyf(bieng):
		return bieng.check('dex','initiative')
	bieng_arr.sort(key=keyf)
	mod = len(bieng_arr)

	var_dict = {}
	Turn = 0

	print('[command] it is currently ' + bieng_arr[Turn].name + '\'s turn')	
	command = input('(combat)> ').split(' ')
	while command[0] != 'q':	
		if command[0] == 'roll':
			#they want to roll a dice type
			print('[combat] ' + str(parseDice(command[1])))
		elif command[0] == 'check':
			if len(command) > 1:
				check = False
				if command[1] != 'self':
					for bieng in bieng_arr:
						if bieng.name == command[1]:
							roll = bieng.check(command[2:])
							target = bieng
							check = True
							break
				if not check:
					#they did not set the stat to anything, target themselfs
					roll = bieng_arr[Turn].check(command[1:])
					target = bieng_arr[Turn]
			print('[combat] ' + target.name + ' rolled a ' + str(roll))
		elif command[0] == 'ls':	
			for bieng in bieng_arr:
				bieng.ToScreen(command)
				print('-'*40)
		elif command[0] == 'show':
			target = bieng_arr[Turn]
			if len(command) > 1:
				if command[1] != 'self':
					target = bieng_arr[findBiengIndex(bieng_arr,command[1])]
			target.ToScreen(command)
		elif command[0] == 'hit':
			target = bieng_arr[Turn]
			if len(command) > 1:
				if command[1] != 'self':
					target = bieng_arr[findBiengIndex(bieng_arr,command[1])]
			if bieng_arr[Turn].rollHit(target):
				print('[combat] ' + bieng_arr[Turn].name + ' hit ' + target.name + '!')
			else:
				print('[combat] ' + bieng_arr[Turn].name + ' missed')
		elif command[0] == 'act':
			bieng_arr[Turn].actions -= 1
		elif command[0] == 'addAct':
			bieng_arr[Turn].actions += 1
		elif command[0] == 'end':
			#they want to end their turn, so remove all of their actions
			bieng_arr[Turn].actions = 0
		elif command[0] == 'turn':
			print('[command] it is currently ' + bieng_arr[Turn].name + '\'s turn')
		elif command[0] == 'addEntity':
			if len(command) > 1:
				#add an entity of a given level with the optional given name to the bieng_arr
				e = entity.Bieng(party.x,party.y,int(command[1]))
				if len(command) > 2:
					#they gave us a name, load it
					name = command[2]
				else:
					#they did not give us a valid name so default to unamed
					name = 'unamed'
				num = 0
				testname = name
				#make sure that the name we want to use does not exist
				#and if it does add a number after it
				while not checkname(bieng_arr,testname):
					num += 1
					testname = name + str(num)
				e.name = testname
				bieng_arr.append(e)	
			else:
				print('[combat] ERROR: entity level required!')
		elif command[0] == 'removeEntity':
			if len(command) > 1:
				print(command[1])
				print('[Debug] alive')
				for i in range(0,len(bieng_arr)):
					if bieng_arr[i].name == command[1]:
						print('[combat] ' + bieng.name + ' dropped a spell fragment: ' + bieng_arr[i].loot())
						del bieng_arr[i]
						#make sure that turn does not point outside of the array
						Turn = Turn % len(bieng_arr)
						#exit the for loop
						break
		else:
			parse_command(command,var_dict,bieng_arr,bieng_arr[Turn].name)
		#this is where you would run the token system for the bieng that is currently on
		if bieng_arr[Turn].actions <= 0:
			#reset their actions and incriment the turn clock
			bieng_arr[Turn].actions = 2
			Turn = (Turn + 1) % len(bieng_arr)
			print('[command] ending the turn!')
			print('-'*30)	
			print('[command] it is currently ' + bieng_arr[Turn].name + '\'s turn')		
		command = input('(combat)> ').split(' ')				
		
#Dis [num] to [target] {sub check && ! tag ind:state}
#Adv [num] to [target] {sub check && ! tag ind:state}
#Sub [num] from [target] {sub check && ! tag specif:state}
#Add [num] to [target] {sub check && ! tag specif:state}
#Set {tag letter:state} to [target/num] for (number) calls
#Roll [dice]
#Add token [token] to [target]
#Hack [target program]
#Token (number) statements
if __name__ == '__main__':
	print(parseDice('1d20'))
	import entity
	a = entity.Bieng(2,2,2)
	a.name = 'Rex'
	b = entity.Bieng(2,2,2)
	b.name = 'test'
	arr = [a,b]	
	combat_wrapper(arr,entity.Party())
#TargetLineRange
#TargetRadiusRange
#TargetEyeContact
#TargetTouch
#TargetSight
#TargetPuncture
#TargetThrough {sub material:noun}
#TargetLine
