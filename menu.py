def menu(shellname):
	def decor(code):
		def shell(previous_shell=None,args=None):
            		#alert the user that we are changing shells (or menus)
			print('[*] entering ' + shellname + ', type q to exit')    
			while True:
                		#get user input and exit if the user types q
				ansr = input('('+shellname+')> ')
				if ansr.lower() == 'q' or ansr.lower() == 'quit' or (previous_shell != None and ansr == previous_shell):
					break
				if ansr == 'l':
					print('\r(' + shellname + ')> ' + lastansr)
					ansr=lastansr
				#feed that input to the custom defined code and see if it is valid
				success = False
				if args != None:	
					success = code(ansr,args)
				else:
					success = code(ansr)
				if not success:
					#the function that we are "decorating" did not like the user input that we gave it
					#print out a uniform error message
					print('[ERROR] "' + ansr + '" not recognised as data or shell')
				lastansr = ansr
			if previous_shell:
				#the programer supplied us with the shell name of the "mother shell" 
				#tell the user we are returning to it
				print('['+shellname+'] returning to ' + str(previous_shell))
			else:
				#tell the user that we are exiting
				print('['+shellname+'] exiting')
			return 1
		return shell
	return decor
