import AES
import random

def randomText(stringSize):
	string = ""

	for character in xrange(stringSize):
		string += str(unichr(random.randint(32, 126)))

	return string

def generateKeys(numKeys, size = 0):
	keys = []

	for keySize in range(1, numKeys + 1):
		key = randomText(keySize if (size == 0) else size)
		keys.append(key)

	return keys

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

	stateArray = randomText(16)

	formattedStateArray = AES.formatStateArray(stateArray)
	print(len(formattedStateArray))
	print(type(formattedStateArray[3]))
	print(formattedStateArray)

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

	stateArray = randomText(16)
	stateArray = AES.formatStateArray(stateArray)
	print(stateArray)

	rIndex = (stateArray[2] & byte1Mask) >> 20
	cIndex = ((stateArray[2] & byte1Mask) >> 16) & nibbleMask

	print("%x" % (stateArray[2]))
	print("(%x, %x)" % (rIndex, cIndex))

	newByte = int(AES.sBox[rIndex][cIndex], 16) << 16
	print(AES.sBox[rIndex][cIndex])

	stateArray = AES.subBytes(stateArray)
	print(stateArray)
	print("%x == %x") % ((stateArray[2] & byte1Mask), newByte)

	if((stateArray[2] & byte1Mask) == newByte):
		successes += 1
	else:
		failures += 1

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testShiftRows():
	successes = 0
	failures = 0

	print("Testing shiftRows functionality")

	stateArray = randomText(16)
	stateArray = AES.formatStateArray(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

	stateArray = AES.shiftRows(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

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

	stateArray = randomText(16)

	stateArray = AES.formatStateArray(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

	stateArray = AES.mixColumns(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

####################################################################################

def testInverseMixColumns():

	print("Testing inverseMixColumns functionality")

	stateArray = randomText(16)

	stateArray = AES.formatStateArray(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

	stateArray = AES.inverseMixColumns(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

####################################################################################

def testAddRoundKey():

	print("Testing addRoundKey functionality")

	stateArray = randomText(16)
	stateArray = AES.formatStateArray(stateArray)
	print("state: %x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

	roundKey = generateKeys(1, 256)
	roundKey = AES.formatKey(roundKey[0])
	print("key: %x %x %x %x %x %x %x %x" % (roundKey[0], roundKey[1], roundKey[2], roundKey[3],
											roundKey[4], roundKey[5], roundKey[6], roundKey[7]))

	stateArray = AES.addRoundKey(stateArray, roundKey)
	print("state: %x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

####################################################################################

def testEncrypt():

	print("Testing encrypt functionality")

	stateArray = randomText(16)
	stateArray = AES.formatStateArray(stateArray)

	key = generateKeys(1, 256)
	key = AES.formatKey(key[0])

	keySchedule = AES.expandKey(key)

	AES.encrypt(stateArray, keySchedule)

####################################################################################

def testInverseRotWord():

	print("Testing inverseRotWord functionality")

	word = random.randint(128000, 2048000000)
	print("%x" % (word))

	word = AES.inverseRotWord(word)
	print("%x" % (word))

####################################################################################

def testInverseShiftRows():
	successes = 0
	failures = 0

	print("Testing inverseShiftRows functionality")

	stateArray = randomText(16)
	stateArray = AES.formatStateArray(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

	stateArray = AES.inverseShiftRows(stateArray)
	print("%x %x %x %x" % (stateArray[0], stateArray[1], stateArray[2], stateArray[3]))

####################################################################################

def testInverseSubBytes():
	successes = 0
	failures = 0
	byte1Mask = int('00ff0000', 16)
	nibbleMask = int('0000000f', 16)

	print("Testing inverseSubBytes functionality")

	stateArray = randomText(16)
	stateArray = AES.formatStateArray(stateArray)
	print(stateArray)

	rIndex = (stateArray[2] & byte1Mask) >> 20
	cIndex = ((stateArray[2] & byte1Mask) >> 16) & nibbleMask

	print("%x" % (stateArray[2]))
	print("(%x, %x)" % (rIndex, cIndex))

	newByte = int(AES.inverseSBox[rIndex][cIndex], 16) << 16
	print(AES.inverseSBox[rIndex][cIndex])

	stateArray = AES.inverseSubBytes(stateArray)
	print(stateArray)
	print("%x == %x" % ((stateArray[2] & byte1Mask), newByte))

	if((stateArray[2] & byte1Mask) == newByte):
		successes += 1
	else:
		failures += 1

	print("Failures: %d Successes: %d" % (failures, successes))

####################################################################################

def testSBoxes():
	testVector = []
	successes = 0
	failures = 0

	print("Testing sBox and inverseSBox functionality")

	for x in xrange(64):
		testVector.append(((x * 4) << 24) | (((x * 4) + 1) << 16) | (((x * 4) + 2) << 8) | ((x * 4) + 3))
		testVector[x] = AES.subWord(testVector[x])
		testVector[x] = AES.inverseSubWord(testVector[x])

	for x in xrange(256):
		testByte = AES.extractByte(testVector[x / 4], x % 4)
		if(testByte == x):
			successes += 1
		else:
			failures += 1
			print("%d != %d" % (x, testByte))

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

#testKeyFormat()
#testRotWord()
#testInverseRotWord()
#testSubWord()
#testXTime()
#testRCon()
testExpandKey()
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