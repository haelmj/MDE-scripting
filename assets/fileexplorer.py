from tkinter import Tk     
from tkinter.filedialog import askopenfilename


def fileExplorer():
    """Returns file path
    
    Prompts use to select a file from an Open dialog box
    """
    # disable full GUI, prevent root window from appearing
    Tk().withdraw() 
    file_path= askopenfilename()
    return file_path