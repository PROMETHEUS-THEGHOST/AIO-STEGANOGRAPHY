import numpy as np
import pandas as pd  # Fixed typo in module name
import os
import cv2
from matplotlib import pyplot as plt
import tkinter as tk  # Changed tkinter import
import customtkinter

result_label = None

# Functions
def msgtobinary(data):
    # Create GUI components for input and binary result
    msg_entry = customtkinter.CTkEntry(app, width=40)
    msg_entry.pack(padx=20, pady=10)

    binary_result_label = customtkinter.CTkLabel(app, text="", width=50)
    binary_result_label.pack(padx=20, pady=10)

    def convert_to_binary():
        msg = msg_entry.get()

        if type(msg) == str:
            result = ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            result = [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            result = format(msg, "08b")
        else:
            binary_result_label.configure(text="Input type is not supported in this function")
            return

        binary_result_label.configure(text="Binary result:\n" + result)
        return result
    
    # Call the convert_to_binary function immediately and return its result
    return convert_to_binary()


# Create the main app
app = customtkinter.CTk()
app.geometry("720x480")
app.title("PROTON STEGANOGRAPHY")

# Call msgtobinary function with the app as an argument
msgtobinary(app)

# Start the main loop
app.mainloop()



def encode_img_data(img):
    # Create GUI components for input and feedback
    encode_img_data_window = customtkinter.CTk()
    encode_img_data_window.geometry("720x480")
    encode_img_data_window.title("Image Steganography")
    data_entry = customtkinter.CTkEntry(encode_img_data_window, width=500, height=10, placeholder_text="Enter the data to be Encoded in Image")
    data_entry.pack(padx=30, pady=10)

    name_entry = customtkinter.CTkEntry(encode_img_data_window, width=500, height=10, placeholder_text="Enter the name of the New Image (Stego Image) after Encoding(with extension)")
    name_entry.pack(padx=30, pady=10)


    feedback_label = customtkinter.CTkLabel(encode_img_data_window, text="", width=50)
    feedback_label.pack(padx=20, pady=10)

    def encode_data():
        data = data_entry.get()
        nameoffile = name_entry.get()

        if len(data) == 0:
            feedback_label.configure(text="Data entered to be encoded is empty")
            return

        no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8

        feedback_label.configure(text=f"Maximum bytes to encode in Image: {no_of_bytes}")

        if len(data) > no_of_bytes:
            feedback_label.configure(text="Insufficient bytes Error, Need Bigger Image or give Less Data !!")
            return

        data += '*^*^*'

        binary_data = msgtobinary(data)
        length_data = len(binary_data)

        feedback_label.configure(text=f"The Length of Binary data: {length_data}")

        index_data = 0

        for i in img:
            for pixel in i:
                r, g, b = msgtobinary(pixel)
                if index_data < length_data:
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data < length_data:
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data < length_data:
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                    index_data += 1
                if index_data >= length_data:
                    break
        
        cv2.imwrite(nameoffile, img)
        feedback_label.configure(text=f"Encoded the data successfully in the Image, and the image is successfully saved with the name {nameoffile}")
    
    # Create a button to trigger encoding
    encode_button = customtkinter.CTkButton(encode_img_data_window, text="Encode Image", width=140, command=encode_data)
    encode_button.pack(padx=20, pady=10)
    
    encode_img_data_window.mainloop()

def decode_img_data(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
    
    total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
    decoded_data = ""
    
    for byte in total_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*^*^*":
            result_label.configure(text=f"The Encoded data that was hidden in the Image was :--  {decoded_data[:-5]}")
            return


def encode_image():
            image = cv2.imread("Sample_cover_files/cover_image.jpg")
            encode_img_data(image)

def decode_image():
            image1 = cv2.imread(input("Enter the Image you need to Decode to get the Secret message :  "))
            decode_img_data(image1)

def img_steg():
    img_steg_window = customtkinter.CTk()
    img_steg_window.geometry("720x480")
    img_steg_window.title("Image Steganography")

    h2_label = customtkinter.CTkLabel(img_steg_window, text="IMAGE STEGANOGRAPHY OPERATIONS")
    h2_label.pack(padx=10, pady=10)

    enc_text_msg_button = customtkinter.CTkButton(img_steg_window, text="Encode the Text message", width=140, command=encode_image)
    enc_text_msg_button.pack(padx=20, pady=10)

    dec_text_msg_button = customtkinter.CTkButton(img_steg_window, text="Decode the Text message", width=140, command=decode_image)
    dec_text_msg_button.pack(padx=20, pady=10)

    exit_button = customtkinter.CTkButton(img_steg_window, text="EXIT", width=140, command=img_steg_window.destroy)
    exit_button.pack(padx=20, pady=10)

    img_steg_window.mainloop()



# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("PROTON STEGANOGRAPHY")

# UI Elements
title_label = customtkinter.CTkLabel(app, text="STEGANOGRAPHY")
title_label.pack(padx=10, pady=10)
heading_label = customtkinter.CTkLabel(app, text="MAIN MENU")
heading_label.pack(padx=10, pady=10)

img_steg_button = customtkinter.CTkButton(app, text="IMAGE STEGANOGRAPHY", width=140, command=img_steg)
img_steg_button.pack(padx=20, pady=10)

txt_steg_button = customtkinter.CTkButton(app, text="TEXT STEGANOGRAPHY", width=140)
txt_steg_button.pack(padx=20, pady=10)

aud_steg_button = customtkinter.CTkButton(app, text="AUDIO STEGANOGRAPHY", width=140)
aud_steg_button.pack(padx=20, pady=10)

vid_steg_button = customtkinter.CTkButton(app, text="VIDEO STEGANOGRAPHY", width=140)
vid_steg_button.pack(padx=20, pady=10)

exit_button = customtkinter.CTkButton(app, text="EXIT", width=140)
exit_button.pack(padx=20, pady=10)

app.mainloop()
