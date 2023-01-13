from tkinter import Tk
import tkinter.messagebox as messagebox
from tkinter import simpledialog

def popup(head, prompt):
    """Prompts the user for input
    
    Parameters:
        head (string): Title of pop up window
        prompt (string): Text to display in window
    Returns:
        USER_INP (string): Users input
    """
    ROOT = Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title=head, prompt=prompt)
    return USER_INP

def passpopup(head, prompt):
    """Prompts the user for password input
    
    Parameters:
        head (string): Title of pop up window
        prompt (string): Text to display in window
    Returns:
        USER_INP (string): Users input
    """        
    ROOT = Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title=head, prompt=prompt, show='*')
    return USER_INP

def show_info(head, prompt):
    root = Tk()
    root.withdraw()
    messagebox.showinfo(head, prompt)

def show_error(head, prompt):
    root = Tk()
    root.withdraw()
    messagebox.showerror(head, prompt)

def show_warning(head, prompt):
    root = Tk()
    root.withdraw()
    messagebox.showwarning(head, prompt)