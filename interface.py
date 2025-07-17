# Identrix - developed by Girgiti github:7ahseeen

import customtkinter as ctk
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

import button_func
import menuPage
import os

basePath = os.path.abspath('.')

iconFolderPath = os.path.join(basePath, 'icons')

appIconPath = os.path.join(iconFolderPath, 'appIcon.png')
devIconPath = os.path.join(iconFolderPath, 'devIcon.png')

def inpArea(App):
        #   ------      Inputs        ------

    #   query input field

    App.queTypeName = tk.Label(App, justify = "left", text = ("Enter the groups of similar amino acids separated by commas : "),    # Identrix - developed by Girgiti github:7ahseeen
                           fg = "#5c352d", bg = '#d0aca1', font = ("Courier", 10, "bold"))

    App.queInput = ctk.CTkTextbox(
        master = App,
        height = 100,
        width = 700,
        fg_color = "#fff",
        corner_radius = 10,
        font = ("Courier", 15),
        text_color="#000",
        border_color = "#5c352d",
        border_width = 1
    )

    #   Input type options
    inpTypeName = tk.Label(App, text = "Input Type : ", fg = "#5c352d", bg = '#d0aca1', font = ("Courier", 12, "bold"))                                                 # Identrix - developed by Girgiti github:7ahseeen
    inpTypeName.pack(anchor = "w", padx = 10, pady = (10, 0))

    inpType = tk.Frame(App, bg = '#d0aca1')
    inpType.pack(pady = 2, anchor='w', padx = 10)

    App.selectedInp = tk.StringVar(value = "DNA")
    inpTypeOpt = ['DNA', 'RNA', 'Proteins']

    for opt in inpTypeOpt:
        tk.Radiobutton(
            inpType, text = opt, variable = App.selectedInp, value = opt, 
            fg = "#5c352d", bg = '#d0aca1', highlightthickness = 0, font = ("Courier", 11), activebackground = '#d0aca1',                       # Identrix - developed by Girgiti github:7ahseeen
            command = lambda : button_func.addQuery(App, App.selectedInp, App.queTypeName, App.queInput, App.seqInput)
        ).pack(side = "left", padx = 10)

    #   Sequence input field

    App.seqInpLabel = tk.Label(App, text = "Input the sequences in FASTA format : ", 
                           fg = "#5c352d", bg = '#d0aca1', font = ("Courier", 12, "bold"))                                                  # Identrix - developed by Girgiti github:7ahseeen
    App.seqInpLabel.pack(anchor = "w", padx = 10, pady = (10, 0))

    App.seqInput = ctk.CTkTextbox(
        master = App,
        height = 120,
        width = 700,
        fg_color = "#fff",
        corner_radius = 10,
        font = ("Courier", 15),
        text_color="#000",
        border_color = "#5c352d",
        border_width = 1
    )
    App.seqInput.pack(padx = 10, pady = (4, 0), anchor = "center")

    #   buttons
    btnFrame = tk.Frame(App, bg='#d0aca1')  # use your app's background color
    btnFrame.pack(anchor="w", padx=12, pady=5)

    #   submit btn

    submitBtn = ctk.CTkButton(
        master=btnFrame,
        text="Analyze",
        font=("Courier", 17),
        fg_color = "#5c352d",
        hover_color = "#80471c",
        corner_radius = 10,
        command=lambda: button_func.analyzeBtn(App)
    )
    submitBtn.pack(side="left", pady=5, padx=(12, 12))
    #   clear btn

    clrBtn = ctk.CTkButton(
        master=btnFrame,
        text="Clear All",
        font=("Courier", 17),
        fg_color = "#5c352d",
        hover_color = "#80471c",
        corner_radius = 10,
        command=lambda: button_func.clearBtn(App)
    )
    clrBtn.pack(side="left", pady=5, padx=12)

    #   err field

    App.errLabel = tk.Label(App, text="Error :",
                                fg = "#5c352d", bg = '#d0aca1', font = ("Courier", 12, "bold"))
    App.errBox = tk.Label(App, text = "Please provide valid input!",
                                  fg = "#5c352d", bg = '#d0aca1', font = ("Courier", 12))



def main_window():

    App = tk.Tk()

    #   ------      Basic App info, ui/ux        ------
    App.title("Identrix")
    App.configure(bg = '#d0aca1')
    
    App.geometry('750x680')
    App.resizable(False, True)

    AppIcon = Image.open(appIconPath)
    App.wm_iconphoto(False, ImageTk.PhotoImage(AppIcon))

    #   appicon
    appIcon = Image.open(appIconPath)
    appIcon = appIcon.resize((50, 50))
    img = ImageTk.PhotoImage(appIcon)
    App.img = img
    imgLabel = tk.Label(App, image = img, bg = '#d0aca1')
    imgLabel.pack(pady = 10, padx = 5)

    #   appname, version, release date etc
    appNameText = tk.Label(App, text = "Identrix", 
                           font = ("Courier", 20, "bold"), fg = "#5c352d", bg = "#d0aca1")
    appNameText.pack()

    #   ------      THE MENU BAR        ------

    menu_Bar = tk.Menu(App, bg = '#EDEADE', 
                       font = ("Courier", 12, "bold"), fg = "#5c352d", activebackground = "#d0aca1")
    #   FIle and Exit
    file_menu = tk.Menu(menu_Bar, tearoff = 0,  bg = '#EDEADE', 
                        font = ("Courier", 10, "bold"), fg = "#5c352d", activebackground = "#d0aca1")
    file_menu.add_command(label = "Save Output", command = lambda : button_func.saveOut(App))
    file_menu.add_command(label = "Upload FASTA File", command = lambda : button_func.upFile(App))

    file_menu.add_command(label = "Exit", command = App.destroy)
    menu_Bar.add_cascade(label = "File", menu = file_menu)
    #   Help
    help_menu = tk.Menu(menu_Bar, tearoff = 0,  bg = '#EDEADE', 
                        font = ("Courier", 10, "bold"), fg = "#5c352d", activebackground = "#d0aca1")
    help_menu.add_command(label = "Instructions", command = lambda : menuPage.appInstructions(App))
    menu_Bar.add_cascade(label="Help", menu = help_menu)
    #   About
    about_menu = tk.Menu(menu_Bar, tearoff = 0,  bg = '#EDEADE', 
                         font = ("Courier", 10, "bold"), fg = "#5c352d", activebackground = "#d0aca1")
    about_menu.add_command(label = "App", command = lambda : menuPage.aboutApp(App))
    about_menu.add_command(label = "Developer", command = lambda : menuPage.aboutDev(App))
    menu_Bar.add_cascade(label= "About", menu = about_menu)

    App.config(menu = menu_Bar)

    App.after(100, inpArea(App))

    App.mainloop()