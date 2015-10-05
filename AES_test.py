import AES
import random

def randomText(stringSize):
	string = ""

	for character in range(stringSize):
		string += str(chr(random.randint(32, 126)))

	return string

def generateKeys(numKeys, size = 0):
	keys = []

	for keySize in range(1, numKeys + 1):
		key = randomText(keySize if (size == 0) else size)
		keys.append(key)

	return keys

def randomBytes(numBytes):
	bytestring = bytearray([])

	for x in range(numBytes):
		bytestring.append(random.randint(0, 255))

####################################################################################

def testKeyFormat():
	keys = []
	successes = 0;
	failures = 0;

	print("Testing keyFormat functionality")

	keys = generateKeys(1000)

	for key in keys:

		#print "Converting key size of %d bytes: " % (len(key)),
		formattedKey = AES.formatKey(key)
		print("%x") % len(formattedKey)
		print("%x") % type(formattedKey[7])
		print("%x") % formattedKey

		if((len(formattedKey) == 8) and (type(formattedKey[7]) is int)):
			#print "success"
			successes += 1
		else:
			#print "failure"
			failures += 1


	print("Failures: %d Successes: %d") % (failures, successes)

####################################################################################

def testPlainTextFormat():
	textSamples = []
	successes = 0
	failures = 0

	print("Testing plainTextFormat functionality")

	for textSize in range(1, 10001):
		plainText = randomText(textSize)
		textSamples.append(AES.formatPlainText(plainText))

		blocks = textSamples[textSize - 1]
		predictedNumBlocks = textSize / 16
		predictedNumBlocks += 1 if (textSize % 16) else 0
		actualNumBlocks = 0

		#print "Converting plainText of size %d bytes into blocks of size 16 bytes: " % (textSize)
		accuracy = 1
		for block in blocks:
			if(len(block) != 16):
				accuracy = 0
			actualNumBlocks += 1

		if(accuracy and (actualNumBlocks == predictedNumBlocks)):
			#print "success"
			successes += 1
		else:
			#print "failure"
			print("%d: %d != %d") % (textSize, actualNumBlocks, predictedNumBlocks)
			failures += 1

	print("Failures: %d Successes: %d") % (failures, successes)

####################################################################################

def testRotWord():
	word = ""
	byte0Mask = int('ff000000', 16)
	byte1Mask = int('00ff0000', 16)
	byte2Mask = int('0000ff00', 16)
	byte3Mask = int('000000ff', 16)

	print("Testing rotWord functionality")

	#for character in xrange(4):
	#	word += str(unichr(random.randint(32, 126)))

	word = random.randrange(int('ffffffff', 16))

	newWord = AES.rotWord(word)

	print("%x : %x") % (word, newWord)

	if(((newWord & byte0Mask) == ((word & byte1Mask) << 8)) and
	   ((newWord & byte1Mask) == ((word & byte2Mask) << 8)) and
	   ((newWord & byte2Mask) == ((word & byte3Mask) << 8)) and
	   ((newWord & byte3Mask) == ((word & byte0Mask) >> 24))):
		print("success")
	else:
		print("failure")

####################################################################################

def testSubWord():
	word = bytearray([])

	print("Testing subWord functionality")

	#for character in xrange(4):
	#	word += str(unichr(random.randint(32, 126)))

	for x in range(4):
		word.append(random.randrange(255))

	print(word)
	newWord = AES.subWord(word)

	print(newWord)

####################################################################################

def testXTime():
	for x in xrange(1, 256):
		value = AES.xTime(x)
		print("%x => %x") % (x, value)

####################################################################################

def testRCon():
	for x in xrange(1, 60):
		value = AES.rCon(x)
		print("%x => %x : %x") % (x, value, value >> 24)

####################################################################################

def testExpandKey():
	keys = []
	successes = 0
	failures = 0
	keyNumber = 0

	print("Testing expandKey functionality")

	#keys = generateKeys(1000, 256)
	key = bytes([0x60, 0x3d, 0xeb, 0x10,
				 0x15, 0xca, 0x71, 0xbe,
				 0x2b, 0x73, 0xae, 0xf0,
				 0x85, 0x7d, 0x77, 0x81,
				 0x1f, 0x35, 0x2c, 0x07,
				 0x3b, 0x61, 0x08, 0xd7,
				 0x2d, 0x98, 0x10, 0xa3,
				 0x09, 0x14, 0xdf, 0xf4])
	keys = [key]
	#print(keys)
	for key in keys:
		#key = AES.formatKey(key)
		keySchedule = AES.expandKey(key)

		print("Key %d: " % (keyNumber))
		#print(len(keySchedule[0]))
		x = 0
		for roundKey in keySchedule:
			print("%d: %x %x %x %x" % (x, roundKey[0], roundKey[1], roundKey[2], roundKey[3]))
			#print("%d: %x" % (x, roundKey))
			#print(roundKey)
			x += 1
		keyNumber += 1
		if((len(keySchedule) * len(keySchedule[0]) == 60) and (type(keySchedule[0][0]) is int)):
			successes += 1
		else:
			failures += 1

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testFormatStateArray():
	successes = 0
	failures = 0

	print("Testing formatStateArray functionality")

	stateArray = bytes([0x32, 0x43, 0xf6, 0xa8,
						0x88, 0x5a, 0x30, 0x8d,
						0x31, 0x31, 0x98, 0xa2,
						0xe0, 0x37, 0x07, 0x34])

	formattedStateArray = AES.formatStateArray(stateArray)
	for word in formattedStateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	if((len(formattedStateArray) == 4) and (type(formattedStateArray[3]) is int)):
		testWord = [ord(stateArray[2]), ord(stateArray[6]), ord(stateArray[10]), ord(stateArray[14])]
		testWord = reduce(lambda x, y: (x << 8) + y, testWord)
		print(testWord)
		if(testWord == formattedStateArray[2]):
			successes += 1
		else:
			failures += 1
	else:
		failures += 1

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testSubBytes():
	successes = 0
	failures = 0
	byte1Mask = int('00ff0000', 16)
	nibbleMask = int('0000000f', 16)

	print("Testing subBytes functionality")

	stateArray = bytes([0x32, 0x43, 0xf6, 0xa8,
						0x88, 0x5a, 0x30, 0x8d,
						0x31, 0x31, 0x98, 0xa2,
						0xe0, 0x37, 0x07, 0x34])

	stateArray = AES.formatStateArray(stateArray)
	print("State In:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	#rIndex = (stateArray[2] & byte1Mask) >> 20
	#cIndex = ((stateArray[2] & byte1Mask) >> 16) & nibbleMask

	#print("%x" % (stateArray[2]))
	#print("(%x, %x)" % (rIndex, cIndex))

	#newByte = int(AES.sBox[rIndex][cIndex], 16) << 16
	#print(AES.sBox[rIndex][cIndex])

	stateArray = AES.subBytes(stateArray)
	print("State Out:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))
	#print("%x == %x") % ((stateArray[2] & byte1Mask), newByte)

	#if((stateArray[2] & byte1Mask) == newByte):
	#	successes += 1
	#else:
	#	failures += 1

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testShiftRows():
	successes = 0
	failures = 0

	print("Testing shiftRows functionality")

	stateArray = bytes([0x32, 0x43, 0xf6, 0xa8,
						0x88, 0x5a, 0x30, 0x8d,
						0x31, 0x31, 0x98, 0xa2,
						0xe0, 0x37, 0x07, 0x34])
	stateArray = AES.formatStateArray(stateArray)
	print("State In:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	stateArray = AES.shiftRows(stateArray)
	print("State Out:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testGF2ModularDouble():

	print("Testing gf2ModularDouble functionality")

	words = generateKeys(1, 256)
	words = AES.formatKey(words[0])

	for word in words:
		doubledByte0 = AES.gf2ModularDouble(AES.extractByte(word, 0))
		quadrupledByte0 = AES.gf2ModularDouble(doubledByte0)
		print("(%x * 2 = %x) * 2 = %x" % (AES.extractByte(word, 0), doubledByte0, quadrupledByte0))

####################################################################################

def testExtractByte():

	print("Testing extractByte functionality")

	words = generateKeys(1, 256)
	words = AES.formatKey(words[0])

	for word in words:
		byte0 = AES.extractByte(word, 0)
		byte1 = AES.extractByte(word, 1)
		byte2 = AES.extractByte(word, 2)
		byte3 = AES.extractByte(word, 3)

		print("%x: %x %x %x %x" % (word, byte0, byte1, byte2, byte3))

####################################################################################

def testMixColumns():

	print("Testing mixColumns functionality")

	stateArray = bytes([0x00, 0x11, 0x22, 0x33,
						0x44, 0x55, 0x66, 0x77,
						0x88, 0x99, 0xaa, 0xbb,
						0xcc, 0xdd, 0xee, 0xff])

	stateArray = AES.formatStateArray(stateArray)
	print("State In:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	stateArray = AES.mixColumns(stateArray)
	print("State Out:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testInverseMixColumns():

	print("Testing inverseMixColumns functionality")

	stateArray = [0x8e, 0xa2, 0xb7, 0xca,
				  0x51, 0x67, 0x45, 0xbf,
				  0xea, 0xfc, 0x49, 0x90,
				  0x4b, 0x49, 0x60, 0x89]

	stateArray = AES.formatStateArray(stateArray)
	print("State In:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	stateArray = AES.inverseMixColumns(stateArray)
	print("State Out:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testAddRoundKey():

	print("Testing addRoundKey functionality")

	stateArray = bytes([0x00, 0x11, 0x22, 0x33,
						0x44, 0x55, 0x66, 0x77,
						0x88, 0x99, 0xaa, 0xbb,
						0xcc, 0xdd, 0xee, 0xff])
	stateArray = AES.formatStateArray(stateArray)

	key = bytes([0x00, 0x01, 0x02, 0x03,
				 0x04, 0x05, 0x06, 0x07,
				 0x08, 0x09, 0x0a, 0x0b,
				 0x0c, 0x0d, 0x0e, 0x0f,
				 0x10, 0x11, 0x12, 0x13,
				 0x14, 0x15, 0x16, 0x17,
				 0x18, 0x19, 0x1a, 0x1b,
				 0x1c, 0x1d, 0x1e, 0x1f])

	#roundKey = generateKeys(1, 256)
	#key = AES.formatKey(key)
	keySchedule = AES.expandKey(key)

	print(keySchedule)

	for roundKeys in keySchedule:
		for key in roundKeys:
			print("key: %x %x %x %x" % (key[0], key[1], key[2], key[3]))

	stateArray = AES.addRoundKey(stateArray, keySchedule[0])
	for word in stateArray:
		print("state: %x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testEncrypt():

	print("Testing encrypt functionality")

	stateArray = bytes([0x00, 0x11, 0x22, 0x33,
						0x44, 0x55, 0x66, 0x77,
						0x88, 0x99, 0xaa, 0xbb,
						0xcc, 0xdd, 0xee, 0xff])
	stateArray = AES.formatStateArray(stateArray)

	print("Input State Array:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	key = bytes([0x00, 0x01, 0x02, 0x03,
				 0x04, 0x05, 0x06, 0x07,
				 0x08, 0x09, 0x0a, 0x0b,
				 0x0c, 0x0d, 0x0e, 0x0f,
				 0x10, 0x11, 0x12, 0x13,
				 0x14, 0x15, 0x16, 0x17,
				 0x18, 0x19, 0x1a, 0x1b,
				 0x1c, 0x1d, 0x1e, 0x1f])

	keySchedule = AES.expandKey(key)

	stateArray = AES.encrypt(stateArray, keySchedule)

	print("Output State Array:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testInverseRotWord():
	word = []

	print("Testing inverseRotWord functionality")

	word = bytearray([0x10, 0x34, 0xfa, 0x4b])

	print("Input Word:")
	#print(word)
	print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	word = AES.inverseRotWord(word, 2)
	print("Output Word:")
	print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testInverseShiftRows():
	successes = 0
	failures = 0

	print("Testing inverseShiftRows functionality")

	stateArray = bytearray([0x8e, 0xa2, 0xb7, 0xca,
							0x51, 0x67, 0x45, 0xbf,
							0xea, 0xfc, 0x49, 0x90,
							0x4b, 0x49, 0x60, 0x89])
	stateArray = AES.formatStateArray(stateArray)
	print("State In:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	stateArray = AES.inverseShiftRows(stateArray)
	print("State Out:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

####################################################################################

def testInverseSubBytes():
	successes = 0
	failures = 0
	byte1Mask = int('00ff0000', 16)
	nibbleMask = int('0000000f', 16)

	print("Testing inverseSubBytes functionality")

	stateArray = bytearray([0x8e, 0xa2, 0xb7, 0xca,
							0x51, 0x67, 0x45, 0xbf,
							0xea, 0xfc, 0x49, 0x90,
							0x4b, 0x49, 0x60, 0x89])
	stateArray = AES.formatStateArray(stateArray)
	print("State In:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	#rIndex = (stateArray[2] & byte1Mask) >> 20
	#cIndex = ((stateArray[2] & byte1Mask) >> 16) & nibbleMask

	#print("%x" % (stateArray[2]))
	#print("(%x, %x)" % (rIndex, cIndex))

	#newByte = int(AES.sBox[rIndex][cIndex], 16) << 16
	#print(AES.sBox[rIndex][cIndex])

	stateArray = AES.inverseSubBytes(stateArray)
	print("State Out:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testSBoxes():
	testVector = []
	resultVector = []
	successes = 0
	failures = 0

	print("Testing sBox and inverseSBox functionality")

	for x in range(256):
		testVector.append(x)

	testVector = bytearray(testVector)

	for x in range(0, 256, 4):
		resultVector.append(AES.subWord(testVector[x : x + 4]))

	print(resultVector[32])

	for x in range(64):
		resultVector.append(AES.inverseSubWord(resultVector[x]))

	print(resultVector[32])

	for x in range(0, 256, 4):
		testByte0 = resultVector[int(x / 4)][x % 4]
		#testByte1 = resultVector[x / 4][1]
		#testByte2 = resultVector[x / 4][2]
		#testByte3 = resultVector[x / 4][3]
		#if((testByte0 == x) and (testByte1 == x) and (testByte2 == x) and (testByte3 == x)):
		if(testByte0 == x):
			successes += 1
		else:
			failures += 1
			print("%x != %x" % (testByte0, x))
			#print("%x != %x or %x != %x or %x != %x or %x != %x" % (x, testByte0, x + 1, testByte1, x + 2, testByte2, x + 3, testByte3))

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testRetrieveInputBytes():
	with open('test1.txt', 'rb') as fp_in:
		state = fp_in.read(16)
		print(bytes([int(state[0]) + 1, int(state[1]) + 150]))
	fp_in.close()
	with open('test1.txt', 'ab') as fp_out:
		outputBytes = bytes([int(state[0]) + 150])
		fp_out.write(outputBytes)
	fp_out.close()

####################################################################################

def testAES():
	print("Testing AES Encryption and Decryption")

	key = [0x00, 0x01, 0x02, 0x03,
		   0x04, 0x05, 0x06, 0x07,
		   0x08, 0x09, 0x0a, 0x0b,
		   0x0c, 0x0d, 0x0e, 0x0f,
		   0x10, 0x11, 0x12, 0x13,
		   0x14, 0x15, 0x16, 0x17,
		   0x18, 0x19, 0x1a, 0x1b,
		   0x1c, 0x1d, 0x1e, 0x1f]

	stateArray = [0x00, 0x11, 0x22, 0x33,
				  0x44, 0x55, 0x66, 0x77,
				  0x88, 0x99, 0xaa, 0xbb,
				  0xcc, 0xdd, 0xee, 0xff]
	stateArray = AES.formatStateArray(stateArray)

	print("Plaintext State Array:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	keySchedule = AES.expandKey(key)

	stateArray = AES.encrypt(stateArray, keySchedule)

	print("Encrypted State Array:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

	stateArray = AES.decrypt(stateArray, keySchedule)

	stateArray = AES.formatOutputStateArray(stateArray)

	print("Decrypted State Array:")
	for word in stateArray:
		print("%x %x %x %x" % (word[0], word[1], word[2], word[3]))

#testKeyFormat()
#testRotWord()
#testInverseRotWord()
#testSubWord()
#testXTime()
#testRCon()
#testExpandKey()
#testPlainTextFormat()
#testFormatStateArray()
#testSubBytes()
#testInverseSubBytes()
#testShiftRows()
#testInverseShiftRows()
#testGF2ModularDouble()
#testExtractByte()
#testMixColumns()
#testInverseMixColumns()
#testAddRoundKey()
#testEncrypt()
#testSBoxes()
#testRetrieveInputBytes()
testAES()