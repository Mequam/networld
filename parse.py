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
