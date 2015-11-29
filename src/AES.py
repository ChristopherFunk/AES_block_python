from SBox import SBox
from Key import Key
import PrintHelper as PH
import Utils as utils

class Aes:
    def __init__(self, key):
        self.keySize = 128
        self.numRounds = 10
        # AES 128 Settings: (would normally be derived from keySize...)
        self.nk = 4 # from std...
        self.nr = 10 # from 128 bit def
        self.nb = 4 # from std...
        self.state = [[0x00 for x in range(4)] for x in range(4)]

        self.sbox = SBox()
        self.keyScheduler = Key(key, self.sbox, self.nk, self.nr, self.nb)
        self.keyScheduler.KeyExpansion()
    # end __init__


    def Cipher(self, msg):
        if msg == "":
            raise Exception("No Message to Encrypt...")

        self.initState(msg)
        self.AddRoundKey()

        for currRound in range(1, self.numRounds):
            self.SubBytes()
            self.ShiftRows()
            self.MixColumns()
            self.AddRoundKey()
        # end for

        # Do last round
        self.SubBytes()
        self.ShiftRows()
        self.AddRoundKey()

        return self.returnSingleLineHex()
    # end Cipher


    def EqInvCipher(self, cipher):
        if cipher == "":
            raise Exception("No CipherText to Encrypt...")

        self.initState(cipher)
        self.AddRoundKey(decrypt=True)

        for currRound in range(1, self.numRounds):
            self.InvShiftRows()
            self.InvSubBytes()
            self.AddRoundKey(decrypt=True)
            self.InvMixColumns()
        # end for

        # Do last round
        self.InvShiftRows()
        self.InvSubBytes()
        self.AddRoundKey(decrypt=True)

        return self.returnSingleLineHex()
    # end EqInvCipher


    def AddRoundKey(self, decrypt=False):
        nextKeys = [[]]
        subKey = [[0x00 for x in range(4)] for x in range(4)]

        if decrypt:
            nextKeys = self.keyScheduler.getInvNextRoundKey()
        else:
            nextKeys = self.keyScheduler.getNextRoundKey()

        for row in range(len(subKey)):
            for col in range(len(subKey)):
                subKey[col][row] = nextKeys[row][col]

        self.state = utils.xorMatricies(self.state, subKey)
    # end AddRoundKey


    def SubBytes(self):
        for row in range(4):
            for col in range(4):
                self.state[row][col] = self.sbox.SubByte(self.state[row][col])
    # end SubBytes


    def ShiftRows(self):
        for i in range(4):
            self.state[i] = self.state[i][i:] + self.state[i][:i]
    # end ShiftRows


    def MixColumns(self):
        tmpState = [[0x00 for x in range(4)] for x in range(4)]

        for col in range(4):
            tmpState[0][col] = utils.galMult(0x02, self.state[0][col]) ^ utils.galMult(0x03, self.state[1][col]) ^ self.state[2][col] ^ self.state[3][col]

            tmpState[1][col] = self.state[0][col] ^ utils.galMult(0x02, self.state[1][col]) ^ utils.galMult(0x03, self.state[2][col]) ^ self.state[3][col]

            tmpState[2][col] = self.state[0][col] ^ self.state[1][col] ^ utils.galMult(0x02, self.state[2][col]) ^ utils.galMult(0x03, self.state[3][col])

            tmpState[3][col] = utils.galMult(0x03, self.state[0][col]) ^ self.state[1][col] ^ self.state[2][col] ^ utils.galMult(0x02, self.state[3][col])

        self.state = tmpState
    # end MixColumns


    def InvSubBytes(self):
        for row in range(4):
            for col in range(4):
                self.state[row][col] = self.sbox.SubIVByte(self.state[row][col])
    # end SubBytes


    def InvShiftRows(self):
        for i in range(4):
            self.state[i] = self.state[i][-i:] + self.state[i][:-i]
    # end ShiftRows


    def InvMixColumns(self):
        tmpState = [[0x00 for x in range(4)] for x in range(4)]

        for col in range(4):
            tmpState[0][col] = utils.galMult(0x0e, self.state[0][col]) ^ utils.galMult(0x0b, self.state[1][col]) ^ utils.galMult(0x0d, self.state[2][col]) ^ utils.galMult(0x09, self.state[3][col])

            tmpState[1][col] = utils.galMult(0x09, self.state[0][col]) ^ utils.galMult(0x0e, self.state[1][col]) ^ utils.galMult(0x0b, self.state[2][col]) ^ utils.galMult(0x0d, self.state[3][col])

            tmpState[2][col] = utils.galMult(0x0d, self.state[0][col]) ^ utils.galMult(0x09, self.state[1][col]) ^ utils.galMult(0x0e, self.state[2][col]) ^ utils.galMult(0x0b, self.state[3][col])

            tmpState[3][col] = utils.galMult(0x0b, self.state[0][col]) ^ utils.galMult(0x0d, self.state[1][col]) ^ utils.galMult(0x09, self.state[2][col]) ^ utils.galMult(0x0e, self.state[3][col])

        self.state = tmpState
    # end MixColumns


    def initState(self, msg):
        msgIndex = 0

        for row in range(4):
            for col in range(4):
                self.state[col][row] = msg[msgIndex]
                msgIndex = msgIndex + 1
    # end initState


    def returnSingleLineHex(self):
        line = []
        for row in range(4):
            for col in range(4):
                line.append(self.state[col][row])
        return line
    # end returnSingleLineHex


    def loadSboxValues(self, sboxFile, inSboxFile):
        self.sbox.loadSbox(sboxFile)
        self.sbox.loadIVSbox(inSboxFile)

        # reload the key...
        self.keyScheduler.ReloadSbox(self.sbox)
    # end loadSboxValues
