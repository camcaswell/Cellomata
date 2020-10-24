import numpy as np
from configparser import ConfigParser
from ast import literal_eval
from math import factorial

''' Functions for generating random update functions, retrieving preset update functions, and analyzing update functions.
'''

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

def random_update_function(states=2, nhood='Moore', radius=1, stability=0, state_weights=None, seed=None):
    ''' generates a random update function in the form of
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
            state_weights = np.zeros((states, states))
            for i in range(states):
                for j in range(states):
                    if i==j:
                        state_weights[i,j] = stability
                    else:
                        state_weights[i,j] = (1-stability)/(states-1)
        else:
            state_weights = np.ones((states, states)) * (1/states)

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
  
def _partition_weight(partition):
    ''' Returns the number of neighborhood configurations that could result in the given tuple of sums.
        Used to properly weight neighborhood sum tuples according to how "common" they are.
    '''
    return factorial(sum(partition))/np.prod([factorial(i) for i in partition])
    

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
    ''' Simply counts how many elements in the domain of the update function map to each state in the codomain.
        A very rough measure of how "likely" each state is to appear.
    '''
    totals = [0]*ruledict['states']
    for operand,result in ruledict.items():
        if operand=='states': continue
        totals[result] += 1
    return totals

def w_outcomes(ruledict):
    ''' Same as outcomes(), except each result is weighted according to how many possible neighborhoods are admitted by
        the neighborhood sum tuple that led to that result.
    '''
    totals = [0]*ruledict['states']
    for operand,result in ruledict.items():
        if operand=='states': continue
        totals[result] += _partition_weight(operand[1])
    return totals


def stability(ruledict):
    ''' Returns a list of counts for each state of how many times that state gets mapped to itself by the update function.
        i.e. how many times ufun(cur_state, nbhd_sums)==next_state for each state.
    '''
    stable_counts = [0]*ruledict['states']
    for operand,result in ruledict.items():
        if operand=='states': continue
        if operand[0]==result: stable_counts[result] += 1
    return stable_counts

def w_stability(ruledict):
    ''' Same as stability() except the count is weighted according to how many possible neighborhoods can result in that particular
        neighborhood sum tuple.
    '''
    stable_counts = [0]*ruledict['states']
    for operand,result in ruledict.items():
        if operand=='states': continue
        if operand[0]==result: stable_counts[result] += _partition_weight(operand[1])
    return stable_counts

def state_weight_matrix(ruledict):
    ''' Returns a matrix of counts for how many times each cur_state gets mapped to each next_state by the update function.
        This is a generalization of the stability() measure (stability() returns the diagonal of this matrix).
    '''
    W = np.zeros((ruledict['states'],ruledict['states']), np.uint8)
    for operand,result in ruledict.items():
        if operand=='states': continue
        W[operand[0], result] += 1
    return W

def w_state_weight_matrix(ruledict):
    ''' Same as state_weight_matrix() except the counts are weighted according to how many possible neighborhoods can result in that 
        particular neighborhood sum tuple.
    '''
    W = np.zeros((ruledict['states'],ruledict['states']), np.uint8)
    for operand,result in ruledict.items():
        if operand=='states': continue
        W[operand[0], result] += _partition_weight(operand[1])
    return W

def nbhd_conformity(ruledict):
    ''' A measure of how much the result of the update function agrees with the neighborhood pre-update.
        Does not count the cell itself together with the neighborhood.
    '''
    agreement_sum = 0
    for operand,result in ruledict.items():
        if operand=='states': continue
        agreement_sum += operand[1][result]
    return agreement_sum/(len(ruledict)-1)

def w_nbhd_conformity(ruledict):
    ''' Same as nbhd_conformity() except the agreement sum is weighted according to how many possible neighborhoods can result in each
        neighborhood sum tuple.
    '''
    agreement_sum = 0
    for operand,result in ruledict.items():
        if operand=='states': continue
        agreement_sum += operand[1][result]*_partition_weight(operand[1])
    return agreement_sum/(len(ruledict)-1)


