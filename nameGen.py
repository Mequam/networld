from random import randrange
def sumD(arr,D=0):
    ret_val=0
    for i in range(0,len(arr)):
        ret_val+=arr[i][D]
    return ret_val
def roll_mapp(mapp,x=None):
    #this function takes a mapp of "tickets"
    #and rolls a dice to see which tickets win, the more tickets you
    #have the more lickely you are to win
    if x == None:
        x = randrange(1,sumD(mapp)+1)
    mapp.sort()
    total=1
    for i in range(0,len(mapp)):
        if x < mapp[i][0] + total:
            return mapp[i][1]
        else:

            total+=mapp[i][0]
def str2arr(string):
	#this function takes a string and returns an array where each of the letters in that string is an element
	ret_val = []
	for i in range(0,len(string)):
		ret_val.append(string[i])
	return ret_val
def cpyArr(arr):
	ret_val = []
	for val in arr:
		ret_val.append(val)
	return ret_val
#this class contains all of the criteria that we use to generate names of a specific dialect
class generator():
	def __init__(self,letter_space = 'bcdfghjklmnpqrstvwxyz',vowels='aeiou'):
		#letter_space is a string where each letter represents a valid charicter for the name generator
		
		#an array used to temporarily store the letters
		buff_arr = str2arr(letter_space)+str2arr(vowels)
		prob_arr = []	

		for i in range(0,len(buff_arr)):
			prob_arr.append(randrange(1,50)**4)
		for i in range(0,4):
			prob_arr[randrange(0,len(prob_arr))] *= 2	
		#store each of the letters with their "tickets" inside of a mapp
		self.mapp = list(zip(prob_arr,buff_arr))

		self.chain = {}
		vowel_arr = str2arr(vowels)
		for vowel in vowel_arr:
			self.chain[vowel] = self.mapp	
		for i in range(0,len(letter_space)):
			#foreach letter in letterspace
		#reset each of the variables so that they will be clean the new letter
			
			#copy the buff_arr into cons_arr so that we can delete choices from it while still knowing all of our options
			#for future iterations of the loop
			cons_arr = str2arr(letter_space)	
			tmp_chain = []
			ticket_chain = []
		
		#fill out each of the variables
			#select which letters we want to jump to from the current one, and how lickely that jump will be	
			for j in range(0,randrange(1,3)):
				if len(cons_arr) == 0:
					break
				index = randrange(0,len(cons_arr))
				tmp_chain.append(cons_arr[index])
				ticket_chain.append(self.getTicket(cons_arr[index])+randrange(-2,3))
				#make sure that each letter is mapped to only once, no dubble dipping!
				del cons_arr[index]
			for vowel in vowel_arr:
				tmp_chain.append(vowel)
				ticket_chain.append(self.getTicket(vowel)*3)
		
		#store the variables that we set into there permanent space
			self.chain[letter_space[i]] = list(zip(ticket_chain,tmp_chain))
		#the average length of words
		self.avl = randrange(4,7)
	def getTicket(self,letter):
		for i in range(0,len(self.mapp)):
			if self.mapp[i][1] == letter:
				return self.mapp[i][0]
		return False
	def makeWord(self):
		l = roll_mapp(self.mapp)
		ret_val = l
		for i in range(0,self.avl+randrange(-1,4)-1):
			l = roll_mapp(self.chain[l])
			ret_val += l
		return ret_val
			
if __name__ == '__main__':
	g = generator()
	for i in range(1,100):
		print(g.makeWord())
