def get_enclosed(parenth=['[',']']):
    def decor(fun):
        def parse(expr,parenth2=parenth):
            first_index = expr.find(parenth2[0])
            second_index = -1
            count = 1
            for i in range(first_index+1,len(expr)):
                if expr[i] == parenth2[0]:
                    count += 1
                elif expr[i] == parenth2[1]:
                    count -= 1
                if count == 0:
                    second_index = i
                    break
            if second_index < first_index:
                return -1
            elif second_index  == -1 or first_index == -1:
                #the string no longer contains any parenthasis
                #so we can return it
                return expr
            else:
                #the function contains parenthasis, pass it down the chain without the parenthasis that we found
                return parse(expr[:first_index] + fun(expr[first_index + 1:second_index]) + expr[second_index + 1:],parenth2)
        return parse
    return decor

#this function takes an array and concatanates the values together using delimiter
def squish(arr,delim):
	ret_val = ''
	for word in arr:
		ret_val += word + delim
	return ret_val[:-1]
#this function is a simple function to prompt the user and force them to pick a letter from the given list
def selectPrompt(prompt,options):
	i = input(prompt)
	while i not in options:
		i = input('('+squish(options,'/')+')> ')
	return i
#this function loads an array from a pickle
def loadArr(filename):
	try:
		f = open(filename,'rb')
		arr = pickle.load(f)
		f.close()
		return arr
	except:
		return False
#this function saves an array to a pickle
def saveArr(arr,filename):
	try:
		f = open(filename,'wb')
		pickle.dump(arr,f,pickle.HIGHEST_PROTOCOL)
		f.close()
		return True
	except:
		return False
