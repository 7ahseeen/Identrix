# Identrix - developed by Girgiti github:7ahseeen

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

import os

basePath = os.path.abspath('.')

iconFolderPath = os.path.join(basePath, 'icons')

appIconPath = os.path.join(iconFolderPath, 'appIcon.png')
devIconPath = os.path.join(iconFolderPath, 'devIcon.png')

#   window for app info
def aboutApp(App):
    aboutAppWindow = tk.Toplevel(App)
    aboutAppWindow.resizable(False, False)

    AppIcon = Image.open(appIconPath)
    aboutAppWindow.wm_iconphoto(False, ImageTk.PhotoImage(AppIcon))
    aboutAppWindow.title("About this software")
    aboutAppWindow.geometry('500x330')
    aboutAppWindow.configure(bg="#d0aca1")

    #   heading
    #   appicon
    appIcon = Image.open(appIconPath)
    appIcon = appIcon.resize((100, 100))
    img = ImageTk.PhotoImage(appIcon)
    aboutAppWindow.img = img
    imgLabel = tk.Label(aboutAppWindow, image = img, bg = '#d0aca1')
    imgLabel.pack(side = "top", pady = 10, anchor = "center")

    #   appname, version, release date etc
    appNameText = tk.Label(aboutAppWindow, text = "Identrix", font = ("Courier", 20, "bold"), fg = "#5c352d", bg = "#d0aca1")
    appNameText.pack()

    appVerText = tk.Label(aboutAppWindow, text = "\n\nVersion 1.0 - Released 17 Jul, 2025\n", font = ("Courier", 10), fg = "#7f493f", bg = "#d0aca1")
    appVerText.pack()

    appInfoText = tk.Label(aboutAppWindow, text = "A tool for finding identity and similarities among\nsequences of DNA, RNA or Proteins\n", font = ("Courier", 10), fg = "#7f493f", bg = "#d0aca1") # Identrix - developed by Girgiti github:7ahseeen
    appInfoText.pack()

#   window for dev info
def aboutDev(App):
    aboutDevWindow = tk.Toplevel(App)
    aboutDevWindow.resizable(False, False)

    AppIcon = Image.open(appIconPath)
    aboutDevWindow.wm_iconphoto(False, ImageTk.PhotoImage(AppIcon))
    aboutDevWindow.title("About the Developer")
    aboutDevWindow.geometry('500x350')
    aboutDevWindow.configure(bg="#d0aca1")

    #   dev info
    devInfoFrame = tk.Frame(aboutDevWindow, bg="#d0aca1")
    devInfoFrame.pack(padx = 10, pady = 10)

    infoTxt = ("\nName\t:\tTahsin Ahmed\n"
               "Degree\t:\tBioinformatics Engineering\n"
               "Faculty\t:\tAgricultural Engineering and Technology\n\n"
               "\t\tBangladesh Agricultural University\n"
               )
    infoLabel = tk.Label(devInfoFrame, text = infoTxt, justify = "left", bg="#d0aca1", font = ("Courier", 10, "bold"))  # Identrix - developed by Girgiti github:7ahseeen
    infoLabel.grid(row = 2, column = 0)

    devIcon = Image.open(devIconPath)
    devIcon = devIcon.resize((100,100))
    devPic = ImageTk.PhotoImage(devIcon)

    iconLabel = tk.Label(devInfoFrame, image = devPic, bg="#d0aca1")
    iconLabel.image = devPic
    iconLabel.grid(row = 0, column = 0, pady = 20)



#   window on how to use the app
def appInstructions(App):
    instructionsWindow = tk.Toplevel(App)
    instructionsWindow.resizable(False, False)

    AppIcon = Image.open(appIconPath)
    instructionsWindow.wm_iconphoto(False, ImageTk.PhotoImage(AppIcon))
    instructionsWindow.title("How to use")
    instructionsWindow.geometry('500x300')
    instructionsWindow.configure(bg="#d0aca1")

    #   Actual Ins

    insTxt = ("■\tSelect what you are trying to \n\tanalyze - DNA, RNA or Protein.\n\n"
              "■\tCopy and Paste the sequence in FASTA format.\n\n"
              "■\tOr you may Upload a FASTA file \n\tfrom 'File > Upload' in the menu.\n\n"
              "■\tFor Proteins, add similar entities \n\tin the text area below sequence input.\n\n"
              "■\tYou may copy the output or save it \n\tfrom 'File > Save Output' in the menu.\n\n"
              "■\t'Clear All' button resets \n\tthe input and output areas."
               )
    infoLabel = tk.Label(instructionsWindow, text = insTxt, justify = "left", bg="#d0aca1", font = ("Courier", 10))                                     # Identrix - developed by Girgiti github:7ahseeen
    infoLabel.pack(side = "top", padx = 5, pady = 10)