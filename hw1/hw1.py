'''
Name: Jonah Miller
PennKey: jonahmil
'''

'''
In all functions below, the keyword "pass" is used to 
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''

def add_word(trie, word):
    '''
    args:
        trie: a dictionary representation of a trie
        word: a string
    ret: None
    Outcome: modified trie with word included
    '''
    if not word:
        return {}

    if trie == None:
        return {}

    c = word[0]
    if c in trie:
        if not trie[c]:
            return {}
        return add_word(trie.get(c), word[1:])
    else:
        trie[c] = add_word({}, word[1:])
        return trie


def create_trie(trie, word_list):
    '''
    args:
        trie: an empty dictionary
        word_list: list of strings
    ret: None
    Outcome: a dictionary representation of the trie
    '''
    if trie == None or word_list == None:
        return {}

    for word in word_list:
        add_word(trie, word)

    return trie

def in_trie(word, trie):
    '''
    args:
        word: a string
        trie: a dictionary representation of a trie
    ret:
        True if the word is in the trie
        False if the word is not in the trie
    '''
    if word == None or trie == None:
        return False

    if len(word) == 0:
        if trie == {}:
            return True

        return False

    c = word[0]

    if c in trie:
        return in_trie(word[1:], trie[c])
    else:
        return False


def list_matches(prefix, trie):
    '''
    args:
        prefix: a string
        trie: a dictionary representation of a trie
    ret:
        List of all words in the trie that begin with prefix
    '''
    list = []

    if prefix == None or trie == None:
        return list

    subtrie = prefix_subtrie(prefix, trie)
    
    if subtrie:
        listify(subtrie, prefix, list)

    return list


def prefix_subtrie(prefix, trie):
    if trie == None:
        return {}

    if not prefix:
        return trie

    c = prefix[0];

    if c in trie:
        return prefix_subtrie(prefix[1:], trie[c])
    else:
        return {}

def listify(trie, parent, list):
    if not trie:
        list.append(parent)
    for k, v in trie.items():
        listify(v, parent + k, list)


def main():
    '''
    Use this for testing! Make sure to be thorough and test for 
    corner cases.
    '''
    # Replace the code below with your own test code
    my_trie = {}
    word_list = ['hello', 'your', 'younger', 'youngest', 'youngun', 
        'yard', 'ding', 'dingy', 'dick']
    create_trie(my_trie, word_list)
    # print(my_trie)
    # print('')
    # add_word(my_trie, 'dicky')
    # print(my_trie)
    print(prefix_subtrie(None, my_trie))

if __name__ == '__main__':
    '''
    This calls the function main() when executing python3 hw1.py
    '''
    main()