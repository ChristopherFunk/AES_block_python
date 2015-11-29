# AES_block_python
My start of an AES implementation in python, for Comp 4140 (Introduction to Cryptography) and also for fun

DO NOT USE THIS FOR CRYPTO/SECURITY! This was a school project and is in no way a secure or usuable (or complete for that matter) implementation of AES. It was for school and for fun.
Again, DO NOT USE THIS FOR ANY CRYPTOGRAPHIC OR SECURITY PURPOSE!!! It is not secure!

To run with default everything:

	make

--or--

	./run.sh

otherwise, if you want to customize the msg and key (with optional Sbox's specified):

	python main.py [msg].txt [key].txt [[Sbox].txt [InverseSbox].txt]

Example: To run with msg, key, and both Sbox values:

	python main.py test1plaintext.txt test1key.txt aes_sbox.txt aes_inv_sbox.txt

Example: To run with just msg, key:

	python main.py test1plaintext.txt test1key.txt

to remove all .pyc files:

	make clean
