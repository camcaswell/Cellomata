import numpy as np
from configparser import ConfigParser
from ast import literal_eval

if __name__=='__main__': 
    exit('Oops, you ran the wrong file.')

def _ruledict_to_generator(ruledict):

    def updater(initial):
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

    return updater

## This was a failed attempt to make the updater faster.
## I'm keeping it in case it makes abstracting on neighborhoods easier.

# def _alt_ruledict_to_generator(ruledict):

#     def updater(initial):
#         ''' When given an initial boardstate, this function will construct a
#             generator that yields successive boardstates.

#             It uses the *ruledict* that was passed to the outer
#             function to determine the next boardstate.
#         '''
#         rows = initial.shape[0]
#         columns = initial.shape[1]
#         prev = initial

#         ## Calculating the initial neighbor sums.
#         prev_nsums = np.zeros((rows, columns, ruledict['states']), dtype=np.uint8)
#         for row in range(rows):
#             for col in range(columns):
#                 for a in range (row-1, row+2):
#                     for b in range(col-1, col+2):
#                         if (a,b) == (row,col):
#                             continue
#                         ## topographical wrap by messing with this
#                         elif not( 0<=a<rows and 0<=b<columns):
#                             prev_nsums[row,col,0] += 1
#                         else:
#                             prev_nsums[row,col,prev[a,b]] += 1

#         ## Using *ruledict*, *prev*, and *prev_nsums* to determine *current*.
#         ## *cur_nsums* are also calculated in the same loop to be used in the next while-iteration.
#         current = np.zeros((rows, columns), dtype=np.uint8)
#         while True:

#             yield prev

#             cur_nsums = np.zeros((rows, columns, ruledict['states']), dtype=np.uint8)
#             for row in range(rows):
#                 for col in range(columns):
#                     current[row,col] = ruledict[prev[row,col], tuple(prev_nsums[row,col,:])]
#                     for a in range (row-1, row+2):
#                         for b in range(col-1, col+2):
#                             if (a,b) == (row,col) or not(0<=a<rows) or not(0<=b<columns):
#                                 continue
#                             else:
#                                 cur_nsums[a,b,current[row,col]] += 1

#             ## Fixing neighborhood sums for cells on the border. Outside border is counted as always all zeros. 
#             for a in range(rows):
#                 cur_nsums[a,0,0] += 3
#                 cur_nsums[a,columns-1,0] += 3
#             for b in range(columns):
#                 cur_nsums[0,b,0] += 3
#                 cur_nsums[rows-1,b,0] += 3
#             for a in [0, rows-1]:
#                 for b in [0, columns-1]:
#                     cur_nsums[a,b,0] -= 1

#             prev = current
#             prev_nsums = cur_nsums

#     return updater

def preset(preset_name):
    ruledict = pre_dict(preset_name)
    retfunc = _ruledict_to_generator(ruledict)
    retfunc.ruledict = ruledict
    return retfunc

def pre_dict(preset_name):
    with open('Preset_Update_Functions.cfg') as preset_file:
        preset_reader = ConfigParser()
        preset_reader.read_file(preset_file)
        ruledict = literal_eval(preset_reader.get(preset_name, 'ruledict'))
    return ruledict



def random_update_function(states=2, nhood='Moore', radius=1, stability=0, state_weights=W, seed=None):
    ''' random_update_function() generates a random update function in the form of
        a dict from the uniform distribution over the functionspace as defined by
        the parameters passed. The dict is overwritten to Last_Random_Update_Function.txt.
    '''
    np.random.seed(seed)
    nbors = (2*radius+1)*(2*radius+1)-1

    ''' *stability* is the probability that a cell will remain in the same state after it is updated
        (over the uniform space of possible state-neighborhood sum combinations, i.e. ignoring that some configurations may be more likely).
        Normally the outcome states are chosen uniformly, but this allows you to artificially increase the stability of boardstates.
    '''
    if not stability:
        stability = 1/states

    rules = {'states':states}
    for state in range(states):
        pdist = [(1-stability)/(states-1)]*states
        pdist[state] = stability
        for neighbor_partition in _starsnbars(nbors, states):
            rules[state, neighbor_partition] = np.random.choice(states, 1, p=pdist)[0]

    config_writer = ConfigParser()
    with open('Last_Random.cfg', 'r') as savefile:
        config_writer.read_file(savefile)
        config_writer.set('Update Function', 'ruledict', str(rules))
    with open('Last_Random.cfg', 'w') as savefile:
        config_writer.write(savefile)

    retfunc = _ruledict_to_generator(rules)
    retfunc.ruledict = rules
    return retfunc

def alt_random_update_function(states=2, nhood='Moore', radius=1, stability=0, state_weights=None, seed=None):
    ''' random_update_function() generates a random update function in the form of
        a dict from the uniform distribution over the functionspace as defined by
        the parameters passed. The dict is overwritten to Last_Random_Update_Function.txt.
    '''
    np.random.seed(seed)
    nbors = (2*radius+1)*(2*radius+1)-1

    ''' *stability* is the probability that a cell will remain in the same state after it is updated
        (over the uniform space of possible state-neighborhood sum combinations, i.e. ignoring that some configurations may be more likely).
        Normally the outcome states are chosen uniformly, but this allows you to artificially increase the stability of boardstates.
    '''
    if not state_weights:
        if stability:
            state_weights = np.zeros(states, states)
            for i in states:
                for j in states:
                    if i==j:
                        state_weights[i,j] = stability
                    else:
                        state_weights[i,j] = (1-stability)/(states-1)
        else:
            state_weights = np.ones(states, states) * (1/states)

    rules = {'states':states}
    for state in range(states):
        for neighbor_partition in _starsnbars(nbors, states):
            rules[state, neighbor_partition] = np.random.choice(states, 1, p=state_weights[state,:])[0]

    config_writer = ConfigParser()
    with open('Last_Random.cfg', 'r') as savefile:
        config_writer.read_file(savefile)
        config_writer.set('Update Function', 'ruledict', str(rules))
    with open('Last_Random.cfg', 'w') as savefile:
        config_writer.write(savefile)

    retfunc = _ruledict_to_generator(rules)
    retfunc.ruledict = rules
    return retfunc
    
def _starsnbars(a, b):
    ''' Constructs a generator that yields all the possible ways to partition *a* objects into *b* sets
    '''
    if a == 0:
        yield (0,)*b
    elif b == 1:
        yield (a,)
    else:
        for c in range(a+1):
            for sumlist in _starsnbars(a-c,b-1):
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

def stability(ruledict):
    stable_counts = [0]*ruledict['states']
    for key,state in ruledict.items():
        if key=='states': continue
        if key[0]==state: stable_counts[state] += 1
    return stable_counts

def state_weight_matrix(ruledict):
    W = np.zeros((ruledict['states'],ruledict['states']), np.uint8)
    for key,state in ruledict.items():
        if key=='states': continue
        W[key[0], state] += 1
    return W