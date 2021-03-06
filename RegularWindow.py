from tkinter import *
import tkinter as Tk
#from tkinter import StringVar
from PIL import Image, ImageTk
from threading import Thread
#------------------------------------------
#Library for weight Sensor
import time
import sys
from hx711 import HX711
import RPi.GPIO as GPIO

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
#-----------------------------------
#Library for Temperature Sensor
from mlx90614 import MLX90614
#-----------------------------
#Library for Vibration Sensor
from Vibration_Sensor_Code1 import *

#########################################################################################
#the dictionary
f = open("Data_No_Water.txt", "r")
NWWeight = f.read()
f.close()

f = open("Data_With_Water.txt", "r")
WWeight = f.read()
f.close()

f = open("Data_Sensor_Weight.txt", "r")
SWeight = f.read()
f.close()

f = open("Data_Temperature.txt", "r")
Temperature = f.read()
f.close()

f = open("Data_Vibration_Sensor.txt", "r")
Vibr = f.read()
f.close()

f = open("Data_EndB_Stat.txt", "r")
EndBStat = f.read()
f.close()

MyDictionary = {
    "NWweight": float(NWWeight),
    "Wweight": float(WWeight),
    "SenseWeight": float(SWeight),
    "Temperature": float(Temperature),
    "Vibration": int(Vibr),
    "EndBStat": EndBStat
    }

######################################################################################################
#Functions
def cleanAndExit():#Function for cleaning up GPIO pins for sensor
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

#------------------------------------------------------------------------------------------------
def updatedict():#updates the dictionary and variables that are used for program management
    global MyDictionary                 #makes the dictionary able to be modified by this function
    f = open("Data_No_Water.txt", "r")  #opens file to read
    NWWeight = f.read()                 #assigns contents of this file to NWWeight
    f.close()                           #closes the file so that the program is able to continue

    f = open("Data_With_Water.txt", "r")
    WWeight = f.read()
    f.close()

    f = open("Data_Sensor_Weight.txt", "r")
    SWeight = f.read()
    f.close()

    f = open("Data_Temperature.txt", "r")
    Temperature = f.read()
    f.close()

    f = open("Data_Vibration_Sensor.txt", "r")
    Vibr = f.read()
    f.close()

    f = open("Data_EndB_Stat.txt", "r")
    EndBStat = f.read()
    f.close()

    MyDictionary = {                    #Assigns variables from the text files to the dictionary updating it
        "NWweight": float(NWWeight),
        "Wweight": float(WWeight),
        "SenseWeight": float(SWeight),
        "Temperature": float(Temperature),
        "Vibration": float(Vibr),
        "EndBStat": EndBStat
    }

    global NWDispV                      #Makes the StringVar values able to be manipulated
    global WDispV
    global SeWeDispV
    global TempDispV
    global VibDispV
    global EBSDispV

    NWDispV.set(NWWeight)               #updates the String Var values similar to the dictionary above
    WDispV.set(WWeight)
    SeWeDispV.set(SWeight)
    TempDispV.set(Temperature)
    VibDispV.set(Vibr)
    EBSDispV.set(EndBStat)

    print(MyDictionary)                 #Is troubleshooting code that prints the dictionary contents in terminal

#--------------------------------------------------------------------------------
def raise_frame(frame):#is used to toggle between frames
    frame.tkraise()

#-------------------------------------------------------------------------------
def recordclickNW():  # the record button for No Water Data
    sweight = MyDictionary["SenseWeight"]
    if sweight < 20:
        ErrorTxt2.config(text="No Jazzve Detected")     #is safety check ensuring that the weight sensor is not empty
    else:
        sweight = str(sweight)                          #setting the dictionary value to a string so that the data can be put into a text file

        f = open("Data_No_Water.txt", "w")              #is writing data from sensor weight to No Water file
        f.write(sweight)
        f.close()
        ErrorTxt2.config(text="No Water Weight Recorded")

        updatedict()                                    #is used to update the contents of the dictionary

#----------------------------------------------------------------------------------
def recordclickW():#the record button for with water file
    sweight = MyDictionary["SenseWeight"]       #same as recordclickNW function
    if sweight < 20:
        ErrorTxt2.config(text = "No Jazzve Detected")
    else:
        sweight = str(sweight)

        f = open("Data_With_Water.txt", "w")
        f.write(sweight)
        f.close()
        ErrorTxt2.config(text="With Water Weight Recorded")
        updatedict()

#---------------------------------------------------------------------------------
def EndBtoggle():#turns EndBStat to true which is ment to end the induction controll loop
    f = open("Data_EndB_Stat.txt", "w")  #writes true to the text file and updates f1 labels
    f.write("True")
    f.close()
    ErrorTxt1.config(text="End Pressed")
    StateTxt.config(text = "idle", bg = "yellow")
    GPIO.output(12, GPIO.LOW)

    updatedict()

#---------------------------------------------------------------------------------
def StartBtoggle():#turns EndBStat to false which should start the induction loop
    f = open("Data_EndB_Stat.txt", "w")
    f.write("False")
    f.close()
    ErrorTxt1.config(text = "Start Pressed")

    updatedict()

###############################################################################################################
#starting the tkinter module
Window = Tk.Tk()
Window.geometry("480x320")

#all of the StringVar for updating lables in real time
NWDispV = StringVar()
NWDispV.set(NWWeight)
WDispV = StringVar()
WDispV.set(WWeight)
SeWeDispV = StringVar()
SeWeDispV.set(SWeight)
TempDispV = StringVar()
TempDispV.set(Temperature)
VibDispV = StringVar()
VibDispV.set(Vibr)
EBSDispV = StringVar()
EBSDispV.set(EndBStat)
#------------------------------------------------------------------------------------
f1 = Frame(Window)  # putting frame in the main window module
f2 = Frame(Window)

for frame in (f1, f2):  # assigning dimensions of frame and making it the size of the window
    frame.place(x=0, y=0, relheight=1, relwidth=1)  # (x,y) topL corner position, (relh,w) seting proportion relative to parent object
    frame.configure(bg="black")
#------------------------------------------------------------------------------------
# f1 widgets
TopTxt = Label(f1, text="The Perfect Brew", relief=RIDGE, bg="cyan", font=20, width=16)
TopTxt.pack(side=TOP)

StartB = Button(f1, text="Start", width=8, font=40, bg="cyan", command= lambda: StartBtoggle())   #lambda is to ensure that this command only runs once and only when clicked
StartB.place(x=190, y=70)

EndB = Button(f1, text="End", width=8, font=40, bg="cyan", command=lambda: EndBtoggle())
EndB.place(x = 360, y = 70)

ConfigB = Button(f1, text="Configure", width=8, font=40, bg="cyan", command=lambda: raise_frame(f2))
ConfigB.place(x = 20, y = 70)

StateLabel = Label(f1,text = "State:", fg = "white", bg = "black", width = 8, font = 40)
StateLabel.place(x = 10, y = 240)
StateTxt = Label(f1, relief=RIDGE, bg="green", text="Waiting", font=20, width=8)
StateTxt.place(x = 90, y = 240)

ErrorLabel = Label(f1, text = "Error:", fg = "white", bg = "black", width = 8, font = 40)
ErrorLabel.place(x = 10, y = 280)
ErrorTxt1 = Label(f1, relief=RIDGE, bg="green", text=" ", font=20, width=12)
ErrorTxt1.place(x = 90, y = 280)

TempLabel = Label(f1, text = "Temperature:", fg = "white", bg = "black", width = 11, font = 40)
TempLabel.place(x = 20, y = 130)
TempDisp = Label(f1, textvariable = TempDispV, fg = "white", bg = "black", width = 4, font = 40)    #this uses textvariable and StringVar to keep labels up to date in real time
TempDisp.place(x = 155, y = 130)

WeightLabel = Label(f1, text = "Sensor Weight:", fg = "white", bg = "black", width = 12, font = 40 )
WeightLabel.place(x = 20, y = 170)
WeightDisp = Label(f1, textvariable = SeWeDispV, fg = "white", bg = "black", width = 4, font = 40)
WeightDisp.place(x = 155, y = 170)

#Picture
im = Image.open("TurkishCoffeMakerImage.png")   #opens the image
photo = ImageTk.PhotoImage(im)                  #sets the image to a tkinter photoimage object
Pic = Label(f1, image=photo)                    #creates a label holding the picture
Pic.image = photo                               #may not be needed
Pic.place(x=280, y=120)                         #places the image in the f1 frame

# ----------------------------------------------------------------------------------------------------------------
# f2 widgets
ConfigBack = Button(f2, text="Go Back", width=8, font=40, bg="cyan", command=lambda: raise_frame(f1))
ConfigBack.place(x = 40, y = 40)

RecordBNW = Button(f2, text="Empty Jazzve", width=14, font=40, bg="cyan", command=lambda: recordclickNW())
RecordBNW.place(x = 220, y = 20)

RecordBW = Button(f2, text = "Full Jazzve", width=14, font=40, bg="cyan", command = lambda: recordclickW())
RecordBW.place(x = 220, y = 70)

WLabel = Label(f2, text = "Full Jazzve Data:", width=14, font=30, bg="black", fg = "white")
WLabel.place(x = 15, y = 120)
WDisp = Label(f2, textvariable = WDispV, width = 6, font = 40, bg = "black", fg = "white")
WDisp.place(x = 55, y = 150)

NWLabel = Label(f2, text = "Empty Jazzve Data:", width=16, font=20, bg="black", fg = "white")
NWLabel.place(x = 5, y = 190)
NWDisp = Label(f2, textvariable = NWDispV, width = 6, font = 40, bg = "black", fg = "white")
NWDisp.place(x = 55, y = 220)

ErrorTxt2 = Label(f2, relief=RIDGE, bg="yellow", text=" ", font=20, width=25)
ErrorTxt2.place(x = 190, y = 280)

InstrTxt = Label(f2, relief=RIDGE,fg = "white", bg="black",wraplength = 260, text="This Window is used to Configure your coffee maker. Once you have the Jazzve prepared, put it in the coffee maker and press the relavent button.", font=15, width=25)
InstrTxt.place(x = 190, y = 120)

#---------------------------------------------------------------------------------------------
#Default Setup
raise_frame(f1) #ensures that the f1 frame is on top once the program boots up

f = open("Data_EndB_Stat.txt", "w")  #Defaults endbstat to true
f.write("True")
f.close()

timestat = 0
#----------------------
#Stuff for Weight Sensor
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(1)

hx.reset()
#------------------------------
#Stuff for Temp Sensor
thermometer_address = 0x5a

thermometer = MLX90614(thermometer_address)
#------------------------------
#Substitute for induction heater toggle
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)
#---------------------------------
#Set up for vibration Sensor
Vib_Start()

while True: #NEED THIS SHIT FOR THE WINDOW TO UPDATE IN REAL TIME
    #--------------------------------------------------------------------
    #code for weight sensor input
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        if False:
            np_arr8_string = hx.get_np_arr8_string()
            binary_string = hx.get_binary_string()
            #print(binary_string + " " + np_arr8_string)
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        #val = hx.get_weight(5)
        val = (1.88*pow(10, -9)*(hx.read_long()**2))+ (0.0019367*hx.read_long())-67
        print(val)


        #putting sensor data in text file to be read
        f = open("Data_Sensor_Weight.txt", "w")
        f.write(str(round(val,1)))
        f.close()
        
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
    #---------------------------------------------------------------------------
    #Temperature Sensor Code
    Temp = thermometer.get_obj_temp()
    
    f = open("Data_Temperature.txt", "w")
    f.write(str(round(Temp,1)))
    f.close()
    #--------------------------------------------------------------------------
    #Vibration Sensor Code
    vibration = readvalue()

    f = open("Data_Vibration_Sensor.txt", "w")
    f.write(str(vibration))
    f.close()
    
    #----------------------------------------------------------------------------
    #Update code to endure GUI labels and stats stay up to date in real time
    time.sleep(.5)
    updatedict()
    Window.update()
    #-------------------------------------------------------------------------------
    #main control loop for interpreting sensor data and toggling the induction heater
    if MyDictionary["EndBStat"] == "False":
        if int(MyDictionary["SenseWeight"]) < int(MyDictionary["NWweight"]):
            ErrorTxt1.config(text = "No Jazzve Detected", bg = "yellow")
        elif int(MyDictionary["SenseWeight"]) < int(MyDictionary["Wweight"])-15:
            ErrorTxt1.config(text = "Not Enought Water", bg = "yellow")
        elif int(MyDictionary["SenseWeight"])> int(MyDictionary["Wweight"])+15:
            ErrorTxt1.config(text = "Too Heavy", bg = "yellow")
        elif int(MyDictionary["Wweight"]) - 15 < int(MyDictionary["SenseWeight"]) < int(MyDictionary["Wweight"])+15:
            if 1150< MyDictionary["Vibration"] < 1250:#checks to see if vibration is in range of state before boiling
                GPIO.output(26, GPIO.HIGH)
                print("Induction Heater On")
            else:
                time.sleep(1)
                timestat+=1
                print("timestat incrimented")
                if timestat == 5:
                    GPIO.output(26, GPIO.LOW)
                    print("Induction Heater Off")
                    timestat = 0

Window.mainloop()
