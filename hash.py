from random import randrange
maxNume = 65535

choice = hex(randrange(maxNume))
choiseStr = str(choice).replace('0x','').upper()

while len(choiseStr) < 4:
    choiseStr = '0' + choiseStr
print(choiseStr)