
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
        str1 += ", "
 
    # return string
    return str1[:-2]

def stringToBool(s):
    if s == 'yes':
         return True
    else:
        return False