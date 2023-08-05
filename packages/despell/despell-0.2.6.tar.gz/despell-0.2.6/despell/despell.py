import numpy as np
import random

qwerty_replace_dict = {'a': ['s', 'z', 'q'], 
                       'b': [' ', 'v', 'n', 'g', 'h'], 
                       'c': ['x', 'd', 'f', 'v', ' '], 
                       'd': ['s', 'f', 'e', 'x', 'c'], 
                       'e': ['w', 'r', 's', 'd', '3', '4'], 
                       'f': ['d', 'c', 'v', 'g', 't', 'r'], 
                       'g': ['f', 'v', 'b', 'h', 'y', 't', 'r'], 
                       'h': ['g', 'b', 'n', 'j', 'u', 'y'], 
                       'i': ['u', 'j', 'k', 'o', '8', '9'], 
                       'j': ['h', 'n', 'm', 'k', 'i', 'u'], 
                       'k': ['j', 'm', ',', 'l', 'o', 'i'], 
                       'l': ['k',',','.',';','p','o'], 
                       'm': ['n', ' ', ',', 'k', 'j'], 
                       'n': ['b', ' ', 'm', 'j', 'h'], 
                       'o': ['i','k','l','p','0','9',], 
                       'p': ['o','l',';','[','-', '0'], 
                       'q': ['a','s','w','1','2'], 
                       'r': ['e','d','f', 't', '5', '4'], 
                       's': ['a','z','x','d','e','w'], 
                       't': ['r','f','g','y','6','5'], 
                       'u': ['y','h','j','i','8','7'], 
                       'v': ['c',' ','b','g','f'], 
                       'w': ['q','a','s','e','3','2'], 
                       'x': ['z',' ','c','d','s'], 
                       'y': ['t','g','h','u','7','6'], 
                       'z': ['a', 's', 'x'], 
                       '1': ['`','2'], 
                       '2': ['1','3'], 
                       '3': ['2','4'], 
                       '4': ['3','5'], 
                       '5': ['4','6'], 
                       '6': ['5','7'], 
                       '7': ['6','8'], 
                       '8': ['7','9'], 
                       '9': ['8','0'], 
                       '0': ['9','-'], 
                       '~': ['!'], 
                       '!': ['`','@'], 
                       '@': ['!', "#"], 
                       '#': ['@', '$'], 
                       ' ': [' '],
                       '$': ['#', '%'], 
                       '%': ['$', '^'], 
                       '^': ['%', '&'], 
                       '&': ['^', '*'], 
                       '*': ['&', '('], 
                       '(': ['*', ')'], 
                       ')': ['(', '-'], 
                       '-': ['0', '='], 
                       '=': ['-'], 
                       '_': ['+', ')'], 
                       '+': ['_'], 
                       '<': ['m', '>', 'l', 'k'], 
                       '>': ['<', '?'], 
                       '?': ['>'], 
                       ':': ['l', '\"'], 
                       "\"": [':'], 
                       '{': [], 
                        '}': [], 
                       ',': ['.','m','l','k',' '], 
                       '.': [',', '/', ';', 'l'], 
                       '/': [], 
                       ';': [], 
                       '\'': [], 
                       '[': [], 
                       ']': [], 
                       '\\': [], 
                       '|': []}

phonetic_replace_dict = {'a': [], 'b': [], 'c': ['k'], 'd': [], 'e': ['ee','y', 'ey','i'], 'f': [], 'g': [], 'h': [], 'i': ['y'], 'j': [], 'k': ['c'], 
                    'll': ['l'], 'm': [], 'n': [], 'ou': ['o'], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 
                    'x': [], 'y': ['i'], 'z': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], 
                    'ss': ['s'], '~': [], '!': [], '@': [], '#': [], '$': [], '%': [], '^': [], '&': [], '*': [], '(': [], 
                    'ei': ['i', 'ie','e'], 'ie': ['ei','i','e'], '=': [], '_': [], '+': [], '<': [], '>': [], '?': [], ':': [], "\"": [], '{': [], 
                    '}': [], ',': [], '.': [], '/': [], ';': [], '\'': [], '[': [], ']': [], '\\': [], '|': []}

caps_replace_dict = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 
                    'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 
                    'x': [], 'y': [], 'z': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], 
                    '0': [], '~': [], '!': [], '@': [], '#': [], '$': [], '%': [], '^': [], '&': [], '*': [], '(': [], 
                    ')': [], '-': [], '=': [], '_': [], '+': [], '<': [], '>': [], '?': [], ':': [], "\"": [], '{': [], 
                    '}': [], ',': [], '.': [], '/': [], ';': [], '\'': [], '[': [], ']': [], '\\': [], '|': []}

complex_replace_dict = {'ight': ['ite', 'yt'], 'ing': ['in'], 'ck': ['k','c'], 'ough': ['au', 'aw'], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [], 
                    'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 
                    'x': [], 'y': [], 'z': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], 
                    '0': [], '~': [], '!': [], '@': [], '#': [], '$': [], '%': [], '^': [], '&': [], '*': [], '(': [], 
                    ')': [], '-': [], '=': [], '_': [], '+': [], '<': [], '>': [], '?': [], ':': [], "\"": [], '{': [], 
                    '}': [], ',': [], '.': [], '/': [], ';': [], '\'': [], '[': [], ']': [], '\\': [], '|': []}

class weights:
    
    def __init__(self,weights):
        
        assert type(weights) == list
        
        for i in range(len(weights)):
            assert (type(weights[i]) == float) or (type(weights[i]) == int)
        
        self.w_sum = np.sum(weights)
        self.w1 = weights[0] / self.w_sum
        self.w2 = (weights[1] + weights[0]) / self.w_sum
        self.w3 = (weights[2] + weights[1]) / self.w_sum
        self.w4 = (weights[3] + weights[2]) / self.w_sum
        self.w5 = (weights[4] + weights[3]) / self.w_sum
        
def corrupt_text(text, error_rate = 1/30, weight_ratios = [1,1,1,1,1]):
    
    """
    Overview
    --------
    Introduces errors into a string.
    
    
    Inputs
    ------
    text (str): A text string.
    error_rate (float): Rate at which errors are introduced,
        measured in errors per character.
    weight_ratios (list): List of floats determining the likelihood
        ratio of different types of errors.
        
        
    Returns
    -------
    
    """
    
    assert type(text) == str
    assert type(error_rate) == float
    assert type(weight_ratios) == list
    
    for i in range( len(weight_ratios) ):
        assert ( type(weight_ratios[i]) == float ) or ( type(weight_ratios[i]) == int )

    
    scaled_weights = weights(weight_ratios)
    
    text = text.lower()
    text = list(text)
    num_chars = len(text)
    
    errors = int( np.ceil( error_rate*num_chars ) )

    if num_chars < errors:
        
        raise Exception("Number of errors exceeds number of characters")
    
    idx = list( range(num_chars) )
    random.shuffle(idx)
    
    error_indices = idx[0:errors]
    
    for i in error_indices:
        
        text[i] = corrupt_char(text[i], scaled_weights)
        
    if np.random.uniform() > scaled_weights.w4:
        
        text = transpose(text)
        
    return ''.join(text)

def corrupt_char(char, scaled_weights):
    
    """
    Overview
    --------
    Replaces a character with an erroneous character.
    
    
    Inputs
    ------
    char (str): A character.
    scaled_weights (object): Object containing weights that determine
        the likelihood of particular types of error.
        
    
    Returns
    -------
    char (str): Erroneous character replacement.
    """
    
    assert type(char) == str
    
    
    if np.random.uniform() < scaled_weights.w1:

            char = spatial_replace(char)
        
    elif np.random.uniform() < scaled_weights.w2:
        
            char = phonetic_transform(char)
            
    elif np.random.uniform() < scaled_weights.w3:
            
            char = char*2
        
    elif np.random.uniform() < scaled_weights.w4:

            char = ''
            
    elif np.random.uniform() < scaled_weights.w5:
        
        char = insertion(char)
            
    return char
            
def spatial_replace(char):
    
    """
    Overview
    --------
    Replaces chars with chars nearby on keyboard.
    """
    
    assert type(char) == str
    
    
    idx = np.random.randint( len( qwerty_replace_dict[char] ) )
    char = qwerty_replace_dict[char][idx]
            
    return char

def insertion(char):
    
    """
    Overview
    --------
    Adds a nearby character to the left or right of input char.
    """
    
    assert type(char) == str
    
    
    idx = np.random.randint( len( qwerty_replace_dict[char] ) )
    
    if np.random.uniform() < 0.5:
        char += qwerty_replace_dict[char][idx]
        
    else:
        char = qwerty_replace_dict[char][idx] + char
        
    return char

def phonetic_transform(char):
    
    """
    Consider using a neural net to do this as creating manual
    rules is pretty tedious and crap.
    """
    
    assert type(char) == str
    
    
    try:
        idx = np.random.randint( len( phonetic_replace_dict[char] ) )
        char = phonetic_replace_dict[char][idx]
        
    except:
        return char
    
    return char  

def transpose(text):
    
    """
    Overview
    --------
    Swaps two adjacent characters.
    """
    
    assert type(text) == list
    
    
    for i in range(len(text)):
        assert type(text[i]) == str
    
    text_len = len(text)
    
    idx = np.random.randint(1,text_len)
    
    swap = text[idx]
    text[idx] = text[idx-1]
    text[idx-1] = swap
    
    return text
