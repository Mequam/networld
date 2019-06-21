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
	else:
		try:
			num = parseDice(word)	
		except:
			print('unable to parse out a number!')	
			return None
	return num
def findBiengIndex(bieng_arr,name):
	for i in range(0,len(bieng_arr)):
		if bieng_arr[i].name == name:
			return i
	print('[combat] ERROR: unable to target ' + name + ', incorrect name')	
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
def addStat(bieng,num,stat):
	if stat == 'str':
		bieng.str += num
		newNum = bieng.str
	elif stat == 'dex':
		bieng.dex += num
		newNum = bieng.dex
	elif stat == 'con':
		bieng.con += num
		newNum = bieng.con
	elif stat == 'int':
		bieng.int += num
		newNum = bieng.int
	elif stat == 'wis':
		bieng.wis += num
		newNum = bieng.wis
	elif stat == 'cha':
		bieng.cha += num
		newNum = bieng.cha
	elif stat == 'ac':
		bieng.ac += num
		newNum = bieng.ac
	elif stat == 'hp':
		bieng.hp += num
		newNum = bieng.hp
	else:
		print('[combat] ERROR: invalid stat!')
		return None
	print('[combat] set ' + bieng.name + ' ' + stat + ' to ' + str(newNum))
	return True	

def parse_command(command,var_dict,bieng_arr,caster):
	if command[0] == 'Add':
		#get the number that they want to use in the modifictation
		num = parse_num(command[1],var_dict)
		if num == None:
			print('[combat] ERROR, invalid number!')	
			return None
		#get the target that they want to use
		target = parse_target(command[3],bieng_arr,caster)
		if target == None:
			return None
		#perform the operation on the bieng
		addStat(bieng_arr[target],num,command[4])		
	elif command[0] == 'Sub':
		num = parse_num(command[1],var_dict)
		if num == None:
			return None
		target = parse_target(command[3],bieng_arr,caster)
		if target == None:
			return None	
		addStat(bieng_arr[target],-1*num,command[4])			
	elif command[0] == 'Adv':
		num = parse_num(command[1],var_dict)
		if num == None:
			return None
		target = parse_target(command[3],bieng_arr,caster)
		if target == None:
			return None
		bieng_arr[target].addAdv(command[4],num)
	elif command[0] == 'Dis':
		num = parse_num(command[1],var_dict)
		if num == None:
			return None
		target = parse_target(command[3],bieng_arr,caster)
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
def combat_wrapper(bieng_arr):
	#TODO: figure out a way to make sure that only biengs are contained inside of the bieng arr
	#this function is a wrapper function containing the variables for the combatMenu below it	
	
	#sort the bieng_arr based on initiative
	def keyf(bieng):
		return bieng.rollDex('initiative')
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
			#they want to make a stat check
			#syntax: check stat [target] [subStat]
			
			#when subStat is None it is ignored by the roll functions, which is why we init it to None
			subStat = None
			#initilise the target to point to the bieng currently taking their turn
			target = bieng_arr[turn]
			
			if len(command) > 2:
				if command[2] != 'self':
					#the self target should refer to the bieng currently taking their turn
					#so dont change it past what we inited it to be
					target = bieng_arr[findBiengIndex(bieng_arr,command[2])]
					if target == None:
						print('[combat] ERROR: not a valid target')
				#only bother checking if its greater than three if we know its greater than 2
				if len(command) > 3:
					subStat = command[3]

				if command[0] == 'str':
					roll = target.rollStr(subStat)
				elif command[0] == 'dex':
					roll = target.rollDex(subStat)
				elif command[0] == 'con':
					roll = target.rollCon(subStat)		
				elif command[0] == 'int':
					roll = target.rollInt(subStat)	
				elif command[0] == 'wis':
					roll = target.rollWis(subStat)
				elif command[0] == 'cha':
					roll = target.rollCha(subStat)
				else:
					print('[combat] ERROR: invalid stat recived!')
				print('[combat] ' + target.name + ' rolled a ' + roll)
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
		else:
			parse_command(command,var_dict,bieng_arr,bieng_arr[Turn].name)
		#this is where you would run the token system for the bieng that is currently on
		if bieng_arr[Turn].actions <= 0:
			#reset their actions and incriment the turn clock
			bieng_arr[Turn].actions = 2
			Turn = (Turn + 1) % mod	
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
	combat_wrapper(arr)
#TargetLineRange
#TargetRadiusRange
#TargetEyeContact
#TargetTouch
#TargetSight
#TargetPuncture
#TargetThrough {sub material:noun}
#TargetLine
