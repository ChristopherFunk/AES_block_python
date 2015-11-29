
def getMsg(fileName):
    f = open(fileName)
    msg = f.read()
    msgL = []

    for byte in msg.split():
        byte = int(byte, 16)
        msgL.append(byte)

    f.close()

    return msgL


def getKey(fileName):
    f = open(fileName)
    key = f.read()
    keyL = []

    for byte in key.split():
        byte = int(byte, 16)
        keyL.append(byte)

    f.close()

    return keyL


def getMsgAndKey(args):
    msg = getMsg(args[1])
    key = getKey(args[2])

    return msg, key


def galMult(a, b):
    product = 0x00

    for i in range(8):
        if not (b & 0x01) == 0:
            product = product ^ a

        x = a & 0x80
        a = a << 1

        if not x == 0:
            a = a ^ 0x1b

        b = b >> 1

    return product & 0xff # python holds onto the shifted bits...
# end galMult


def xorMatricies(matrixOne, matrixTwo):
    xorMatrix = [[0x00 for x in range(4)] for x in range(4)]

    for row in range(4):
        for col in range(4):
            xorMatrix[row][col] = matrixOne[row][col] ^ matrixTwo[row][col]

    return xorMatrix
# end xorMatricies
