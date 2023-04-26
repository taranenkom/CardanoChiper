#Grille cipher
from backend import *
from GUI import *
        
if __name__ == "__main__":

    file_name = "big_text.txt"
    text_file_path = "D:\\Programing\\Python\\UdemyCiphers\\Cardano\\{}".format(file_name)
    block_size = 4**2
    key = [(0,0), (0,1), (0,2), (1,1)]
    
    crypted_path = encrypt_file_optimized_2(text_file_path, key, 0, block_size) #best working version
    decrypted_path = decrypt_file_optimazed(text_file_path.split(".")[0]+"_crypted.txt", key, 0, block_size) #best working version
    
    run_GUI()