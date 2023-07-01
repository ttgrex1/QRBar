import PySimpleGUI as sg
import qrcode
import shutil
import pickle
import os
import barcode
from barcode.writer import ImageWriter

# create the layout of the window
layout = [
    [sg.Menu([["File", ["Set Default Folder", "Open File"]]], key="-MENU-")],  # add an open file menu item
    [sg.Text("Enter the data for the QR code:")],
    [sg.Input(key="-DATA-")],
    [sg.Button("Generate QR Code"), sg.Button("Generate Barcode"), sg.Button("Save")],  # add a save button
    [sg.Image(key="-IMAGE-")]
]

# create the window
window = sg.Window("QR Code and Barcode Generator", layout)

# initialize some variables
default_folder = None  # default folder to save QR codes
settings_file = "settings.pkl"  # settings file name

# try to load the settings from the file
try:
    with open(settings_file, "rb") as f:  # open the file in binary mode
        default_folder = pickle.load(f)  # load the default folder from the file
except FileNotFoundError:  # if the file does not exist
    pass  # do nothing

# Barcode generation function
def generate_barcode(upc):
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(upc, writer=ImageWriter())
    filename = ean.save('barcode')
    return filename

# event loop
while True:
    event, values = window.read()  # read user input

    if event == sg.WIN_CLOSED:  # if user closes window
        break

    elif event == "Generate QR Code":  # if user clicks generate QR code button
        data = values["-DATA-"]  # get the data from the input box
        img = qrcode.make(data)  # create a QR code image
        filename = data + ".png"  # use the data as the file name with .png extension
        img.save(filename)  # save the image
        window["-IMAGE-"].update(filename=filename)  # update the image element with the QR code

    elif event == "Generate Barcode":  # if user clicks generate barcode button
        data = values["-DATA-"]  # get the data from the input box
        filename = generate_barcode(data)  # generate the barcode image and get the filename
        window["-IMAGE-"].update(filename=filename)  # update the image element with the barcode

    elif event == "Save":  # if user clicks save button
        if default_folder:  # if default folder is set
            shutil.copy(filename, default_folder)  # copy the image to the default folder
            sg.popup(f"QR code or Barcode saved to {default_folder}")  # show a popup message
        else:  # if default folder is not set
            sg.popup("Please set a default folder first")  # show a popup message

    elif event == "Set Default Folder":  # if user clicks set default folder menu item
        default_folder = sg.popup_get_folder("Select a folder to save QR codes")  # get a folder from user
        with open(settings_file, "wb") as f:  # open the file in binary mode
            pickle.dump(default_folder, f)  # save the default folder to the file

    elif event == "Open File":  # if user clicks open file menu item
        filename = sg.popup_get_file("Select a file to open")  # get a file name from user
        if filename:  # if a file is selected
            window["-IMAGE-"].update(filename=filename)  # update the image element with the selected file
            name = os.path.basename(filename)  # get the file name from the file path
            name = os.path.splitext(name)[0]  # remove the file extension from the file name
            window["-DATA-"].update(value=name)  # update the input box with the file name

# close the window
window.close()
