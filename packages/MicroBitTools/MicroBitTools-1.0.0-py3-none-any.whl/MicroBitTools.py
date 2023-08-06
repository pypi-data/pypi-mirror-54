import shutil
import os
import serial
import requests

readymicrobithexurl="https://download2268.mediafire.com/h0s925j6zbeg/d9hg2oihzf8ur8i/microbitserialsystem+%282%29.hex"


class InternalTools:
    def yntoboolean(data="no"):
        data = data.lower()
        if data == "y":
            return True
        elif data == "n":
            return False
        else:
            return "ERROR: \nInput was not either y or n"


def export(pythonfile, dirtomoveto):
    pyfilenoext = pythonfile[:-3]
    os.system("cd "+os.getcwd())
    os.system('py2hex "' + pythonfile + '"')
    print("Moving to microbit.")
    shutil.move(pyfilenoext+".hex", dirtomoveto)
    print("Done!")


class SerialSystem:

    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = "COM3"
    ser.open()

    microbitpath = "F:\\"

    #FIXA
    def ReadyMicrobit(self, printb=False):
        #shutil.copyfile(os.getcwd() + "\\src\\" + "microbitserialsystem.hex", self.microbitpath+"SerialSystem.hex")
        #shutil.copy
        if printb:
            print("Downloading HEX")
        url = readymicrobithexurl
        r = requests.get(url)
        if printb:
            print("Downloaded HEX")
            print("Fixing HEX")
        content = ""
        contentb = r.content
        contentb = str(contentb)
        contentb = contentb[:-1]
        contentb = contentb[2:]
        contentsplit = contentb.split("\\n")
        for i in contentsplit:
            content = content+i+"\n"
        if printb:
            print("Fixed HEX\n"+str(r.content))
            print("Moving HEX to microbit")

        outF = open(self.microbitpath+"SerialSystem.hex", "w")
        outF.write(content)
        if printb:
            print("Moved HEX to microbit")

    def read(self):

        try:
            mbd = str(self.ser.readline())
        except serial.serialutil.SerialException:
            return {"error": "Can not find MicroBit"}
        except IndexError:
            return {"error": "Unknown error"}

        try:
            mbdf = mbd[2:]
            # mbdf = mbdf.replace(" ", "")
            mbdf = mbdf.replace("'", "")
            mbdf = mbdf.replace("\\r\\n", "")
            mbdf = mbdf.replace("\\xc2", "")
        except IndexError:
            return {"error": "Could not read!"}

        if mbdf.startswith("}"):
            mbdf = mbdf[1:]
            mbdfsplit = mbdf.split("\\xa7")
            try:
                temp = int(mbdfsplit[0])
                try:
                    brightness = int(mbdfsplit[1])
                except ValueError:
                    brightness = ""
                ButtonA = InternalTools.yntoboolean(mbdfsplit[2][2:])
                ButtonB = InternalTools.yntoboolean(mbdfsplit[3][2:])
                CmpsH = int(mbdfsplit[4])

                dicmbd = {
                    "temp": temp,
                    "brightness": brightness,
                    "Buttons": {
                        "A": ButtonA,
                        "B": ButtonB
                    },
                    "CompassHeading": CmpsH
                }

                return dicmbd
            except IndexError:
                return {"error": "Could not read!"}
        else:
            return {"error": "Could not read!"}


def test():
    print("SUCCESS")