#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import requests
import time
from requests.auth import HTTPBasicAuth
headers ={'Content-Type': 'application/xml', 'appKey' : '1ca74b6c-0501-4c78-af8c-593f44832f63'}
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    #print "Tap rfid tag or card"
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # If a card is found
    #if status == MIFAREReader.MI_OK:
        #print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+""+str(uid[1])+""+str(uid[2])+""+str(uid[3])
	cardUID = str(uid[0])+""+str(uid[1])+""+str(uid[2])+""+str(uid[3])
        #r = requests.put("http://10.196.70.125:8080/Thingworx/Things/RFID/Properties/tagId?method=put&value="+cardUID, auth=('Administrator', 'admin'),headers=headers)    
        r = requests.put("http://192.168.43.247:8080/Thingworx/Things/RFID/Properties/tagId?method=put&value="+cardUID, auth=('Administrator', 'admin'),headers=headers)    
	print "Response code {0} ".format(r.status_code) 
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

