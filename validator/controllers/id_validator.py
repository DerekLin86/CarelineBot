import re


class IDValidator:
    def __init__(self):
        pass

    def isValid(self, id_number):
        pattern = '^[A-Z]+[0-9]{9}$'

        if (len(id_number) != 10):
            return False        

        if (not re.match(pattern, id_number)):
            return False        

        return True


