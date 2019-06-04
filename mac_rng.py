from uuid import getnode as getmac
import random
import make_node
def seed_node(x,y):
    random.seed((getmac()-1)*400+(y-1)*20+x)

if __name__=='__main__':
    while True:
        ansr=input('(x y)> ')
        if ansr == 'q':
            break
        x = int(ansr.split(' ')[0])
        y = int(ansr.split(' ')[1])
        make_node.node(x,y,getmac()).toString()
