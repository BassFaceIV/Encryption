#include <stdio.h>
#include <string.h>
#include <math.h>

void copyBytes(char * wordSource, char * wordDestination){
	int index;

	for(index = 0; index < 4; index++){
		wordDestination[index] = wordSource[index];
	}
}

char ** formatKey(char * password){
	int length;
	int index;
	char key[8][4];

	length = strlen(password);

	for(column = 0; column < 8; column++){
		for(row = 0; row < 4; row++){
			key[column][row] = password[(column * 4) + row];
		}
	}

	if(length > 32){

		for(index = 32; index < length; index++){
			key[index / 8][index % 4] = key[index / 8][index % 4] ^ password[index];
		}
	}
	else if(length < 32){
		for(index = 0; index < 32; index++){
			key[(length + index) / 8][(index + length) % 4] = password[index];
		}
	}

	return key;
}

void rotateWords(char keyWord[4]){
	int index;
	char byte;

	byte = keyWord[0];
	keyWord[0] = keyWord[1];
	keyWord[1] = keyWord[2];
	keyWord[2] = keyWord[3];
	keyWord[3] = byte;
}

void substituteBytes(char keyWord[4]){
	int index;
	int row;
	int column;

	for(index = 0; index < 4; index++){
		row = (int)((keyWord[index] >> 4) & 0x0F);
		column = (int)(keyWord[index] & 0x0F);
		keyWord[index] = lookupTable[row][column];
	}
}

int roundConstant(int j){
	if(j = 1){
		return 1;
	}
	return (2 * roundConstant(j - 1));
}

void g(char keyWord[4], roundNumber){
	rotateWords(keyWord);
	substituteBytes(keyWord);
	keyWord[0] = keyWord[0] ^ (char)roundConstant(roundNumber);
}

void expandKey(char key[8][4], char keySchedule[60][4]){
	int word;
	char * gKeyWord;
	char * newBytes;

	for(word = 0; word < 8; word++){
		copyBytes(key[word], keySchedule[word]);
	}

	for(word = 8; word < 60; word++){
		if(word % 8 == 0){
			gKeyWord = keySchedule[word - 1];
			g(gKeyWord);
			keySchedule[word][0] = keySchedule[word - 8][0] ^ gKeyWord[0];
			keySchedule[word][1] = keySchedule[word - 8][1] ^ gKeyWord[1];
			keySchedule[word][2] = keySchedule[word - 8][2] ^ gKeyWord[2];
			keySchedule[word][3] = keySchedule[word - 8][3] ^ gKeyWord[3];
		}
		else if(((word % 8) - 4) == 0){
			newBytes = substituteBytes(keySchedule[word - 1]);
			keySchedule[word][0] = newBytes[0] ^ keySchedule[word - 8][0];
			keySchedule[word][1] = newBytes[1] ^ keySchedule[word - 8][1];
			keySchedule[word][2] = newBytes[2] ^ keySchedule[word - 8][2];
			keySchedule[word][3] = newBytes[3] ^ keySchedule[word - 8][3];
		}
		else{
			keySchedule[word][0] = keySchedule[word - 1][0] ^ keySchedule[word - 8][0];
			keySchedule[word][1] = keySchedule[word - 1][1] ^ keySchedule[word - 8][1];
			keySchedule[word][2] = keySchedule[word - 1][2] ^ keySchedule[word - 8][2];
			keySchedule[word][3] = keySchedule[word - 1][3] ^ keySchedule[word - 8][3];
		}
	}
}

void getNextStateArray(FILE * fp, char stateArray[4][4]){
	int column;
	int row;
	int character;

	for(column = 0; column < 4; column++){
		for(row = 0; row < 4; row++){
			stateArray[column][row] = (!feof(fp)) ? (char)fgetc(fp) : NULL;
		}
	}
}

void main(int argc, char * argv[]){
	FILE * fp_read;
	FILE * fp_write;
	char key[8][4];
	char keySchedule[60][4]
	char stateArray[4][4];

	key = formatKey(argv[2]);
	expandKey(key, keySchedule);

	fp_read = fopen(argv[1], "r");

	while(!feof(fp)){
		getNextStateArray(fp_read, stateArray);
	}
}