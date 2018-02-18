from tkinter import Tk, Label, Button, Toplevel, messagebox, PhotoImage
from tinydb import TinyDB, Query
from matplotlib import pyplot
import random
import smartOff
import calendar;
import time;
import http.client
from cron import startThread1
ipAddress = "192.168.137.146"
salt = 25
key = 1
def sendSignalToDevice(predict) :
    actionVal = salt+key
    if predict:
        actionVal = actionVal + 1

    conn = http.client.HTTPConnection(ipAddress)
    actionStr = '/socket1On?action=' + str(actionVal) + '&salt=' + str(salt)
    r1 = conn.request('GET',actionStr)

class ShowImage:
    def __init__(self, master, path):
        print(path)
        self.graph = PhotoImage(file=path)
        Label(master, image = self.graph).pack()

class MicrowaveGUI:
    maxUsage = 0
    def __init__(self, master):
        self.label = Label(master, text="Control Microwave ")
        self.label.pack()

        self.threeHourDemo = Button(master, text="3 Hour Auto-Pilot Demo", command=self.threeHourDemoPredict)
        self.threeHourDemo.pack()

        self.threeHour = Button(master, text="3 Hour Auto-Pilot Current", command=self.threeHourPredict)
        self.threeHour.pack()

        self.instant = Button(master, text="Instant", command=self.instantPredict)
        self.instant.pack()
        
        db = TinyDB('metadata.json')
        metadata = Query()
        app = db.search(metadata.appliance == 'microwave')
        self.maxUsage = app[-1]['maxUsage']
        self.model = smartOff.loadMicrowaveModel()
       # startThread1(self)
	
    def test(self):
        print("ISHUUUUUUUUUUUUU")
        timeGM = time.localtime()
        print(timeGM)
        ts = time.time() #calendar.timegm(timeGM)
        print("PREDICTING FOR", ts)
        predict = smartOff.predictForSingleTime(self.model, str(ts), self.maxUsage, 'MICROWAVE')
        print(predict)
        sendSignalToDevice(predict)
        return predict
       # 

    def threeHourPredict(self):
        timeGM = time.localtime()
        print(timeGM)
        ts = time.time() #calendar.timegm(timeGM)
        print("PREDICTING FOR", ts)
        usage = smartOff.predictOnNext3Hours(self.model, str(ts), self.maxUsage)
        labelG = str(timeGM.tm_mon) + '/'+ str(timeGM.tm_mday) + '/' + str(timeGM.tm_year)
        labelG = labelG + " From " + str(timeGM.tm_hour) + ":"+str(timeGM.tm_min) + " to "
        labelG = labelG + " To " + str(timeGM.tm_hour+3) + ":"+str(timeGM.tm_min)
        pyplot.plot(usage, label = labelG)
        pyplot.legend()
        graphFile = 'images/' + ''.join(random.choice('abcdefghighklmnopqrst') for _ in range(5))+'.png'
        pyplot.savefig(graphFile)
        pyplot.clf()
        img_root = Toplevel()
        img_gui = ShowImage(img_root, graphFile)
        img_root.mainloop()

    def threeHourDemoPredict(self):
        print("PREDICT")
        usage = smartOff.predictOnNext3Hours(self.model, "1515578400", self.maxUsage)
        pyplot.plot(usage, label = "10th Jan 2018 5 AM to 8 AM")
        pyplot.legend()
        graphFile = 'images/' + ''.join(random.choice('abcdefghighklmnopqrst') for _ in range(5))+'.png'
        pyplot.savefig(graphFile)
        pyplot.clf()
        img_root = Toplevel()
        img_gui = ShowImage(img_root, graphFile)
        img_root.mainloop()


    def instantPredict(self):
        timeGM = time.localtime()
        print(timeGM)
        ts = time.time() #calendar.timegm(timeGM)
        print("PREDICTING FOR", ts)
        predict = smartOff.predictForSingleTime(self.model, str(ts), self.maxUsage, 'MICROWAVE')
        sendSignalToDevice(predict)
        startThread1(self)
        if (predict):
            messagebox.showinfo("Microwave Operation", "Microwave should be ON. Syncing with device")
        else:
            messagebox.showinfo("Microwave Operation", "Microwave should be OFF. Syncing with device")



class TVGUI:
    maxUsage = 0
    def __init__(self, master):
        self.label = Label(master, text="Control TV ")
        self.label.pack()

        self.threeHourDemo = Button(master, text="3 Hour Auto-Pilot Demo", command=self.threeHourDemoPredict)
        self.threeHourDemo.pack()

        self.threeHour = Button(master, text="3 Hour Auto-Pilot Current", command=self.threeHourPredict)
        self.threeHour.pack()

        self.instant = Button(master, text="Instant", command=self.instantPredict)
        self.instant.pack()

        db = TinyDB('metadata.json')
        metadata = Query()
        app = db.search(metadata.appliance == 'tv')
        self.maxUsage = app[-1]['maxUsage']
        print(self.maxUsage)
        self.model = smartOff.loadTVModel()

    def threeHourPredict(self):
        timeGM = time.localtime()
        ts = time.time() #calendar.timegm(timeGM)
        print("PREDICTING FOR", ts)
        usage = smartOff.predictOnNext3Hours(self.model, str(ts), self.maxUsage)
        labelG = str(timeGM.tm_mon) + '/'+ str(timeGM.tm_mday) + '/' + str(timeGM.tm_year)
        labelG = labelG + " From " + str(timeGM.tm_hour) + ":"+str(timeGM.tm_min) + " to "
        labelG = labelG + " To " + str(timeGM.tm_hour+3) + ":"+str(timeGM.tm_min)
        pyplot.plot(usage, label = labelG)
        pyplot.legend()
        graphFile = 'images/'+ ''.join(random.choice('abcdefghighklmnopqrst') for _ in range(5))+'.png'
        pyplot.savefig(graphFile)
        pyplot.clf()
        img_root = Toplevel()
        img_gui = ShowImage(img_root, graphFile)
        img_root.mainloop()

    def threeHourDemoPredict(self):
        timeGM = time.localtime()
        ts = calendar.timegm(timeGM)
        print("PREDICTING FOR", ts)
        usage = smartOff.predictOnNext3Hours(self.model, str(ts), self.maxUsage)
        pyplot.plot(usage, label = "6th July 2017 1 PM to 4 PM")
        pyplot.legend()
        graphFile = 'images/'+ ''.join(random.choice('abcdefghighklmnopqrst') for _ in range(5))+'.png'
        pyplot.savefig(graphFile)
        pyplot.clf()
        img_root = Toplevel()
        img_gui = ShowImage(img_root, graphFile)
        img_root.mainloop()

    def instantPredict(self):
        ts = time.time()
        predict = smartOff.predictForSingleTime(self.model, str(ts), self.maxUsage, 'TV')
        sendSignalToDevice(predict)
        if (predict):
            messagebox.showinfo("TV Operation", "TV should be ON. Syncing with device")
        else:
            messagebox.showinfo("TV Operation", "TV should be OFF. Syncing with device")


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("SmartOFF")

        self.label = Label(master, text="Turns off appliances automatically")
        self.label.pack()

        self.microwave = Button(master, text="Microwave", command=self.microwave)
        self.microwave.pack()

        self.tv = Button(master, text="TV", command=self.tv)
        self.tv.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        conn = http.client.HTTPConnection(ipAddress)

    def microwave(self):
        mw_root = Tk()
        mw_gui = MicrowaveGUI(mw_root)
        mw_root.mainloop()


    def tv(self):
        tv_root = Tk()
        tv_gui = TVGUI(tv_root)
        tv_root.mainloop()

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
