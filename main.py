from src.SBox import SBox
from src.AES import Aes
from src import PrintHelper as PH
import src.Utils as utils
import sys


def validateArgs():
    # args: msg, key
    if (len(sys.argv) != 3 and len(sys.argv) != 5) or not ".txt" in sys.argv[1] or not ".txt" in sys.argv[2]:
        print "Program takes [msg file].txt and [key file].txt as arguments, with the option of [[Sbox].txt [InverseSbox].txt]"
        sys.exit()
# end validateArgs


def displayResults(msg, cipher, msg_dec):
    print "Original Msg: ",
    PH.printHexString(msg)
    print "Cipher Text : ",
    PH.printHexString(cipher)
    print "Plain Text  : ",
    PH.printHexString(msg_dec)
# end displayResults


def main():
    validateArgs()
    msg, key = utils.getMsgAndKey(sys.argv)
    aes = Aes(key)

    if len(sys.argv) == 5:
        print "Loading Sbox Values: " + str(sys.argv[3]) + ", " + str(sys.argv[4])
        aes.loadSboxValues(sys.argv[3], sys.argv[4])

    cipher = aes.Cipher(msg)
    msg_dec = aes.EqInvCipher(cipher)

    displayResults(msg, cipher, msg_dec)
# end main


main()
