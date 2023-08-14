# AIO-STEGANOGRAPHY

This project provides 4 types of Steganography { Image, Text, Audio, Video } that hides User's Text message in the desired cover file using the tool and can send it to the receiver who can extract the Hidden message using the same tool .

# Project Name : AIO-Steganography
# Made By - Vaisakh Sriram

* Steganography is the art of hiding the fact that communication is taking place, by hiding information in other information. 
* This project hides the message with in the image, text file, audio file and video file. In this project, the sender selects a cover file (image, text, audio or video) with secret text and hide it into the cover file by using different efficient algorithm and generate a stego file of same format as our cover file (image, text, audio or video). Then the stego file is sent to the destination with the help of private or public communication networks. On the other side i.e. receiver, the receiver downloads the stego file and by using the appropriate decoding algorithm retrieves the secret text that is hidden in the stego file.

![1](https://user-images.githubusercontent.com/77832407/152796278-a60d3042-a6cd-442d-96e0-7f5a8b11f3ed.jpg)

# Image Steganography ( Hiding TEXT in IMAGE ) :

* Using ***Least Significant Bit Insertion*** we overwrite the LSB bit of actual image with the bit of text message character. At the end of text message we push a delimiter to the message string as a checkpoint useful in decoding function. We encode data in order of Red, then Green and then Blue pixel for the entire message.

# Text Steganography ( Hiding TEXT in TEXT ) :

* In Unicode, there are specific zero-width characters (ZWC). We used four ZWCs for hiding the Secret Message through the Cover Text.

![image](https://user-images.githubusercontent.com/77832407/152797497-54ad8d79-9375-4c8a-9b7a-2b3586303d47.png)

* We get its ascii value and it is incremented or decremented based on if ascii value between 32 and 64 , it is incremented by 48(ascii value for 0) else it is decremented by 48
* Then xor the the obtained value with 170(binary equivalent-10101010) 
* Convert the obtained number from first two step to its binary equivalent then add "0011" if it earlier belonged to ascii value between 32 and 64 else add "0110" making it 12       bit for each character.
* With the final binary equivalent we also 111111111111 as delimiter to find the end of message 
* Now from 12 bit representing each character every 2 bit is replaced with equivalent ZWCs according to the table. Each character is hidden after a word in the cover text.
