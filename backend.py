import time
import numpy as np
from math import sqrt
import random
from os import remove as remove_file
import os
def show_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function: {func.__name__}\nExecution time: {end_time - start_time}")
        return result
    return wrapper

def decrypt_text(plain_text, key, rotations=0):
    side_length = int(sqrt(len(plain_text)))
    matrix = np.array([list(plain_text[i:i+side_length]) for i in range(0, len(plain_text), side_length)])
    cypher_text = ""
    # print(matrix)
    
    for i in range(0,rotations):
        key = [(position[1], side_length - 1 - position[0]) for position in key]
    key = sorted(key)
    
    # print(key)
    for i in range(0,4):
        for position in key: #update the key
            cypher_text += matrix[position[0]][position[1]]
            # print(f"{i}) {cypher_text} and {key}")
            key[key.index(position)] = (position[1], side_length - 1 - position[0])#update the key
            key = sorted(key)
            
    return cypher_text


def encrypt_text(plain_text, key, rotations=0):
    side_length = int(sqrt(len(plain_text)))
    #create empty matrix
    matrix=np.empty((side_length,side_length), dtype=str)
    # print(f"Before rotation: {key}")
    for i in range(0,rotations):
        key = [(position[1], side_length - 1 - position[0]) for position in key]
        
    key = sorted(key)
    # print(f"After rotation: {key}")
    text_index=0
    for i in range(0,4):
        for position in key: #update the key
            matrix[position[0]][position[1]]=plain_text[text_index]
            # print(f"{i}) {cypher_text} and {key}")
            key[key.index(position)] = (position[1], side_length - 1 - position[0])#update the key
            key = sorted(key)
            text_index+=1
    # print(matrix)

    #matrix to string
    cypher_text=""
    for i in range(0,side_length):
        for j in range(0,side_length):
            cypher_text+=matrix[i][j]
    return cypher_text
    
@show_execution_time
def generate_key(side_length):
    #make a matrix full of zeros
    side_length=int(side_length)
    random.seed()
    matrix=np.zeros((side_length,side_length), dtype=int)
    key=[]
    current_row_index=int(side_length/2-1)
    while current_row_index>=0:
        # print(f"current_row_index={current_row_index}")
        accessable_in_row = [i for i in range(current_row_index,side_length-(current_row_index+1)) if matrix[current_row_index][i]==0]
        for j in range(current_row_index,side_length-(current_row_index+1)):
            # print(f"accessable_in_row={accessable_in_row}")
            side = random.randint(0,3) #0 - top, 1 - right, 2 - bottom, 3 - left (0 rotation, 1 rotation, 2 rotation, 3 rotation)
            index_from_accessable=random.choice(accessable_in_row)
            accessable_in_row.remove(index_from_accessable)
            if side==0:
                row_index=current_row_index
                column_index=index_from_accessable
            if side==1:
                row_index=index_from_accessable
                column_index=side_length-(current_row_index+1)
            if side==2:
                row_index=side_length-(current_row_index+1)
                column_index=side_length-(index_from_accessable+1)
            if side==3:
                row_index=side_length-(index_from_accessable+1)
                column_index=current_row_index
            # print(f"\tside={side}, row_index={row_index}, column_index={column_index}")
            key.append((row_index,column_index))
            for i in range(0,4):
                matrix[row_index][column_index]=1
                row_index,column_index=column_index,side_length-(row_index+1)
            
        current_row_index-=1
    
    key = sorted(key)
    return key

@show_execution_time
def encrypt_file(file_path, key, rotation,block_size): #block size - perfect square of an even number
    with open(file_path, "r") as f:
        plain_text = f.read()
    block_size = int(block_size)
    crypted_text = ""
    if len(plain_text)%block_size!=0:
        plain_text+=" "*(block_size-len(plain_text)%block_size)
    for i in range(0, len(plain_text), block_size):
        # print(f"i={i}")
        crypted_text+= encrypt_text(plain_text[i:i+block_size], key, rotation)
    with open(file_path.split(".")[0]+"_crypted.txt", "w") as f:
        f.write(crypted_text)

@show_execution_time
def decrypt_file(file_path, key, rotation,block_size): #block size - perfect square of an even number
    with open(file_path, "r") as f:
        cypher_text = f.read()
    plain_text = ""
    for i in range(0, len(cypher_text), block_size):
        plain_text+= decrypt_text(cypher_text[i:i+block_size], key, rotation)
    with open(file_path.split(".")[0]+"_decrypted.txt", "w") as f:
        f.write(cypher_text)

def input_text_correction(input_text):
    side_length=sqrt(len(input_text))
    if side_length%1!=0:
        input_text+=" "*((int(sqrt(len(input_text)))+1)**2-len(input_text))
    side_length=sqrt(len(input_text))
    if int(side_length)%2==1:
        side_length+=1
    return input_text+(" "*int(side_length**2-len(input_text)))

def rotate_key(key, rotations, side_length):
    for i in range(0,rotations):
        key = [(position[1], side_length - 1 - position[0]) for position in key]
    return key

def get_key_positions(key, side_length):
    key = sorted(key)
    key_positions = [key]
    # print(key)
    for i in range(0,4):
        for position in key: #update the key
            # print(f"{i}) {cypher_text} and {key}")
            key[key.index(position)] = (position[1], side_length - 1 - position[0])#update the key
        key_positions.append(sorted(key))

    # key_postions = [key] #added the first position
    # for i in range(0,4):
    #     key_postions.append(sorted([(position[1], side_length - 1 - position[0]) for position in key_postions[i]]))
    return key_positions[:-1]


def clear_a_file(file_path):
    
    if os.path.exists(file_path):
        os.remove(file_path)
    open(file_path, 'w').close()
    
@show_execution_time
def encrypt_file_optimazed(file_path, key, rotation,block_size):
    crypted_file_path = file_path.split(".")[0]+"_crypted.txt"
    clear_a_file(crypted_file_path)
    side_length = int(sqrt(block_size))
    # crypted_text_array = np.full((side_length,side_length), dtype=str)
    plain_text_array = np.empty((side_length, side_length), dtype='|S1')
    # print("Key: ", key)
    key = rotate_key(key, rotation, side_length)
    # print("Key after rotation: ", key)
    keys = get_key_positions(key, side_length)
    
    chunk_of_plain_text =""
    plain_text_index=0
    with open(file_path, "r") as read_file, open(crypted_file_path, "a") as crypted_file:
        while True:
            chunk_of_plain_text = read_file.read(block_size)
            if not chunk_of_plain_text:
                break
            if len(chunk_of_plain_text)<block_size:
                chunk_of_plain_text += " "*(block_size-len(chunk_of_plain_text))
            plain_text_index=0
            
            plain_text_array = np.array(list(chunk_of_plain_text), dtype='|S1').reshape(side_length,side_length)
            
            crypted_text = ""
            #Fill the crypted matrix
            # for key in keys:
            #     for postion in key:
            #         crypted_file.write(plain_text_array[postion[0]][postion[1]].decode('utf-8'))
            for key in keys:
                # print(key)
                for postion in key:
                    crypted_text+=plain_text_array[postion[0]][postion[1]].decode('utf-8')
                    # crypted_text_array[postion[0]][postion[1]]=chunk_of_plain_text[plain_text_index]
                    # plain_text_index+=1
            # np.savetxt(crypted_file, crypted_text_array, fmt='%s') #save encrypted text to file
            # print(crypted_text)
            crypted_file.write(crypted_text) # convert array to string; append encrypted text to file
            
    return crypted_file_path

def get_keys_for_decryption(key, side_length):    
    # print(key)
    key 
    keys = [key]
    for i in range(1,4):
        for position in key: #update the key
            # print(f"{i}) {cypher_text} and {key}")
            key[key.index(position)] = (position[1], side_length - 1 - position[0])#update the key
        key = sorted(key)
        keys.append(key)

    return keys
@show_execution_time
def decrypt_file_optimazed(crypted_file_path, key, rotation,block_size):
    decrypted_file_path = crypted_file_path.split(".")[0]+"_decrypted.txt"
    clear_a_file(decrypted_file_path)
    side_length = int(sqrt(block_size))
    decrypted_text_array = np.empty((side_length, side_length), dtype='|S1')
    key = rotate_key(key, rotation, side_length)
    keys = get_keys_for_decryption(key, side_length)
    keys = get_key_positions(key, side_length)
    #put the last key in the first position
    keys.insert(0, keys.pop())
    # print(keys)
    chunk_of_crypted_text =""
    crypted_text_index=0
    debug_chunk = chunk_of_crypted_text
    decrypted_text = ""
    plain_text = ""
    with open(crypted_file_path, "r") as crypted_file, open(decrypted_file_path, "ab") as decrypted_file:
        while True:
            chunk_of_crypted_text = crypted_file.read(block_size)
            if not chunk_of_crypted_text:
                break
            crypted_text_index=0
            for key in keys:
                for position in key:
                    decrypted_text_array[position[0]][position[1]]=chunk_of_crypted_text[crypted_text_index]
                    crypted_text_index+=1
            #plain_text = decrypted_text_array.tostring().decode('utf-8').replace(" ", "")
            decrypted_file.write(decrypted_text_array.tobytes())
            
            
            
    # print("The chunk of decrypted text is:\n{}".format(debug_chunk))
    # print(decrypted_text_array)
    return decrypted_file_path

def is_two_files_identical(file_path1, file_path2):
    with open(file_path1, "r") as file1, open(file_path2, "r") as file2:
        file1_text = file1.read()
        file2_text = file2.read()
        if file1_text == file2_text:
            return True
        else:
            return False

@show_execution_time    
def encrypt_file_optimized_2(file_path, key, rotation, block_size):
    crypted_file_path = file_path.split(".")[0] + "_crypted.txt"
    clear_a_file(crypted_file_path)
    side_length = int(sqrt(block_size))
    keys = get_key_positions(rotate_key(key, rotation, side_length), side_length)
    # print(keys)
    with open(file_path, "rb") as read_file, open(crypted_file_path, "ab") as crypted_file:
        while True:
            chunk_of_plain_text = read_file.read(block_size)
            if not chunk_of_plain_text:
                break
            if len(chunk_of_plain_text) < block_size:
                chunk_of_plain_text += b" " * (block_size - len(chunk_of_plain_text))
            
            crypted_text = ""
            for key in keys:
                for position in key:
                    index = position[0] * side_length + position[1]
                    crypted_text += chunk_of_plain_text[index:index+1].decode('utf-8')
            crypted_file.write(crypted_text.encode('utf-8'))
    return crypted_file_path
if __name__ == "__main__":
    pass
    # # file_name = "big_text.txt"
    # file_name = "big_text.txt"
    # text_file_path = "D:\\Programing\\Python\\UdemyCiphers\\Cardano\\{}".format(file_name)
    # block_size = 4**2
    # key = [(0,0), (0,1), (0,2), (1,1)]
    # #key = [(0, 0), (0, 1), (0, 4), (0, 5), (1, 0), (2, 1), (2, 2), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3), (5, 0), (5, 1), (6, 1), (6, 3)]
    # #encrypt_file(text_file_path,key,0,block_size)
    
    # crypted_path = encrypt_file_optimized_2(text_file_path, key, 0, block_size)
    # decrypted_path = decrypt_file_optimazed(text_file_path.split(".")[0]+"_crypted.txt", key, 0, block_size)
    
    # # decrypt_file(file_path,key,0,block_size)
