def prettyResultSmall(name, value, suffix=''):
    label = '{}:'.format(name)
    numbervalue = getSmallNumberValue(value)
    spaces = 16 - len(label) - len(numbervalue) - len(suffix)
    filler = ''
    if spaces > 0:
        filler = ' '*spaces
    return label + filler + numbervalue + suffix

def getSmallNumberValue(value):
    if(value > 100000):
        numbervalue = '{:>n}K'.format(round(value/1000.0))
    else:
        numbervalue = '{:>n}'.format(round(value))
    return numbervalue
