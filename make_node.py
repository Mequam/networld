import random
import GramGen

def cat2num(cat):
    if cat == 'insane':
        return 11
    elif cat == 'high':
        return 8
    elif cat == 'medium':
        return 6
    elif cat == 'low':
        return 4
    elif cat == 'scarce':
        return 1
    else:
        print('[*] returning 0!')
        return 0
def get_cat(x=None):
    return roll_mapp([(1,'insane'),(1,'scarce'),(3,'medium'),(2,'high'),(2,'low')]) 
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
        x=random.randrange(1,sumD(mapp)+1)
    mapp.sort()
    total=1
    for i in range(0,len(mapp)):
        if x < mapp[i][0] + total:
            return mapp[i][1]
        else:

            total+=mapp[i][0]

def get_rand(arr):
    return arr[random.randrange(0,len(arr))]

class node:
    def toString(self,debug=False):
        print(f'tempature: {self.temp}')
        print(f'slope: {self.slope}')
        print(f'flatness: {self.flat}')
        print(f'hostility: {self.hostil}')
    def __init__(self,x,y,mac):
        self.seed=(mac-1)*400+(y-1)*20+x
        random.seed(self.seed)
class Terrain:
	def __init__(self,g,entry):
		self.desc = g.entry(entry)
g = GramGen.generator('gen.xml')
t = Terrain(g,'schems/noun_clause/biomes/biomes.scm')
print(t.desc)
