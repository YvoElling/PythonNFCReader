# Python NFC Reader
NFC Reader using ACS ACR122U smartcard reader for the Solar Team Eindhoven payment system. This application is
used as submodule of the overlying raspberry pi python-kivy user interface to identify yourself as a buyer of 
the one of the product in store. 

### 0. Requirements
Developed on Ubuntu 18.04 with Plasma KDE. Requires Python3.
Depdencies that are required:
 - libusb-dev (USB development)
 - pcscd (PC/SC daemon)
 - pcsc-tools (To run pcsc_scan)
 - libpcsclite1 (PC/SC lite library)
 - libpcsclite-dev (PC/SC lite development library)
 - pyscard (python module) download repository and setup.py)
 - swig (for building the wheel of pyscard)
 
 After connecting the ACS ACR122U, run: 
 > lsusb
 
 and
 > pcsc_scan 
 
 
 Validate whether the ACR appears in the output lists of either command. Note: It has to appear in both!
 If an error occurs, or the program keeps searching but does not find anything, do the following:
 > sudo nano /etc/modprobe.d/blacklist.conf
 
 Subsequently, add the following two lines to the bottom of the file
 > install nfc /bin/false<br>
 > install pn533 /bin/false
 
 You can save the file by pressing CTRL+X. You will probably have to restart your computer now.
 
### 1. Errorcodes
See table underneath<br>
Category = {Development, Debug, Runtime}

| Errorcode 	| Category   	| Meaning                                                                                                                                       	|
|-----------	|-------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|
| 1         	| Development 	| Program has reached timelimit while waiting for a card to be presented. This error should not happen and implies an incorrect implementation. 	|
|           	|             	|                                                                                                                                               	|                                                                                                                                                	|                                                                                                                                     	|
