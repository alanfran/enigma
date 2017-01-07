from copy import deepcopy
import os
from StringClasses import AlphabetCustom, SpecificationFiles


# Gets the reflector
def getReflector():
    reflector = []

    # Read the reflector specification from file
    with open(SpecificationFiles.reflectorOut, 'r') as f:
        lines = f.readlines()

    # Create list of tuples, creating the reflector
    for line in lines:
        reflector.append((line[0], line[2]))

    return reflector

# Gets the steckerboard
def getSteckerboard():
    steckerboard = []

    # Read the steckerboard specification from file
    with open(SpecificationFiles.steckerboardOut, 'r') as f:
        lines = f.readlines()

    # Create a list of tuples, creating the steckerboard
    for line in lines:
        steckerboard.append((line[0], line[2]))

    return steckerboard

# Gets the list of rotors
def getRotors():
    rotors = []

    # Read rotor specifications from file
    with open(SpecificationFiles.rotorsOut, 'r') as f:
        lines = f.readlines()

    # Each rotor is on one line
    for line in lines:
        line = [x for x in line if x in AlphabetCustom.alphabet]
        rotors.append(line)

    return rotors

# Get the list of characters that the rotors shift on
def getKnocksOn():
    # Read knocks on specifications from file
    with open(SpecificationFiles.knocksOnOut, 'r') as f:
        knocksOn = f.read().splitlines()

    return knocksOn

# Get the message setting to shift the rotors by
def getMessageSetting():
    # Read the message setting specification from file
    with open(SpecificationFiles.messageSettingOut, 'r') as f:
        messageSetting = f.read().splitlines()

    return messageSetting

# Get the message
def getMessage():
    # If the file does not exist, create it with empty text
    if not os.path.isfile(SpecificationFiles.messageOut):
        setMessage('Please enter text in {0}'.format(SpecificationFiles.messageOut))

    # Read message from file
    with open(SpecificationFiles.messageOut, 'r') as f:
        message = f.read()

    return message

# Set the message
def setMessage(message):
    # Set message to file
    with open(SpecificationFiles.messageOut, 'w+') as f:
        f.write(message)

class Enigma(object):
    # constructor
    def __init__(self, rotors, reflectorChoice, steckerBoard, knocksOn, messageSetting):
        # Rotor lists from left to right eg: [3, 2, 1]
        self._rotors = rotors
        # Shift rotors per each message setting
        for i in range(0, len(self._rotors)):
            self._rotors[i] = self._rotors[i][int(messageSetting[i]):] + self._rotors[i][:int(messageSetting[i])]
        # Original rotors are copied to allow a reset function
        self._originalRotors = deepcopy(self._rotors)
        # List of substitution pairs [('A', 'B'), ...]
        self._reflector = reflectorChoice
        # List of substitution pairs [('A', 'Z'), ... ]
        self._steckerBoard = steckerBoard
        # List of what letter the rotors shift at
        self._knocksOn = knocksOn

    # Resets the machine to its original state
    def reset(self):
        self._rotors = deepcopy(self._originalRotors)

    # Outputs the specifications of the enigma machine
    def print_specs(self):
        print('steckerboard: {0}'.format(self._steckerBoard))
        print('rotors: {0}'.format(self._rotors))
        print('original rotors: {0}'.format(self._originalRotors))
        print('knock ons: {0}'.format(self._knocksOn))
        print('reflector: {0}'.format(self._reflector))

    # Encrypts the message
    def encrypt(self, message, keep_non_alphabet=False):
        # remove all non alphabet characters unless keep_non_alphabet = True
        if keep_non_alphabet is False:
            message = filter(lambda ch: ch in AlphabetCustom.alphabet, message)

        encrypted = ''

        # assuming 3 rotors...
        # for each character in message
        #    character -> steckerBoard -> rotorR -> rotorM -> rotorL -> reflect -> rotorL -> rotorM -> rotorR -> steckerBoard -> output
        #    shiftRotor(RIGHT, 1)
        for ch in message:
            if ch in AlphabetCustom.alphabet:
                # steckerboard
                newCh = self.steckerBoard(ch)

                # pass through all rotors, right to left ordering
                for i in reversed(range(0, len(self._rotors))):
                    newCh = self.rotor(i, newCh)

                # reflect
                newCh = self.reflect(newCh)

                # pass back through all rotors, left to right ordering
                for j in range(0, len(self._rotors)):
                    newCh = self.invRotor(j, newCh)

                # steckerboard
                newCh = self.steckerBoard(newCh)
            else:
                newCh = ch

            # add letter to encrypted text
            encrypted += newCh

            # shift the rotor by one
            self.shiftRotor(len(self._rotors) - 1, 1)

            # handle if loop -> rotate next rotor
            # check right to left ordering
            for k in reversed(range(0, len(self._rotors))):
                if self.knockLeft(k):
                    continue
                else:
                    break

        return encrypted

    # Shifts a rotor by n
    def shiftRotor(self, rotorPosition, n):
        n = n % len(self._rotors[0])
        # Shift the rotor by rotating it n ticks
        self._rotors[rotorPosition] = self._rotors[rotorPosition][n:] + self._rotors[rotorPosition][:n]
	
    # Check if a rotor should shift its neighbor to the left, and then perform the shift if appropriate
    def knockLeft(self, rotorPosition):
        # If the rotor is on the letter it knocks on, shift the adjacent rotor
        if self._rotors[rotorPosition][0] == self._knocksOn[rotorPosition]:
            self.shiftRotor((rotorPosition - 1) % len(self._rotors), 1)
            return True
        else:
            return False

    # Swap char with its tuple-mate using the steckerboard
    def steckerBoard(self, char):
        for tuple in self._steckerBoard:
            if char == tuple[0]:
                return tuple[1]
            elif char == tuple[1]:
                return tuple[0]

        # char not found in steckerboard
        return char

    # Swap char with its tuple-mate using the reflector
    def reflect(self, char):
        for tuple in self._reflector:
            if char == tuple[0]:
                return tuple[1]
            elif char == tuple[1]:
                return tuple[0]

    # Get the character output from a specific rotor
    def rotor(self, rotorPosition, char):
        # substitute this character with the appropriate character from the rotor
        return self._rotors[rotorPosition][AlphabetCustom.alphabet.index(char)]

    # Get the character opposite of rotor()
    def invRotor(self, rotorPosition, char):
        # do the opposite of rotor()
        return AlphabetCustom.alphabet[self._rotors[rotorPosition].index(char)]


# Get enigma machine specifications
myReflector = getReflector()
mySteckerboard = getSteckerboard()
myRotors = getRotors()
myKnocksOn = getKnocksOn()
myMessageSetting = getMessageSetting()

# Get plaintext
myMessage = getMessage()
print('Plaintext: {0}'.format(myMessage))

# Initialize enigma machinie using specifications
myEnigma = Enigma(rotors=myRotors, reflectorChoice=myReflector, steckerBoard=mySteckerboard, knocksOn=myKnocksOn,
                  messageSetting=myMessageSetting)

# Encrypt the message
encrypted = myEnigma.encrypt(myMessage)
print('Ciphertext: {0}'.format(encrypted))
setMessage(encrypted)

debug = False
if debug:
    # Reset the enigma machine to its original state
    myEnigma.reset()

    # "Encrypt" the encrypted text to decrypt it
    decrypted = myEnigma.encrypt(encrypted)
    print('Decrypted: {0}'.format(decrypted))