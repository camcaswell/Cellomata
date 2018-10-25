import numpy as np
from configparser import ConfigParser
from ast import literal_eval

if __name__=='__main__': 
    exit('Oops, you ran the wrong file.')

def ruledict_to_generator(ruledict):

    def retfunc(initial):
        ''' When given an initial boardstate, this function will construct a
            generator that yields successive boardstates.

            It uses the *ruledict* that was passed to the outer
            function to determine the next boardstate.
        '''
        rows = initial.shape[0]
        columns = initial.shape[1]
        current = initial

        while True:
            yield current

            neighbor_sums = np.zeros((rows, columns, ruledict['states']), dtype=np.uint8)
            for row in range(rows):
                for col in range(columns):
                    for a in range (row-1, row+2):
                        for b in range(col-1, col+2):
                            if (a,b) == (row,col):
                                continue
                            ## topographical wrap by messing with this
                            elif not( 0<=a<rows and 0<=b<columns):
                                neighbor_sums[row,col,0] += 1
                            else:
                                neighbor_sums[row,col,current[a,b]] += 1

            for row in range(rows):
                for col in range(columns):
                    current[row,col] = ruledict[current[row,col], tuple(neighbor_sums[row,col,:])]

    return retfunc

def preset(preset_name):
    with open('Preset_Update_Functions.cfg') as preset_file:
        preset_parser = ConfigParser()
        preset_parser.readfp(preset_file)
        ruledict = literal_eval(preset_parser.get(preset_name, 'ruledict'))

    retfunc = ruledict_to_generator(ruledict)
    retfunc.ruledict = ruledict
    return retfunc

def pre_dict(preset_name):
    with open('Preset_Update_Functions.cfg') as preset_file:
        preset_parser = ConfigParser()
        preset_parser.readfp(preset_file)
        ruledict = literal_eval(preset_parser.get(preset_name, 'ruledict'))
    return ruledict



def random_update_function(states=2, nhood='Moore', radius=1, seed=None):
    ''' random_update_function() generates a random update function in the form of
        a dict from the uniform distribution over the functionspace as defined by
        the parameters passed. The dict is overwritten to Last_Random_Update_Function.txt.
    '''
    np.random.seed(seed)
    nbors = (2*radius+1)*(2*radius+1)-1

    rules = {'states':states}
    for state in range(states):
        for neighbor_partition in starsnbars(nbors, states):
            rules[state, neighbor_partition] = np.random.randint(0, states, dtype=np.uint8)

    with open('Last_Random_Update_Function.txt', 'w') as savefile:
        print('[NAME]', file=savefile)
        print(f'ruledict = {rules}', file=savefile)

    retfunc = ruledict_to_generator(rules)
    retfunc.ruledict = rules
    return retfunc

    
def starsnbars(a, b):
    ''' Constructs a generator that yields all the possible ways to partition *a* objects into *b* sets
    '''
    if a == 0:
        yield tuple([0 for idx in range(b)])
    elif b == 1:
        yield (a,)
    else:
        for c in range(a+1):
            for sumlist in starsnbars(a-c,b-1):
                yield (c,) + sumlist

def func_dist(ruledict1, ruledict2):
    try:
        str1 = ''
        str2 = ''
        retval = 0
        for key, val1 in ruledict1.items():
            if key=='states': continue
            str1 += str(val1)
            str2 += str(ruledict2[key])
            if val1-ruledict2[key]:
                retval+=1
        return retval, '\n'+str1+'\n'+str2+'\n'
    except:
        raise ValueError("Functions must have same domain (i.e. neighborhoods and number of states).")

def outcomes(ruledict):
    totals = [0]*ruledict['states']
    for key,val in ruledict.items():
        if key=='states': continue
        totals[val] += 1
    return totals




