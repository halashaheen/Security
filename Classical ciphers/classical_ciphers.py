import math
import string
import sys
import numpy as np
"""
    Caesar_Cipher Function : 
	input : plaintext,key
	output : ciphertext after applying the algorithm
	explanation : The main operation is getting the order of the character then adding the key to this order
    (mod26 as we have 26 char) 
    then getting the character of the new order.
"""
def Caesar_Cipher(plaintext,key):
    ciphertext = "" 

    for i in plaintext:
        #not a character , pass it 
        if (i == '\n'):
            continue
        else:
            char = i 
            # encryption of uppercase characters
            if (char.isupper()): 
                ciphertext += chr((ord(char) + key-65) % 26 + 65) 
            # encryption of lowercase characters
            else: 
                ciphertext += chr((ord(char) + key - 97) % 26 + 97) 
    #to return the ciphertext in uppercase as in the slides
    ciphertext=ciphertext.upper()
    return ciphertext
"""
    find_position Function : 
	input : playfair_matrix,character
	output : the row and column numbers of the character given
	explanation : helper function for the playfair cipher
"""
#helper function for the playfair cipher, it takes the matrix and the character and returns its row and column numbers
def find_position(playfair_matrix,character):
	x=y=0
	for i in range(5):
		for j in range(5):
			if playfair_matrix[i][j]==character:
				x=i
				y=j

	return x,y
"""
    Play_Fair_Cipher : 
	input : plaintext,keyword
	output : the ciphertext after applying the algorithm
	explanation : 1.The Algorithm consistes of 2 steps:
    Generate the key Square(5×5)
    2.Algorithm to encrypt the plain text: The plaintext is split into pairs of two letters.
    If there is an odd number of letters, a  X is added to the last letter.
"""
def Play_Fair_Cipher(plaintext,keyword):
    #empty matrix to construct the playfair matrix
    matrix=[]
    plaintext=plaintext.upper()
    #if there is any spaces in the plaintext
    plaintext = plaintext.replace(" ","")
    #J is equal to I
    plaintext = plaintext.replace("J","I")
    keyword=keyword.upper()
    #if there is any spaces in the keyword
    keyword = keyword.replace(" ","")
    alpha='abcdefghijklmnopqrstuvwxyz'
    alpha=alpha.upper()
    
    #fill the matrix with the keyword
    for e in keyword.upper():
        #to discard duplicates 
        if e not in matrix:
            matrix.append(e)

    #fill the remaining places in the matrix with alphabets
    for e in alpha:
        #to discard duplicates 
        if e not in matrix:
            #I and J are the same
            if e=='J':
                continue
            else:
                matrix.append(e)
    #reshaping the list to be look like a 5x5 matrix
    keyword_matrix=[]
    for e in range(5):
        keyword_matrix.append('')
        
    keyword_matrix[0]=matrix[0:5]
    keyword_matrix[1]=matrix[5:10]
    keyword_matrix[2]=matrix[10:15]
    keyword_matrix[3]=matrix[15:20]
    keyword_matrix[4]=matrix[20:25]

    #formatting the plaintext in a list
    message=[]
    for  character in plaintext:
        message.append(character)
    i=0
    l=int(len(message)/2)
    for j in range(l):
        #if there is a repeated consecutive character insert X between them
        if message[i] == message[i+1]:
            message.insert(i+1,'X')
        i=i+2
    #if there is  remaining 1 character (odd length) insert X in the end
    if len(message)%2==1:
        message.append("X")

    #the final version of the message, putting the 2 characters together
    i=0
    new_message=[]
    l=int(len(message)/2)+1
    for x in range(1,l):
        new_message.append(message[i:i+2])
        i=i+2   

    #getting the cipher text
    q=0
    cipher_matrix=[]
    #for each 2 characters
    for e in new_message:
        #get the row and column numbers of each character of the 2 characters
        r1,c1=find_position(keyword_matrix,e[0])
        r2,c2=find_position(keyword_matrix,e[1])
        #if the two characters are in the same row
        if r1==r2:
                if c1==4:
                        c1=-1
                if c2==4:
                        c2=-1
                cipher_matrix.append(keyword_matrix[r1][c1+1])
                cipher_matrix.append(keyword_matrix[r1][c2+1])
        #if the two characters are in the same column       
        elif c1==c2:
                if r1==4:
                        r1=-1
                if r2==4:
                        r2=-1
                cipher_matrix.append(keyword_matrix[r1+1][c1])
                cipher_matrix.append(keyword_matrix[r2+1][c2])
        #the general case
        else:
            cipher_matrix.append(keyword_matrix[r1][c2])
            cipher_matrix.append(keyword_matrix[r2][c1])

        cipher_text=''.join(cipher_matrix)

    return cipher_text

"""
    getKeyMatrix : 
	input : key as an array of integers
	output : returns the key in the matrix form
	explanation : helper function for the hill cipher algorithm, it does reshaping of the key depending on the length of the key
"""

def getKeyMatrix(key):
    #if the key is array of 4 integers it will be reshaped as a matrix of 2x2
    if(len(key)==4):
       key_Matrix = np.reshape(key,(2,2))
      
    #if the key is array of 9 integers it will be reshaped as a matrix of 3x3
    elif(len(key)==9):
       key_Matrix = np.reshape(key,(3,3))
       
    else:
        return("There is an Error in the key, it should be 4 or 9 integers ")
        
    return(np.matrix(key_Matrix))
"""
    Hill_Cipher : 
	input : message,K
	output : the ciphertext after applying the algorithm
	explanation : To encrypt a message, each block of n letters (considered as an n-component vector)
    is multiplied by an invertible n × n matrix, against modulus 26.
    The matrix used for encryption is the cipher key. 
"""
def Hill_Cipher(message, K):
    encrypted = ""
    message=message.replace(" ","")
    message = message.lower()
    message_in_numbers = []
    K = getKeyMatrix(K)
    #checking if the key is 2x2 and the message is not divisable by 2 (is odd) so we need to x in the end
    if(K.shape[0] == 2):
        if(len(message) %2 !=0):
            message = message + 'x'
    #checking if the key is 3x3 and the message is not divisable by 3
    elif(K.shape[0] == 3):
        if(len(message) %3 !=0):
            #the remainder is 1 so we need to x in the end
            if(len(message) % 3 ==1):
                message = message + 'xx'
            #the remainder is 2 so we need to x in the end
            else:
                message = message + 'x' 
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    #dict to get the order (index) of a character    
    letter_to_index = dict(zip(alphabet, range(len(alphabet))))
    #dict to get the character of an order (index) 
    index_to_letter = dict(zip(range(len(alphabet)), alphabet))
    #get the indecies of each character in the message and append it into the list
    for letter in message:
        message_in_numbers.append(letter_to_index[letter])
    #format the message into the desired shape so we can apply np.dot
    split_P = [
        message_in_numbers[i : i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]
        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0] #the encrypte indecies of characters 

        #getting the characters of those indecies
        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]
    encrypted=encrypted.upper()
    return encrypted

"""
    generateKey : 
	input : string,key,mode
	output : the correct key depending on the mode and the size of the message
	explanation : there is 2 modes in generating the key in vigenere cipher, if the key size equal to the 
    message size there is no need for this function, auto key mode repeates the key until its the same size of the message ,
    while repeating mode appends the message to the key until the key is the same size as the message
"""
def generateKey(string,key,mode):  
    key=key.upper()   
    string=string.upper()
    key = list(key) 
    #if the size of the key is the same as the message, the mode doesnot matter and the key will stay the same
    if len(string) == len(key): 
        return(key) 
    else: 
        #if the mode is false, so its repeating key mode
        if(mode==False) :
            #repeat the key until the sizes are equal            
            for i in range(len(string)-len(key)): 
                key.append(key[i % len(key)]) 
            return("" . join(key)) 
        #else the mode is true, so its auto key mode
        else: 
            #repeat the message until the sizes are equal 
            for i in range(len(string) -len(key)): 
                key.append(string[i % len(key)]) 
            return("" . join(key))
"""
    Vigenere_Cipher : 
	input : string,key,mode
	output : the ciphertext after applying the algorithm
	explanation : it is the same as the caesar Cipher but it uses different moves for each character depending
    on the character corresponding to it in the key
"""
def Vigenere_Cipher(string, key,mode): 
    #get the key depending on the chosen mode
    key = generateKey(string,key,mode)
    string=string.upper()   
    cipher_text = []   
    for i in range(len(string)): 
        if (string[i]== '\n'):
            continue           
        else:
            #same as ceasar but use the order of the correponding character of the key           
            x = ((ord(string[i])%65 + ord(key[i])%65)) %26
            x += ord('A') 
            cipher_text.append(chr(x)) 
    
    return("" . join(cipher_text))
"""
    Vernam_Cipher : 
    input : plaintext,key,key
    output : the ciphertext after applying the algorithm
    explanation : Assign a number to each character of the plain-text and the key according to alphabetical order. 
    Add both the number (Corresponding plain-text character number and Key character number). 
    Subtract the number from 26 if the added number is greater than 26, if it isn’t then leave it. 

"""
def Vernam_Cipher(plaintext, key):
      plaintext = plaintext.upper()
      key  = key.upper()
      ciphertext = ""
      ptr = 0
      for char in plaintext:
            ciphertext = ciphertext + chr((((ord(char)-65) ^ (ord(key[ptr])-65))%26)+65)
            ptr = ptr + 1
            if ptr == len(key):
                  ptr = 0
      return ciphertext

def main_files():
    print("DON'T FORGET TO WRITE YOUR PLAINTEXTS IN THE CORRECT FILE FOR EACH CIPHER")
    print("YOU WILL FIND THE OUTPUT IN THE FILES CORRESPONDING TO EACH CIPHER")

    #Caesar
    caesar_input =open('Caesar/caesar_plain.txt',"r")
    f1=caesar_input.read()
    plaintext_list = f1.splitlines()
    caesar_output=open('Caesar/caesar_cipher.txt',"w")
    key1=input("Enter your desired key for the CAESAR cipher: ")   
    for x in plaintext_list: 
        #handling empty line error
        if len(x) == 0 :
            continue
        result=Caesar_Cipher(x,int(key1))
        caesar_output.write(result)
        caesar_output.write("\n")   
    caesar_output.close()

    #Playfair
    playfair_input=open('PlayFair/playfair_plain.txt',"r")
    f2=playfair_input.read()
    plaintext_list = f2.splitlines()
    playfair_output=open('PlayFair/playfair_cipher.txt',"w")
    key2=input("Enter your desired key for the PLAYFAIR cipher: ")
    for x in plaintext_list:
        #handling empty line error
        if len(x) == 0 :
            continue
        result=Play_Fair_Cipher(x,key2)
        playfair_output.write(result)
        playfair_output.write("\n")
    playfair_output.close()

    #Hill_Cipher
    mode=input("Enter 2 if you will use 2*2 key matrix, 3 if you will use 3*3 key matrix for the HILL chipher: ")
    key3=[]
    if(int(mode)==2):
        hill_input=open('Hill/hill_plain_2x2.txt',"r")
        f3=hill_input.read() 
        plaintext_list = f3.splitlines()
        print("Enter your 2x2 key matrix in the form of array of integers and seperate the integers with space ")
        key = input()
        key_list = key.split()
        map_object = map(int, key_list)
        key3 = list(map_object)
        hill_output=open('Hill/hill_cipher_2x2.txt',"w")
    else:
        hill_input=open('Hill/hill_plain_3x3.txt',"r")
        f3=hill_input.read()
        plaintext_list = f3.splitlines()
        print("Enter your 3x3 key matrix in the form of array of integers and seperate the integers with space ")
        print("Eaxmple: key 3x3 will be written row by row as --> 2 4 12 9 1 6 7 5 3")
        key = input()
        key_list = key.split()
        map_object = map(int, key_list)
        key3 = list(map_object)
        hill_output=open('Hill/hill_cipher_3x3.txt',"w")   
    for x in plaintext_list:
        #handling empty line error
        if len(x) == 0 :
            continue
        result=Hill_Cipher(x,key3)
        hill_output.write(result)
        hill_output.write("\n")   
    hill_output.close() 

    #Vigenere_Cipher
    vigenere_input = open('Vigenere/vigenere_plain.txt',"r")
    f4=vigenere_input.read()
    plaintext_list = f4.splitlines()
    key4=input("Enter your desired key for the VIGENERE cipher: ")
    vigenere_output=open('Vigenere/vigenere_cipher.txt',"w")
    mode=input("Choose your desired mode (write false or true) , true for auto and false for repeating: ")
    mode = mode.lower()
    if(mode == "false"):
        for x in plaintext_list: 
            #handling empty line error
            if len(x) == 0 :
                continue
            result=Vigenere_Cipher(x, key4 , False)
            vigenere_output.write(result)
            vigenere_output.write("\n")
    else:
        for x in plaintext_list: 
            #handling empty line error
            if len(x) == 0 :
                continue
            result=Vigenere_Cipher(x, key4 , True)
            vigenere_output.write(result)
            vigenere_output.write("\n")
    vigenere_output.close()

    #vernam
    vernam_input =open('Vernam/vernam_plain.txt',"r")
    f5=vernam_input.read()
    plaintext_list = f5.splitlines()
    vernam_output=open('Vernam/vernam_cipher.txt',"w")
    key5=input("Enter your desired key for the VERNAM cipher: ")
    for x in plaintext_list: 
        #handling empty line error
        if len(x) == 0 :
            continue
        result=Vernam_Cipher(x,key5)
        vernam_output.write(result)
        vernam_output.write("\n")  
    vernam_output.close()

def main_console_input():
    print("Enter the name of the cipher you want to use ")
    print("[caesar - hill - playfair - vernam - vigenere]")
    chosen_cipher = input()
    #incase the user entered capital letters
    chosen_cipher = chosen_cipher.lower()
    if chosen_cipher == "caesar":
        plaintext=input("Enter your plaintext for the CAESAR cipher: ")
        key=input("Enter your desired key for the CAESAR cipher: ")
        cipher_text = Caesar_Cipher(plaintext,int(key))
        print("your ciphertext is: ",cipher_text)
    elif chosen_cipher == "hill":
        plaintext=input("Enter your plaintext for the HILL cipher: ")
        mode=input("Enter 2 if you will use 2*2 key matrix, 3 if you will use 3*3 key matrix for the HILL chipher: ")
        if(int(mode)==2):
            print("Enter your 2x2 key matrix in the form of array of integers and seperate the integers with space ")
            print("Eaxmple: key 3x3 will be written row by row as --> 5 17 8 3")
            key = input()
            key_list = key.split()
            map_object = map(int, key_list)
            key3 = list(map_object)
        elif(int(mode)==3):
            print("Enter your 3x3 key matrix in the form of array of integers and seperate the integers with space ")
            print("Eaxmple: key 3x3 will be written row by row as --> 2 4 12 9 1 6 7 5 3")
            key = input()
            key_list = key.split()
            map_object = map(int, key_list)
            key3 = list(map_object)
        cipher_text=Hill_Cipher(plaintext,key3)
        print("your ciphertext is: ",cipher_text)
    
    elif chosen_cipher == "playfair":
        plaintext=input("Enter your plaintext for the PLAYFAIR cipher: ")
        key=input("Enter your desired key for the PLAYFAIR cipher: ")
        cipher_text=Play_Fair_Cipher(plaintext,key)
        print("your ciphertext is: ",cipher_text)

    elif chosen_cipher == "vernam":
        plaintext=input("Enter your plaintext for the VERNAM cipher: ")
        key=input("Enter your desired key for the VERNAM cipher: ")
        cipher_text=Vernam_Cipher(plaintext,key)
        print("your ciphertext is: ",cipher_text)

    elif chosen_cipher == "vigenere":
        plaintext=input("Enter your plaintext for the VIGENERE cipher: ")
        key=input("Enter your desired key for the VIGENERE cipher: ")
        mode=input("Choose your desired mode (write false or true) , true for auto and false for repeating: ")
        mode = mode.lower()
        if(mode == "false"):
            cipher_text=Vigenere_Cipher(plaintext, key, False)
            print("your ciphertext is: ",cipher_text)
        elif(mode == "true"):
            cipher_text=Vigenere_Cipher(plaintext, key , True)
            print("your ciphertext is: ",cipher_text)
        else:
            print("Error, See the screenshots for referencing ")

def main():
    print("Please Enter method for entering the input\n - F : for reading from files\n - C : for reading from console")
    method = input()
    if method == 'F':
         main_files()
    elif method == 'C':
        main_console_input()
    else:
        print("invalid method !!!")
        print("re-enter the required method ")
        main()


    print("Want another operation?, Type yes or no")
    result = input()
    result = result.lower()
    if result == "yes":
        main()
    elif result == "no":
        pass
    else:
        print("Error! see the screenshots for referencing, the answer is yes or no only")

main()