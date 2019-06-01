from random import randrange
from math import floor
def check_outer(expr,parenth=['(',')']):
    #this function checks to see if a given expression is surrounded COMPLETY by parenthasis
    inside = 0
    elen = len(expr)
    for i in range(0,elen):
        if expr[i] == parenth[0]:
            inside += 1
        elif expr[i] == parenth[1]:
            inside -= 1
        elif inside == 0:
            #the reason this is else is so it doesnt fire if our last charicter is parenthasis
            #we are currently outside of parenthasies, so return false
            #becuse the entire expression is not inside of parenthasis
            return False
    #we never made it out of the currlys so we were allways inside parenthasis
    return True
def strip_outer(expr,parenth=['(',')']):
    if check_outer(expr):
        #there is a pair of outside parenthasis, strip them and return the next stripped version in the chain 
        return strip_outer(expr[1:-1])
    else:
        #there are no parenthasys on the outsides of the expression
        return expr
def parse(expr,f_arr,default,parenth=['(',')'],args=[]):
    #strip the outer parenthasis that way if the program sends us a parenthasised expression
    #we can use it like a normal one
	expr = strip_outer(expr,parenth)
	inside = 0
	for i in range(0,len(f_arr)):
		for j in range(0,len(expr)):	
			if expr[j] == parenth[0]:
				inside+=1
			elif expr[j] == parenth[1]:
				inside -= 1
			elif expr[j:j+len(f_arr[i][0])] == f_arr[i][0] and inside == 0:
				return f_arr[i][1](j,expr,f_arr,default,parenth,args)	
#we found no funtion symbols in the expresion, return an intager to exit the recursion series
	return default(expr)

def parse_safe(expr,f_arr,default,parenth=['(',')'],args=[]):
	pass_expr = ''
	split_expr = expr.split(' ')
	for word in split_expr:
		pass_expr += word	
	return parse(pass_expr,f_arr,default,parenth,args)
	
#to make a function that works with the parse function above, it either needs to be an exit case or to call parse again
#and the j variable points to the FIRST index of the string that represents this operation
def And(j,expr,f_arr,default,parenth,args):
	return parse(expr[0:j],f_arr,default,parenth,args) and parse(expr[j+2:len(expr)],f_arr,default,parenth)
def Or(j,expr,f_arr,default,parenth,args):
	return parse(expr[0:j],f_arr,default,parenth,args) or parse(expr[j+2:len(expr)],f_arr,default,parenth,args)	
def Not(j,expr,f_arr,default,parenth,args):
	return not parse(expr[1:len(expr)],f_arr,default,parenth,args)
def Default(expr):
	if expr == 't' or expr == 'true':
		return True
	elif expr == 'f' or expr == 'false':
		return False
	else:
		return expr
arr = [('&&',And),('||',Or),('!',Not)] 
if __name__ == '__main__':
    ansr = input('(main)> ')
    while ansr != 'q':
        print(parse(ansr,arr,Default))
        ansr = input('(main)> ')
