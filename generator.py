from copy import deepcopy
import os
import random
from StringClasses import AlphabetCustom, SpecificationFiles


# Generate a random reflector
def generateReflector(output=True):
    reflector = []
    alpha = deepcopy(AlphabetCustom.alphabet)

    # Create a list of tuples for our alphabet
    while len(alpha) > 0:
        rand = random.sample(range(0, len(alpha)), 2)
        charA, charB = (alpha[rand[0]], alpha[rand[1]])
        reflector.append((charA, charB))
        alpha = alpha.replace(charA, '')
        alpha = alpha.replace(charB, '')

    if output:
        with open(SpecificationFiles.reflectorOut, 'w+') as f:
            f.write('\n'.join('{} {}'.format(x[0],x[1]) for x in reflector))

    return reflector

# Generate a random steckerboard
def generateSteckerboard(optimal_tuples):
    # Use generateReflector, but do not output same result
    steckerboard = []
    alpha = deepcopy(AlphabetCustom.alphabet)

    # Create a list of tuples for our alphabet
    i = 0
    while len(alpha) > 0 and i < optimal_tuples:
        rand = random.sample(range(0, len(alpha)), 2)
        charA, charB = (alpha[rand[0]], alpha[rand[1]])
        steckerboard.append((charA, charB))
        alpha = alpha.replace(charA, '')
        alpha = alpha.replace(charB, '')
        i += 1

    with open(SpecificationFiles.steckerboardOut, 'w+') as f:
        f.write('\n'.join('{} {}'.format(x[0],x[1]) for x in steckerboard))

    return steckerboard

# Generate a list of random rotor
def generateRotors(count):
    rotors = []

    # Create count rotors
    for i in range(0, count):
        rotor = []
        alpha = deepcopy(AlphabetCustom.alphabet)

        # Randomly choose a letter and place it into the rotor
        while len(alpha) > 0:
            rand = random.randint(0, len(alpha) - 1)
            charA = alpha[rand]
            rotor.append(charA)
            alpha = alpha.replace(charA, '')

        rotors.append(rotor)

    with open(SpecificationFiles.rotorsOut, 'w+') as f:
        for line in rotors:
            line = ''.join(x for x in line)
            f.write('{0}\n'.format(line))

    return rotors

# Generate a list of characters that the rotors shift on
def generateKnocksOn(count):
    knocksOn = []

    # Create a knock on for each rotor
    for i in range(0, count):
        # Choose a character of our alphabet at random
        rand = random.randint(0, len(AlphabetCustom.alphabet) - 1)

        knocksOn.append(AlphabetCustom.alphabet[rand])

    with open(SpecificationFiles.knocksOnOut, 'w+') as f:
        for el in knocksOn:
            f.write(el + '\n')

    return knocksOn

# Generate a list of ints that the rotors shift by initially
def generateMessageSetting(count):
    messageSetting = []

    # Create a message setting per rotor
    for i in range(0, count):
        # Choose a random int within our alphabet
        rand = random.randint(0, len(AlphabetCustom.alphabet) - 1)
        messageSetting.append(str(rand))

    with open(SpecificationFiles.messageSettingOut, 'w+') as f:
        for el in messageSetting:
            f.write(el + '\n')

    return messageSetting

# Generate the message file if it has not yet been created
def generateMessageOutFile():
    if not os.path.isfile(SpecificationFiles.messageOut):
        with open(SpecificationFiles.messageOut, 'w+') as f:
            f.write('Please enter text in {0}'.format(SpecificationFiles.messageOut))

# Choose the number of rotors
numRotors = 5
optimal_tuples = 43

# Generate the specifications
reflector = generateReflector()
steckerboard = generateSteckerboard(optimal_tuples)
rotors = generateRotors(numRotors)
knocksOn = generateKnocksOn(numRotors)
messageSetting = generateMessageSetting(numRotors)
generateMessageOutFile()

debug = False
if debug:
    print(reflector)
    print(steckerboard)
    print(rotors)
    print(knocksOn)
    print(messageSetting)