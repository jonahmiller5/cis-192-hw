'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 3
'''

'''
In all functions below, the keyword "pass" is used to
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''

from itertools import cycle


def load_file_list(filename):
    '''
    Read the list of files from filename
    args:
        filename: the name of the file containing a list
        of filenames separated line by line
    ret:
        filelist: a list of filenames

    Note: be sure to remove any trailing newlines
    '''
    l = []

    if filename is None or not isinstance(filename, str):
        print('load_file_list(): Invalid input for "filename"')
        return l

    file = None
    try:
        file = open(filename)
    except FileNotFoundError:
        return l

    for line in file:
        l.append(line[:-1])

    return l


def sort_file_list_helper(filelist):
    filematching = {}

    listfromtuples = lambda tuples: [tuple[1] for tuple in tuples]
    strip = lambda file: int(''.join([c for c in file if c.isdigit()]))

    for file in filelist:
        num = strip(file)
        filematching[num] = file

    tuplelist = [file for file in sorted(filematching.items())]

    return listfromtuples(tuplelist)


def sort_file_list_easy(filelist):
    '''
    Sort the list of files in place based on ID
    args:
        filelist: a list containing a set of strings
        representing the filenames
    ret: None
    Outcome: filelist should be sorted by numeric ID

    Note: for this function, assume the prefix to the ID
    is file and the suffix is .txt
    '''
    if filelist is None or not isinstance(filelist, list):
        print('sort_file_list_easy(): Invalid input for "filelist"')
        return []

    return sort_file_list_helper(filelist)


def sort_file_list_hard(filelist):
    '''
    Sort the list of files in place based on ID
    args:
        filelist: a list containing a set of strings
        representing the filenames
    ret: None
    Outcome: filelist should be sorted by numeric ID

    Note: for this function, you may not assume any fixed
    prefix or suffix to the ID. They may be completely
    arbitrary, and even different across files
    '''
    if filelist is None or not isinstance(filelist, list):
        print('sort_file_list_hard(): Invalid input for "filelist"')
        return []

    return sort_file_list_helper(filelist)


def write_in_cyclic_order(filelist, strlist):
    '''
    Write one string from strlist to each file in filelist,
    iterating over them in the same order.
    args:
        filelist: a list of filenames to write to
        strlist: an iterable of strings to write to the files
    ret: None
    Outcome: each file must have a string corresponding to
    its position in the sorted list

    Note: you may not assume that strlist is the same
    length as filelist, but you may assume it is not longer
    than filelist. If strlist is shorter than filelist,
    then you must cycle back to the beginning of strlist
    upon completing. For this, you may use the cycle function
    imported above.
    '''
    if filelist is None or not filelist isinstance(filelist, list):
    	return

    if strlist is None or not filelist isinstance(strlist, str) or not filelist isinstance(strlist, list):
    	return

    iterator = cycle(strlist)
    s = next(iterator)
    for filename in filelist:
        file = None
        try:
            file = open(filename, 'w+')
        except FileNotFoundError:
            s = next(iterator)
            continue

        file.write(s)
        file.close()
        s = next(iterator)


def main():
    '''
    Use this for testing! Make sure to be thorough and test for
    corner cases.
    '''
    filename = 'file_list_hard.txt'
    strlist = 'abcdefghijklmnopqrstuvwxyz'
    filelist = load_file_list(filename)
    filelist = sort_file_list_easy(filelist)
    # write_in_cyclic_order(filelist, strlist)
    # print(filelist)


if __name__ == '__main__':
    '''
    This calls the function main() when executing python3 hw2.py
    '''
    main()
