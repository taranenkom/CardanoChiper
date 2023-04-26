from tkinter import *
from tkinter import messagebox, filedialog
from backend import *

WIDTH = 400
HEIGHT = 300

def run_GUI():
    root = Tk()
    my_gui = GrilleCipherGUI(root)
    root.mainloop()

class FileManipulationWindow:
    def __init__(self, parent):
        self.parent = parent
        
        self.window = Toplevel(parent)
        self.window.title("File Manipulation")
        master = self.window
        
        self.file_path_label = Label(master, text="File Path")
        self.file_path_label.grid(row=0, column=0)
        self.file_path_entry = Entry(master, width=WIDTH)
        self.file_path_entry.grid(row=0, column=1)
        
        self.browse_button = Button(master,text="Browse", command=self.browse_for_file)
        self.browse_button.grid(row=1, column=0)
        
        self.block_size_label = Label(master, text="Block Size")
        self.block_size_label.grid(row=2, column=0)
        self.block_size_entry = Entry(master, width=WIDTH)
        self.block_size_entry.grid(row=2, column=1)
        
        self.key_label = Label(master, text="Key")
        self.key_label.grid(row=3, column=0)
        self.key_entry = Entry(master, width=WIDTH)
        self.key_entry.grid(row=3, column=1)
        
        self.rotation_label = Label(master, text="Rotation")
        self.rotation_label.grid(row=4, column=0)
        self.rotation_entry = Entry(master, width=WIDTH)
        self.rotation_entry.grid(row=4, column=1)
        
        self.key_generator_button = Button(master, text="Generate Key", command=self.generate_key)
        self.key_generator_button.grid(row=5, column=0)
        
        self.encrypt_file_button = Button(master, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_file_button.grid(row=6, column=0)
        
        self.decrypt_file_button = Button(master, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_file_button.grid(row=7, column=0)
        
        self.close_button = Button(master, text="Close", command=self.close)
        self.close_button.grid(row=8, column=0)
        
        self.create_key_button = Button(master, text="Create Key", command=self.create_key)
        self.create_key_button.grid(row=9, column=0)
    
    def create_key(self):
        # Create a new grid window
        block_size = int(self.block_size_entry.get())
        if block_size % 2 == 1:
            block_size += 1
        self.block_size_entry.delete(0, END)
        self.block_size_entry.insert(0, block_size)
        grid_window = KeyCreationWindow(self.window, block_size)
        
        # Wait for the grid window to be closed
        self.window.wait_window(grid_window.window)
        
        # Get the clicked tiles from the grid window
        clicked_tiles = grid_window.indexs_to_send
        clicked_tiles = sorted(clicked_tiles)
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, str(clicked_tiles))
    def generate_key(self):
        key = generate_key(int(self.block_size_entry.get()))
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, str(key))

    def browse_for_file(self):
        self.file_path_entry.delete(0, END)
        self.file_path_entry.insert(0, filedialog.askopenfilename())
        
    def encrypt_file(self):
        block_size = int(self.block_size_entry.get())
        if block_size%2==1:
            block_size+=1
        self.block_size_entry.delete(0, END)
        self.block_size_entry.insert(0, block_size)
        rotations = int(self.rotation_entry.get())
        key = eval(self.key_entry.get())
        encrypt_file_optimized_2(self.file_path_entry.get(),key, rotations, block_size**2)
        
    def decrypt_file(self):
        block_size = int(self.block_size_entry.get())
        self.block_size_entry.delete(0, END)
        self.block_size_entry.insert(0, block_size)
        rotations = int(self.rotation_entry.get())
        key = eval(self.key_entry.get())
        decrypt_file_optimazed(self.file_path_entry.get(),key, rotations, block_size**2)
    
    def close(self):
        self.window.destroy()
        
class KeyCreationWindow:
    def __init__(self, parent, size):
        self.parent = parent
        self.size = size
        self.clicked_tiles = []
        
        # Create a new window
        self.window = Toplevel(parent)
        self.window.title("Interactive Grid")
        
        self.indexs_to_send = []
        # Create the grid of buttons
        self.buttons = []
        for row in range(size):
            button_row = []
            for col in range(size):
                button = Button(self.window, width=2, height=1, bg="white")
                button.config(command=lambda r=row, c=col: self.click_tile(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)
            
        # Create the close button
        close_button = Button(self.window, text="Done", command=self.close)
        close_button.grid(row=size, column=0, columnspan=size, pady=10)
        
    def click_tile(self, row, col):
        if (row, col) not in self.clicked_tiles:
            self.indexs_to_send.append((row, col))
            self.buttons[row][col]["bg"] = "red"
            self.clicked_tiles.append((row, col))
            row,col=col,self.size-(row+1)
            for i in range(1,4):
                button = self.buttons[row][col]
                button["bg"] = "black"
                self.clicked_tiles.append((row, col))
                row,col=col,self.size-(row+1)
    
    def should_be_coloured(self):
        should_be_coloured = 0
        minus_the_coloured_in_the_row = 1
        while minus_the_coloured_in_the_row < self.size:
            should_be_coloured += self.size - minus_the_coloured_in_the_row
            minus_the_coloured_in_the_row+=2
        print(should_be_coloured)
        return should_be_coloured

    def close(self):
        # self.parent.focus_set()
            # print(should_be_coloured)
        if len(self.indexs_to_send) != self.should_be_coloured():
            messagebox.showerror("Error", "You must colour every tile!")
        else:
            self.window.destroy()

class GrilleCipherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Grille Cipher")

        text_block_width=WIDTH -50
        self.plain_text_label = Label(master, text="Plain Text")
        self.plain_text_label.grid(row=0, column=0)

        self.key_label = Label(master, text="Key")
        self.key_label.grid(row=1, column=0)
        self.rotations_label = Label(master, text="Rotations")
        self.rotations_label.grid(row=2, column=0)

        self.cypher_text_label = Label(master, text="Cypher Text")
        self.cypher_text_label.grid(row=3, column=0)

        self.plain_text_entry = Entry(master, width=WIDTH)
        self.plain_text_entry.grid(row=0, column=1)

        self.key_entry = Entry(master, width=WIDTH)
        self.key_entry.grid(row=1, column=1)

        self.rotations_entry = Entry(master, width=WIDTH)
        self.rotations_entry.grid(row=2, column=1)

        self.cypher_text_entry = Entry(master, width=WIDTH)
        self.cypher_text_entry.grid(row=3, column=1)

        self.encrypt_button = Button(master, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(row=4, column=0)

        self.decrypt_button = Button(master, text="Decrypt", command=self.decrypt)
        self.decrypt_button.grid(row=5, column=0)
        
        self.generate_key_button = Button(master, text="Generate Key", command=self.generate_key)
        self.generate_key_button.grid(row=7, column=0)
        
        self.open_button = Button(master,text="Open Key Creator Window", command=self.open_key_creation_window)
        self.open_button.grid(row=9, column=0)
        
        self.file_manipulation_button = Button(master, text="File Manipulation", command=self.open_file_manipulation_window)
        self.file_manipulation_button.grid(row=10, column=0)
    
    def open_file_manipulation_window(self):
        FileManipulationWindow(self.master)
        
    
    def browse_for_file(self):
        file_path = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
        self.file_path_entry.delete(0, END)
        self.file_path_entry.insert(0, file_path)  
    def open_key_creation_window(self):
        
        plain_text = self.plain_text_entry.get()
        plain_text = input_text_correction(plain_text)
        self.plain_text_entry.delete(0, END)
        self.plain_text_entry.insert(0, plain_text)
        # Create a new grid window
        grid_window = KeyCreationWindow(self.master, size=int(sqrt(len(plain_text))))
        
        # Wait for the grid window to be closed
        self.master.wait_window(grid_window.window)
        
        # Get the clicked tiles from the grid window
        clicked_tiles = grid_window.indexs_to_send
        clicked_tiles = sorted(clicked_tiles)
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, str(clicked_tiles))
            
    def generate_key(self):
        plain_text = self.plain_text_entry.get()
        plain_text = input_text_correction(plain_text)
        self.plain_text_entry.delete(0, END)
        self.plain_text_entry.insert(0, plain_text)
        self.generated_key = generate_key(sqrt(len(plain_text)))
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, str(self.generated_key))
    
    def encrypt(self):
        plain_text = self.plain_text_entry.get()
        key = self.key_entry.get()
        rotations = self.rotations_entry.get()
        plain_text = input_text_correction(plain_text)
        if not rotations:
            rotations = 0
        
        try: 
            key = eval(key)#convert string representation of list to actual list
            cypher_text = encrypt_text(plain_text, key, int(rotations))
            print(cypher_text)
            self.cypher_text_entry.delete(0, END)
            self.cypher_text_entry.insert(0, cypher_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        cypher_text = self.cypher_text_entry.get()
        key = self.key_entry.get()
        rotations = self.rotations_entry.get()
        try:
            rotations = int(rotations)
        except:
            rotations = 0
        if not rotations:
            rotations = 0
        try:
            key = eval(key) #convert string representation of list to actual list
            plain_text = decrypt_text(cypher_text, key, int(rotations))
            print(plain_text)
            self.plain_text_entry.delete(0, END)
            self.plain_text_entry.insert(0, plain_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
            
