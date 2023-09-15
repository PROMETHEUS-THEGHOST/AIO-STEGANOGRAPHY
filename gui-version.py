import numpy as np
import pandas as pand
import os
import cv2
from matplotlib import pyplot as plt
import tkinter
import customtkinter

#System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("PROTON STEGANOGRAPHY")


#UI Elements
title_label = customtkinter.CTkLabel(app, text="STEGANOGRAPHY")
title_label.pack(padx=10, pady=10)
heading_label = customtkinter.CTkLabel(app, text="MAIN MENU")
heading_label.pack(padx=10, pady=10)

img_steg_button = customtkinter.CTkButton(app, text="IMAGE STEGANOGRAPHY", width=140)
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