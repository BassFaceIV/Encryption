import random
import sys
#import io

		# 0		1	  2		3	  4		5	  6		7	  8		9	  a 	b 	  c 	d  	  e 	f
sBox = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],	#0
		[0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],	#1
		[0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],	#2
		[0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],	#3
		[0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],	#4
		[0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],	#5
		[0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],	#6
		[0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],	#7
		[0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],	#8
		[0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],	#9
		[0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],	#a
		[0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],	#b
		[0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],	#c
		[0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],	#d
		[0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],	#e
		[0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]	#f

				# 0		1	  2		3	  4		5	  6		7	  8		9	  a 	b 	  c 	d  	  e 	f
inverseSBox = [[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],	#0
			   [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],	#1
			   [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],	#2
			   [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],	#3
			   [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],	#4
			   [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],	#5
			   [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],	#6
			   [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],	#7
			   [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],	#8
			   [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],	#9
			   [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],	#a
			   [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],	#b
			   [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],	#c
			   [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],	#d
			   [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],	#e
			   [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]]	#f

def formatKey(key):
	keyLength = len(key)
	newKey = ""
	formattedKey = []

	if(keyLength < 32):
		multiples = 32 / keyLength
		remainder = 32 % keyLength

		while(multiples):
			newKey += key
			multiples -= 1

		newKey += key[:remainder]
	elif(keyLength > 32):
		multiples = keyLength / 32
		remainder = keyLength % 32

		for x in range(32):
			newKey += key[random.randint(0, keyLength - 1)] #will need seed in future
	else:
		newKey = key;

	newKey = map(ord, newKey)

	for z in range(8):
		formattedKey.append(reduce(lambda x, y: (x << 8) + y, newKey[(z * 4): (z + 1) * 4]))

	return formattedKey

def formatStateArray(stateArray):
	newStateArray = []

	for z in range(4):
		newStateArray.append([stateArray[z], stateArray[z + 4], stateArray[z + 8], stateArray[z + 12]])

	return newStateArray

def subWord(word):
	nibbleMask = int('0000000f', 16)

	x0 = (word[0] >> 4) & nibbleMask
	x1 = (word[1] >> 4) & nibbleMask
	x2 = (word[2] >> 4) & nibbleMask
	x3 = (word[3] >> 4) & nibbleMask

	y0 = word[0] & nibbleMask
	y1 = word[1] & nibbleMask
	y2 = word[2] & nibbleMask
	y3 = word[3] & nibbleMask

	word[0] = sBox[x0][y0]
	word[1] = sBox[x1][y1]
	word[2] = sBox[x2][y2]
	word[3] = sBox[x3][y3]

	return word

def inverseSubWord(word):
	nibbleMask = int('0000000f', 16)

	x0 = (word[0] >> 4) & nibbleMask
	x1 = (word[1] >> 4) & nibbleMask
	x2 = (word[2] >> 4) & nibbleMask
	x3 = (word[3] >> 4) & nibbleMask

	y0 = word[0] & nibbleMask
	y1 = word[1] & nibbleMask
	y2 = word[2] & nibbleMask
	y3 = word[3] & nibbleMask

	word[0] = inverseSBox[x0][y0]
	word[1] = inverseSBox[x1][y1]
	word[2] = inverseSBox[x2][y2]
	word[3] = inverseSBox[x3][y3]

	return word

def rotWord(word, offset = 1):
	for x in range(4 * offset):
		if(x % 4 == 0):
			temp = word[0]
		if(x % 4 == 3):
			word[x % 4] = temp
		else:
			word[x % 4] = word[(x + 1) % 4]

	return word

def inverseRotWord(word, offset = 1):
	for x in range(-1, (4 * -offset) - 1, -1):
		if(x % 4 == 3):
			temp = word[-1]
		if(x % 4 == 0):
			word[0] = temp
		else:
			word[x % 4] = word[(x - 1) % 4]

	return word

def xTime(value):
	if(value == 1):
		return 1
	else:
		rcon = xTime(value - 1)
		return ((rcon << 1) ^ (int('0x11b', 16) & -(rcon >> 7)))

def rCon(iteration):
	rc = xTime(iteration)

	return rc


def expandKey(key):
	keySchedule = []
	tempKeySchedule = []
	finalKeySchedule = []
	iteration = 1

	for roundNum in range(15):
		for word in range(4):
			indexStart = (roundNum * 16) + (word * 4)

			if(roundNum < 2):
				for byte in range(4):
					keySchedule.append(key[indexStart + byte])
			else:
				if(word == 0):
					if(roundNum % 2):
						temp = subWord(keySchedule[indexStart - 4 : indexStart])
					else:
						temp = subWord(rotWord(keySchedule[indexStart - 4 : indexStart]))
						temp[0] = temp[0] ^ rCon(iteration)
						iteration += 1
				else:
					temp = keySchedule[indexStart - 4 : indexStart]
				for x in range(4):
					keySchedule.append(temp[x] ^ keySchedule[indexStart - 32 : indexStart - 28][x])
			tempKeySchedule.append(keySchedule[indexStart : indexStart + 16])
		finalKeySchedule.append(tempKeySchedule[(roundNum * 4) : ((roundNum + 1) * 4)])

	return finalKeySchedule

def subBytes(stateArray):
	index = 0

	for word in stateArray:
		stateArray[index] = subWord(word)
		index += 1

	return stateArray

def inverseSubBytes(stateArray):
	index = 0

	for word in stateArray:
		stateArray[index] = inverseSubWord(word)
		index += 1

	return stateArray

def shiftRows(stateArray):
	offset = 0

	for word in stateArray:
		stateArray[offset] = rotWord(word, offset)
		offset += 1

	return stateArray

def inverseShiftRows(stateArray):
	offset = 0

	for word in stateArray:
		stateArray[offset] = inverseRotWord(word, offset)
		offset += 1

	return stateArray

def gf2ModularDouble(multiplicand):
	return (multiplicand << 1) ^ (int('0x11b', 16) & -(multiplicand >> 7))

def mixColumns(stateArray):
	newStateArray = [[], [], [], []]

	for column in range(4):
		newStateArray[0].append(gf2ModularDouble(stateArray[0][column]) ^
								gf2ModularDouble(stateArray[1][column]) ^
								stateArray[1][column] ^
								stateArray[2][column] ^
								stateArray[3][column])

		newStateArray[1].append(gf2ModularDouble(stateArray[1][column]) ^
								gf2ModularDouble(stateArray[2][column]) ^
								stateArray[2][column] ^
								stateArray[3][column] ^
								stateArray[0][column])

		newStateArray[2].append(gf2ModularDouble(stateArray[2][column]) ^
								gf2ModularDouble(stateArray[3][column]) ^
								stateArray[3][column] ^
								stateArray[0][column] ^
								stateArray[1][column])

		newStateArray[3].append(gf2ModularDouble(stateArray[3][column]) ^
								gf2ModularDouble(stateArray[0][column]) ^
								stateArray[0][column] ^
								stateArray[1][column] ^
								stateArray[2][column])

	return newStateArray

def inverseMixColumns(stateArray):
	newStateArray = [[], [], [], []]

	for column in range(4):
		newStateArray[0].append(gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[0][column]) ^ stateArray[0][column]) ^ stateArray[0][column]) ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[1][column])) ^ stateArray[1][column]) ^ stateArray[1][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[2][column]) ^ stateArray[2][column])) ^ stateArray[2][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[3][column]))) ^ stateArray[3][column])

		newStateArray[1].append(gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[1][column]) ^ stateArray[1][column]) ^ stateArray[1][column]) ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[2][column])) ^ stateArray[2][column]) ^ stateArray[2][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[3][column]) ^ stateArray[3][column])) ^ stateArray[3][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[0][column]))) ^ stateArray[0][column])

		newStateArray[2].append(gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[2][column]) ^ stateArray[2][column]) ^ stateArray[2][column]) ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[3][column])) ^ stateArray[3][column]) ^ stateArray[3][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[0][column]) ^ stateArray[0][column])) ^ stateArray[0][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[1][column]))) ^ stateArray[1][column])

		newStateArray[3].append(gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[3][column]) ^ stateArray[3][column]) ^ stateArray[3][column]) ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[0][column])) ^ stateArray[0][column]) ^ stateArray[0][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[1][column]) ^ stateArray[1][column])) ^ stateArray[1][column] ^
								gf2ModularDouble(gf2ModularDouble(gf2ModularDouble(stateArray[2][column]))) ^ stateArray[2][column])

	return newStateArray

def addRoundKey(stateArray, roundKeys):
	for word in range(4):
		for byte in range(4):
			stateArray[byte][word]  ^= roundKeys[word][byte]

	return stateArray

def encrypt(stateArray, keySchedule):
	stateArray = addRoundKey(stateArray, keySchedule[0])
	
	for roundNum in range(13):
		stateArray = subBytes(stateArray)
		stateArray = shiftRows(stateArray)
		stateArray = mixColumns(stateArray)
		stateArray = addRoundKey(stateArray, keySchedule[roundNum + 1])

	stateArray = subBytes(stateArray)
	stateArray = shiftRows(stateArray)
	stateArray = addRoundKey(stateArray, keySchedule[14])

	return stateArray

def decrypt(stateArray, keySchedule):
	stateArray = addRoundKey(stateArray, keySchedule[14])

	for roundNum in range(13):
		stateArray = inverseShiftRows(stateArray)
		stateArray = inverseSubBytes(stateArray)
		stateArray = addRoundKey(stateArray, keySchedule[13 - roundNum])
		stateArray = inverseMixColumns(stateArray)

	stateArray = inverseShiftRows(stateArray)
	stateArray = inverseSubBytes(stateArray)
	stateArray = addRoundKey(stateArray, keySchedule[0])

	return stateArray

def formatOutputStateArray(stateArray):
	outputStateArray = []

	for z in range(4):
		outputStateArray.append([stateArray[0][z], stateArray[1][z], stateArray[2][z], stateArray[3][z]])

	return outputStateArray

#add ctr or cbc modes of operation to handle imperfect block sizes

def aes(filename, option):
	byte3Mask = int('000000ff', 16)
	error = False
	chunk = 0

	password = raw_input("Enter Password: ")
	passwordConfirm = raw_input("confirm Password: ")
	if(password != passwordConfirm):
		print("Passwords did not match. Aborting...")
	else:
		key = formatKey(password)
		for word in key:
			print("%x" % (word),)
		keySchedule = expandKey(key)
		for key in keySchedule:
			for word in key:
				print("%x" % (word),)
			print("\n")

		with open(filename, 'rb') as f_in:
			state = f_in.read(16)

			while (state != "") and (error == False):
				if(len(state) < 16):
					state = formatPlainText(state)
				state = formatStateArray(state)

				if(option.lower() == 'e'):
					print("Encrypting chunk %d" % (chunk))
					encryptedState = encrypt(state, keySchedule)

					encryptedState = formatOutput(encryptedState)

					with open(filename + '.aes', 'ab') as f_out:
						#f_out.write(encryptedState)
						for word in encryptedState:
							f_out.write(chr((word >> 24) & byte3Mask))
							f_out.write(chr((word >> 16) & byte3Mask))
							f_out.write(chr((word >> 8) & byte3Mask))
							f_out.write(chr(word & byte3Mask))
					f_out.close()

				elif(option.lower() == 'd'):
					print("Decrypting chunk %d" % (chunk))
					decryptedState = decrypt(state, keySchedule)

					decryptedState = formatOutput(decryptedState)

					with open(filename.rstrip('.aes'), 'ab') as f_out:
						for word in decryptedState:
							#might need to convert in and out of beginning and final text differently
							f_out.write(chr((word >> 24) & byte3Mask))
							f_out.write(chr((word >> 16) & byte3Mask))
							f_out.write(chr((word >> 8) & byte3Mask))
							f_out.write(chr(word & byte3Mask))
					f_out.close()
				else:
					print("Option unavailable")
					error = True

				chunk += 1
				state = f_in.read(16)
		f_in.close()

#aes(sys.argv[1], sys.argv[2])