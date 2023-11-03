import tkinter as tk
from utils.model_driver import AppInterface


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("400x300") 
    
    app = AppInterface(root=root)

    root.mainloop()