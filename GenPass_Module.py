from random import choice, shuffle, randrange

class Generating:
    def __init__(self):
        self.Characters()
        self.Combination()

    def Characters(self):
        characters = ":><?@#$%^&*()_+-=[]{}|;':\",./<>\\"
        random_characters = choice(characters)
        return random_characters

    def Combination(self):
        alphabet = "ABCDEFGHCHIJKLMNOPQRSTUVWXYZabcdefgjklmnopqrstuvwxyz012345689"
        random_combination = choice(alphabet)
        return random_combination

    def GenPass(self, lenght, chars):
        A = chars
        E = lenght
        retezec3 = []
        znaky2 = []
        for x in range(A):
            znak1 = Generating.Characters(1)
            znaky2.append(znak1)

        for w in range(E):
            string1 = Generating.Combination(2)
            retezec3.append(string1)

        for y in range(A):
            retezec3.pop()

        pocitadlo1 = 0
        for z in range(A):
            B1 = randrange(1, E + 1)
            B1 = B1 - 1
            zn1 = znaky2[pocitadlo1]
            retezec3.insert(B1, zn1)
            pocitadlo1 = pocitadlo1 + 1

        retezec4 = ""
        rete1 = retezec4.join(retezec3)
        return rete1
