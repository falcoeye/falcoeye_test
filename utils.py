import operator
import random
import string

ops = {"==": operator.eq, "!=": operator.ne, "in": operator.contains}



# printing lowercase
letters = string.ascii_lowercase
def random_string(length=5):
    return ''.join(random.choice(letters) for i in range(length))