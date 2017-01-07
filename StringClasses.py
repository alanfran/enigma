import string

# Class to hold our customizable alphabet
class AlphabetCustom(object):
    # Note: alphabet must be an even length
    alphabet = string.letters + string.digits + string.punctuation[:-1] + ' '

# Class to hold our file names
class SpecificationFiles(object):
    reflectorOut = 'reflectorOut.txt'
    steckerboardOut = 'steckerboardOut.txt'
    rotorsOut = 'rotorsOut.txt'
    knocksOnOut = 'knocksOnOut.txt'
    messageOut = 'messageOut.txt'
    messageSettingOut = 'messageSettingOut.txt'