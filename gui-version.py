import numpy as np
import cv2
import customtkinter
import threading
import wave

result_label = None

# Functions
def msgtobinary(msg):
    if type(msg) == str:
        result = ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result = [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        result = format(msg, "08b")
    else:
        result = ""
    return result

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

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel = img[i, j]
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
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel = img[i, j]
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
    
    total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
    decoded_data = ""
    
    for byte in total_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*^*^*":
            return decoded_data[:-5]
    return ""

def encode_image():
            image = cv2.imread("Sample_cover_files/cover_image.jpg")
            encode_img_data(image)

def decode_image():
    def perform_decode():
        image_name = image_entry.get()
        if not image_name:
            feedback_label.configure(text="Please enter the name of the image file.")
            return

        # Assuming the image is in the same directory as the program
        image_path = image_name
        image = cv2.imread(image_path)
        if image is None:
            feedback_label.configure(text=f"Invalid image file: {image_name}")
            return

        decoded_message = decode_img_data(image)
        feedback_label.configure(text="Decoded message:\n" + decoded_message)

    def decode_image_thread():
        decode_button.configure(state="disabled")
        decoded_message = perform_decode()
        feedback_label.configure(text="Decoded message:\n" + decoded_message)
        decode_button.configure(state="normal")

    decode_window = customtkinter.CTk()
    decode_window.geometry("400x200")
    decode_window.title("Decode Image")

    image_label = customtkinter.CTkLabel(decode_window, text="Enter the name of the image file:")
    image_label.pack(padx=20, pady=10)

    image_entry = customtkinter.CTkEntry(decode_window, width=250, height= 25)
    image_entry.pack(padx=20, pady=10)

    decode_button = customtkinter.CTkButton(decode_window, text="Decode Image", width=30, command=decode_image_thread)
    decode_button.pack(padx=20, pady=10)

    feedback_label = customtkinter.CTkLabel(decode_window, text="", width=250, height= 25)
    feedback_label.pack(padx=20, pady=10)

    decode_window.mainloop()



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

def txt_encode(text):
    def perform_encode():
        def calculate_length(text):
            l = len(text)
            i = 0
            add = ""
            while i < l:
                t = ord(text[i])
                if t >= 32 and t <= 64:
                    t1 = t + 48
                    t2 = t1 ^ 170  # 170: 10101010
                    res = bin(t2)[2:].zfill(8)
                    add += "0011" + res
                else:
                    t1 = t - 48
                    t2 = t1 ^ 170
                    res = bin(t2)[2:].zfill(8)
                    add += "0110" + res
                i += 1
            res1 = add + "111111111111"
            return res1

        def encode_data():
            text_to_encode = text_entry.get("1.0", "end-1c")
            if not text_to_encode:
                feedback_label.configure(text="Please enter data to be encoded.")
                return

            binary_text = calculate_length(text_to_encode)
            feedback_label.configure(text=f"The string after binary conversion applying all the transformations:\n{binary_text}")
            length = len(binary_text)
            feedback_label2.configure(text=f"Length of binary after conversion: {length}")

            ZWC = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
            file1 = open("Sample_cover_files/cover_text.txt", "r+")
            name_of_file = name_entry.get()
            if not name_of_file:
                feedback_label.configure(text="Please enter the name of the Stego file after Encoding (with extension).")
                return

            file3 = open(name_of_file, "w+", encoding="utf-8")
            word = []
            for line in file1:
                word += line.split()

            i = 0
            while i < len(binary_text):
                s = word[int(i / 12)]
                j = 0
                x = ""
                HM_SK = ""
                while j < 12:
                    x = binary_text[j + i] + binary_text[i + j + 1]
                    HM_SK += ZWC[x]
                    j += 2
                s1 = s + HM_SK
                file3.write(s1)
                file3.write(" ")
                i += 12

            t = int(len(binary_text) / 12)
            while t < len(word):
                file3.write(word[t])
                file3.write(" ")
                t += 1

            file3.close()
            file1.close()
            feedback_label.configure(text="Stego file has been successfully generated.")

        encode_window = customtkinter.CTk()
        encode_window.geometry("600x400")
        encode_window.title("Encode Text Data")

        text_label = customtkinter.CTkLabel(encode_window, text="Enter data to be encoded:")
        text_label.pack(padx=20, pady=10)

        text_entry = customtkinter.CTkText(encode_window, width=140, height=10)
        text_entry.pack(padx=20, pady=10)


        encode_button = customtkinter.CTkButton(encode_window, text="Encode Text Data", width=30, command=encode_data)
        encode_button.pack(padx=20, pady=10)

        feedback_label = customtkinter.CTkLabel(encode_window, text="", width=60, height=5)
        feedback_label.pack(padx=20, pady=10)

        feedback_label2 = customtkinter.CTkLabel(encode_window, text="", width=60)
        feedback_label2.pack(padx=20, pady=10)

        name_label = customtkinter.CTkLabel(encode_window, text="Enter the name of the Stego file (with extension):")
        name_label.pack(padx=20, pady=10)

        name_entry = customtkinter.CTkEntry(encode_window, width=250, height= 50)
        name_entry.pack(padx=20, pady=10)

        encode_window.mainloop()

def encode_txt_data():
    def perform_encode():
        try:
            with open("Sample_cover_files/cover_text.txt", "r") as file:
                count2 = sum(len(word) for line in file for word in line.split())
                max_words = int(count2 / 6)
                feedback_label.configure(text=f"Maximum number of words that can be inserted: {max_words}")
        except FileNotFoundError:
            feedback_label.configure(text="Cover file not found.")

        text_to_encode = text_entry.get("1.0", "end-1c")
        l = len(text_to_encode)

        if l <= max_words:
            feedback_label.configure(text="Input message can be hidden in the cover file.")
            txt_encode(text_to_encode)
        else:
            feedback_label.configure(text="String is too big, please reduce string size.")

    encode_window = customtkinter.CTk()
    encode_window.geometry("400x400")
    encode_window.title("Encode Text Data")

    text_label = customtkinter.CTkLabel(encode_window, text="Enter data to be encoded:")
    text_label.pack(padx=20, pady=10)

    text_entry = customtkinter.CTkEntry(encode_window, width=200, height=10)
    text_entry.pack(padx=20, pady=10)

    encode_button = customtkinter.CTkButton(encode_window, text="Encode Text Data", width=30, command=perform_encode)
    encode_button.pack(padx=20, pady=10)

    feedback_label = customtkinter.CTkLabel(encode_window, text="", width=40, height=5)
    feedback_label.pack(padx=20, pady=10)

    encode_window.mainloop()

def decode_txt_data():
    def perform_decode():
        def BinaryToDecimal(binary):
            decimal = int(binary, 2)
            return decimal

        def decode_data():
            stego_file_name = stego_entry.get()
            if not stego_file_name:
                feedback_label.configure(text="Please enter the stego file name (with extension) to decode the message.")
                return

            ZWC_reverse = {u'\u200C': "00", u'\u202C': "01", u'\u202D': "11", u'\u200E': "10"}
            temp = ''
            try:
                with open(stego_file_name, "r", encoding="utf-8") as file4:
                    for line in file4:
                        for words in line.split():
                            T1 = words
                            binary_extract = ""
                            for letter in T1:
                                if letter in ZWC_reverse:
                                    binary_extract += ZWC_reverse[letter]
                            if binary_extract == "111111111111":
                                break
                            else:
                                temp += binary_extract

                feedback_label.configure(text="Encrypted message presented in code bits:\n" + temp)
                lengthd = len(temp)
                feedback_label2.configure(text="Length of encoded bits: " + str(lengthd))

                i = 0
                a = 0
                b = 4
                c = 4
                d = 12
                final = ''
                while i < len(temp):
                    t3 = temp[a:b]
                    a += 12
                    b += 12
                    i += 12
                    t4 = temp[c:d]
                    c += 12
                    d += 12
                    if t3 == '0110':
                        decimal_data = BinaryToDecimal(t4)
                        final += chr((decimal_data ^ 170) + 48)
                    elif t3 == '0011':
                        decimal_data = BinaryToDecimal(t4)
                        final += chr((decimal_data ^ 170) - 48)

                feedback_label3.configure(text="Message after decoding from the stego file:\n" + final)

            except FileNotFoundError:
                feedback_label.configure(text=f"File not found: {stego_file_name}")

        # Create GUI components for decoding
        decode_window = customtkinter.CTk()
        decode_window.geometry("600x400")
        decode_window.title("Decode Text Data")

        stego_label = customtkinter.CTkLabel(decode_window, text="Enter the stego file name (with extension):")
        stego_label.pack(padx=20, pady=10)

        stego_entry = customtkinter.CTkEntry(decode_window, width=200)
        stego_entry.pack(padx=20, pady=10)

        decode_button = customtkinter.CTkButton(decode_window, text="Decode Text Data", width=30, command=decode_data)
        decode_button.pack(padx=20, pady=10)

        feedback_label = customtkinter.CTkLabel(decode_window, text="", width=60, height=5)
        feedback_label.pack(padx=20, pady=10)

        feedback_label2 = customtkinter.CTkLabel(decode_window, text="", width=60)
        feedback_label2.pack(padx=20, pady=10)

        feedback_label3 = customtkinter.CTkLabel(decode_window, text="", width=60, height=5)
        feedback_label3.pack(padx=20, pady=10)

        decode_window.mainloop()

    perform_decode()

def txt_steg():
    txt_steg_window = customtkinter.CTk()
    txt_steg_window.geometry("400x300")
    txt_steg_window.title("Text Steganography")

    encode_button = customtkinter.CTkButton(txt_steg_window, text="Encode the Text message", width=30, command=encode_txt_data)
    encode_button.pack(padx=30, pady=30)

    decode_button = customtkinter.CTkButton(txt_steg_window, text="Decode the Text message", width=30, command=decode_txt_data)
    decode_button.pack(padx=20, pady=10)

    exit_button = customtkinter.CTkButton(txt_steg_window, text="Exit", width=30, command=txt_steg_window.destroy)
    exit_button.pack(padx=20, pady=10)

    txt_steg_window.mainloop()

def encode_aud_data():
    def encode_audio_data():
        nameoffile = file_entry.get()
        stegofile = stego_entry.get()
        data = data_entry.get("1.0", "end-1c")

        if not nameoffile or not stegofile or not data:
            feedback_label.configure(text="Please fill in all the fields.")
            return

        try:
            song = wave.open(nameoffile, mode='rb')
            nframes = song.getnframes()
            frames = song.readframes(nframes)
            frame_list = list(frames)
            frame_bytes = bytearray(frame_list)

            res = ''.join(format(i, '08b') for i in bytearray(data, encoding='utf-8'))
            length = len(res)

            data = data + '*^*^*'

            result = []
            for c in data:
                bits = bin(ord(c))[2:].zfill(8)
                result.extend([int(b) for b in bits])

            j = 0
            for i in range(0, len(result), 1):
                res = bin(frame_bytes[j])[2:].zfill(8)
                if res[len(res) - 4] == str(result[i]):
                    frame_bytes[j] = (frame_bytes[j] & 253)  # 253: 11111101
                else:
                    frame_bytes[j] = (frame_bytes[j] & 253) | 2
                    frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
                j = j + 1

            frame_modified = bytes(frame_bytes)

            with wave.open(stegofile, 'wb') as fd:
                fd.setparams(song.getparams())
                fd.writeframes(frame_modified)

            feedback_label.configure(text="Encoded the data successfully in the audio file.")
            song.close()
        except Exception as e:
            feedback_label.configure(text=f"Error: {str(e)}")

    encode_aud_window = customtkinter.CTk()
    encode_aud_window.geometry("720x480")
    encode_aud_window.title("Encode Audio Data")

    h2_label = customtkinter.CTkLabel(encode_aud_window, text="AUDIO STEGANOGRAPHY - Encode Audio Data")
    h2_label.pack(padx=10, pady=10)

    file_label = customtkinter.CTkLabel(encode_aud_window, text="Enter the name of the audio file (with extension):")
    file_label.pack(padx=20, pady=10)

    file_entry = customtkinter.CTkEntry(encode_aud_window, width=200)
    file_entry.pack(padx=20, pady=10)

    stego_label = customtkinter.CTkLabel(encode_aud_window, text="Enter the name of the stego file (with extension):")
    stego_label.pack(padx=20, pady=10)

    stego_entry = customtkinter.CTkEntry(encode_aud_window, width=200)
    stego_entry.pack(padx=20, pady=10)

    data_label = customtkinter.CTkLabel(encode_aud_window, text="Enter the secret message:")
    data_label.pack(padx=20, pady=10)

    data_entry = customtkinter.CTkTextbox(encode_aud_window, width=200, height=10)
    data_entry.pack(padx=20, pady=10)

    encode_button = customtkinter.CTkButton(encode_aud_window, text="Encode Audio Data", width=30, command=encode_audio_data)
    encode_button.pack(padx=20, pady=10)

    feedback_label = customtkinter.CTkLabel(encode_aud_window, text="", width=60)
    feedback_label.pack(padx=20, pady=10)

    encode_aud_window.mainloop()

def decode_aud_data():
    def decode_audio_data():
        try:
            nameoffile = file_entry.get()
            song = wave.open(nameoffile, mode='rb')

            nframes = song.getnframes()
            frames = song.readframes(nframes)
            frame_list = list(frames)
            frame_bytes = bytearray(frame_list)

            extracted = ""
            p = 0
            for i in range(len(frame_bytes)):
                if p == 1:
                    break
                res = bin(frame_bytes[i])[2:].zfill(8)
                if res[len(res) - 2] == '0':
                    extracted += res[len(res) - 4]
                else:
                    extracted += res[len(res) - 1]

                all_bytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
                decoded_data = ""
                for byte in all_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*":
                        feedback_label.configure(text="The Encoded data was: " + decoded_data[:-5])
                        p = 1
                        break
        except Exception as e:
            feedback_label.configure(text="Error: " + str(e))

    decode_aud_window = customtkinter.CTk()
    decode_aud_window.geometry("720x480")
    decode_aud_window.title("Decode Audio Data")

    h2_label = customtkinter.CTkLabel(decode_aud_window, text="AUDIO STEGANOGRAPHY - Decode Audio Data")
    h2_label.pack(padx=10, pady=10)

    file_label = customtkinter.CTkLabel(decode_aud_window, text="Enter the name of the audio file to be decoded (with extension):")
    file_label.pack(padx=20, pady=10)

    file_entry = customtkinter.CTkEntry(decode_aud_window, width=200)
    file_entry.pack(padx=20, pady=10)

    decode_button = customtkinter.CTkButton(decode_aud_window, text="Decode Audio Data", width=30, command=decode_audio_data)
    decode_button.pack(padx=20, pady=10)

    feedback_label = customtkinter.CTkLabel(decode_aud_window, text="", width=200, height=10)
    feedback_label.pack(padx=20, pady=10)

    decode_aud_window.mainloop()


def aud_steg():
    aud_steg_window = customtkinter.CTk()
    aud_steg_window.geometry("720x480")
    aud_steg_window.title("Audio Steganography")

    h2_label = customtkinter.CTkLabel(aud_steg_window, text="AUDIO STEGANOGRAPHY OPERATIONS")
    h2_label.pack(padx=10, pady=10)

    encode_button = customtkinter.CTkButton(aud_steg_window, text="Encode the Text message", width=140, command=encode_aud_data)
    encode_button.pack(padx=20, pady=10)

    decode_button = customtkinter.CTkButton(aud_steg_window, text="Decode the Text message", width=140, command=decode_aud_data)
    decode_button.pack(padx=20, pady=10)

    exit_button = customtkinter.CTkButton(aud_steg_window, text="EXIT", width=140, command=aud_steg_window.destroy)
    exit_button.pack(padx=20, pady=10)

    aud_steg_window.mainloop()




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

txt_steg_button = customtkinter.CTkButton(app, text="TEXT STEGANOGRAPHY", width=140, command= txt_steg)
txt_steg_button.pack(padx=20, pady=10)

aud_steg_button = customtkinter.CTkButton(app, text="AUDIO STEGANOGRAPHY", width=140, command= aud_steg)
aud_steg_button.pack(padx=20, pady=10)

vid_steg_button = customtkinter.CTkButton(app, text="VIDEO STEGANOGRAPHY", width=140)
vid_steg_button.pack(padx=20, pady=10)

exit_button = customtkinter.CTkButton(app, text="EXIT", width=140, command=app.destroy)
exit_button.pack(padx=20, pady=10)

app.mainloop()
