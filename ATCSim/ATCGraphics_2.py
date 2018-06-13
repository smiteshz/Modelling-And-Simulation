import numpy as np
from tkinter import Frame, Canvas, Tk
from enum import Enum
from collections import namedtuple, defaultdict
from math import atan, degrees, cos, sin, radians
from time import sleep

INDEX = 0
FList = []
LandTimes = []
atc = None
Event = namedtuple('Event', ['action', 'time', 'airplane'])
RunwayLoc = (35, 20)
HLD1Loc = (20, 10)
HLD2Loc = (20, 30)
allAirplanes = []
gui = None
tk = None
BK = []

RunwayObj = namedtuple('RWY', ['name', 'alt', 'pos'])

R25a = RunwayObj("RWY25A", 100, pos=list(RunwayLoc))

def dist(a, b):
    return abs(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5)


def heading(a, b):
    if (a[0] - b[0])!=0:
        retval = degrees(atan((a[1] - b[1]) / (a[0] - b[0])))
    else:
        retval = 90
    return retval


def nextCoordinates(hdg, currentPosition, airSpeed):
    airDistance = airSpeed / 1.0
    nextX = currentPosition[0] + airDistance * cos(radians(hdg))
    nextY = currentPosition[1] + airDistance * sin(radians(hdg))
    # print(nextX,nextY)
    return [nextX, nextY]

class Airplane:
    def __init__(self, arrival):
        global INDEX, RunwayLoc
        self.ID = INDEX
        INDEX += 1
        self.action = "LND"  #np.random.choice(["LND", "TOF"])
        if self.action == "LND":
            self.hdg = np.random.randint(0, 90)
            self.airspeed = 1#np.random.randint(1, 4)
            self.alt = np.random.randint(1000, 10000)
            self.arrival = arrival
            self.hldctr = 0
            self.ctr = 0
            self.landing = 0
            self.land_time = 0
            self.dest = None
            if np.random.sample() < 0.5:
                self.pos = np.array([0, np.random.randint(0, 20)])
            else:
                self.pos = np.array([np.random.randint(0, 35), 0])
        else:
            self.hdg = 0
            self.airspeed = 0
            self.alt = 1000
            self.arrival = arrival
            self.pos = np.array(RunwayLoc)
        return

    def __repr__(self):
        return (str(self.ID))

    def __str__(self):
        return ("%s"%self.ID)
        # return ("Airplane %s at position [%d,%d] and altitude %d, heading %d" % (
        #     self.ID, self.pos[0], self.pos[1], self.alt, self.hdg))

    def step(self, clock):
        global RunwayLoc, HLD1Loc, HLD2Loc, FList
        if self.action == "LND":
            # print("Landing Advance")
            self.pos = np.array(nextCoordinates(self.hdg, self.pos, self.airspeed))
            if self.dest != None:
                if np.array_equal(np.round(self.pos),self.dest):
                    if np.array_equal(self.dest, RunwayLoc):
                        event = [i for i in FList if i.time == clock + 1]
                        if Event("LND", clock + 1, self) not in event:
                            FList.append(Event("LND", clock + 1,  self))
                    elif np.array_equal(self.dest, HLD1Loc) or np.array_equal(self.dest,HLD2Loc):
                        event = [i for i in FList if i.time == clock + 1]
                        if Event("HLD", clock + 1, self) not in event:
                            FList.append(Event("HLD", clock + 1, self))


        elif self.action == "HLD":
            if self.hldctr == 0:
                self.hdg = 0
                self.ctr +=1
            elif self.hldctr == 1:
                self.hdg = 90
                self.ctr+=1
            elif self.hldctr == 2:
                self.hdg = 180
                self.ctr+=1
            elif self.hldctr == 3:
                self.hdg = 270
                self.ctr+=1
            if self.ctr == 3:
                self.ctr = 0
                self.hldctr += 1
                if self.hldctr == 4:
                    self.hldctr = 0
            self.pos = np.array(nextCoordinates(self.hdg, self.pos, self.airspeed))
        elif self.action == "TOF":
            self.pos = RunwayLoc

    def startTaxi(self, clock):
        taxiTime = np.floor(np.random.normal(120, 60))
        return np.ceil(clock + taxiTime)

    def initiateHolding(self, clock):
        self.action = "HLD"
        return

    def initiateLanding(self, clock):
        global FList
        self.action = "TDN"
        return

class GUI(Frame):
    def __init__(self, window):
        super().__init__()
        self.root = window
        self.canvas = Canvas(self.root, width=800, height=800)
        self.canvas.pack()
        self.checkered(self.canvas, 20, 800, 800)
        self.airplanes = []
        self.mapping = defaultdict(list)
        self.scale = 20
        self.objectScale = 500
        return

    def addObject(self, obj):
        temp = self.canvas.create_oval(obj.pos[0] * self.scale - obj.alt / self.objectScale,
                                       obj.pos[1] * self.scale - obj.alt / self.objectScale,
                                       obj.pos[0] * self.scale + obj.alt / self.objectScale,
                                       obj.pos[1] * self.scale + obj.alt / self.objectScale, outline='white',
                                       fill='blue')
        try:
            self.mapping.update({obj: temp})
        except:
            pass
        self.airplanes.append(temp)
        self.canvas.pack()
        self.root.update()
        return

    def removeObject(self, obj):
        removal = self.mapping[obj]
        self.canvas.delete(removal)
        self.canvas.pack()
        self.root.update()

    def updatePosition(self):
        global allAirplanes
        for i in allAirplanes:
            shape = self.mapping[i]
            self.canvas.coords(shape, i.pos[0] * self.scale - i.alt / self.objectScale,
                               i.pos[1] * self.scale - i.alt / self.objectScale,
                               i.pos[0] * self.scale + i.alt / self.objectScale,
                               i.pos[1] * self.scale + i.alt / self.objectScale)
        self.root.update()
        return

    def checkered(self, canvas, line_distance, h, w):
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, h, line_distance):
            canvas.create_line(x, 0, x, w, fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, h, line_distance):
            canvas.create_line(0, y, w, y, fill="#476042")


class RunwayMode(Enum):
    TAKEOFF = 0
    LANDING = 1


class ATC(object):
    def __init__(self):
        self.totalcap = 0
        self.LNDPLANES = []
        self.TOFPLANES = []
        self.HLD1 = []
        self.HLD2 = []
        self.HLD = []
        self.LNDCLR = None
        self.TOFCLR = None
        self.mode = RunwayMode.LANDING
        self.last_tick = 0
        self.runwayclr = True
        self.runway_c = 0
        self.ctr = 0

    def checkLanding(self,clock):
        global FList
        if self.last_tick == self.LNDCLR:
            self.ctr+=1
        else:
            self.last_tick = self.LNDCLR
        if self.ctr >= 120:
            self.LNDCLR = None
            self.ctr = 0
        if self.mode == RunwayMode.LANDING and self.LNDCLR == None:
            airplane = self.HLD.pop(0)
            print("Dequeuing hld plane",airplane," at ",clock," at position ",airplane.pos)
            try:
                self.HLD1.remove(airplane)
            except:
                self.HLD2.remove(airplane)
            self.LNDCLR = airplane
            airplane.action = "LND"
            FList.append(Event("HLDEXT", clock + 1, airplane))
        else:
            return

    def manage(self, events, clock):
        global FList, RunwayLoc, allAirplanes, gui, LandTimes
        while len(events) != 0:
            ev = events.pop(0)
            if ev.action == "ARR":
                print("Runway Status", self.LNDCLR)
                allAirplanes.append(ev.airplane)
                gui.addObject(ev.airplane)
                if ev.airplane.action == "LND":
                    self.LNDPLANES.append(ev.airplane)
                    if self.LNDCLR == None and self.mode == RunwayMode.LANDING:
                        self.proceedLand(ev)
                    else:
                        self.proceedHold(ev)
                else:
                    self.TOFPLANES.append(ev.airplane)
                    ev.airplane.startTaxi(ev)
            elif ev.action == "LND":
                ev.airplane.initiateLanding(ev.time)
                sample_lnd_time = np.random.normal(60,15)
                print("Landing airplane",ev.airplane," at ",ev.time + abs(sample_lnd_time) + 1)
                FList.append(Event("RNC", ev.time + abs(np.round(sample_lnd_time)) + 1, ev.airplane))
            elif ev.action == "HLD":
                print(ev.airplane.pos)
                ev.airplane.initiateHolding(ev.time)
            elif ev.action == "EXT":
                ev.airplane.hdg = heading(ev.airplane.pos,[0,0])
                FList.append(Event("DEL",ev.time + dist(ev.airplane.pos,[0,0]), ev.airplane))
            elif ev.action == "TOF":
                pass
            elif ev.action == "DEL":
                allAirplanes.remove(ev.airplane)
                airplane = ev.airplane
                gui.removeObject(airplane)
                del airplane
            elif ev.action == "RNC":
                # if ev.airplane.action == "LND":
                ev.airplane.land_time = ev.time
                LandTimes.append(ev.airplane.land_time - ev.airplane.arrival)
                self.LNDCLR = None
                self.LNDPLANES.remove(ev.airplane)
                FList.append(Event("DEL",ev.time +1 , ev.airplane))
            elif ev.action == "HLDEXT":
                self.proceedLand(ev)


    def proceedHold(self,event):
        global HLD1Loc,HLD2Loc
        airplane = event.airplane
        self.HLD.append(airplane)
        if len(self.HLD1)<=23:
            self.HLD1.append(airplane)
            airplane.hdg = heading(airplane.pos, HLD1Loc)
            airplane.dest = HLD1Loc
            #FList.append(Event("HLD", event.time + np.round(timereq), event.airplane))
        elif len(self.HLD2)<=23:
            self.HLD2.append(airplane)
            airplane.hdg = heading(airplane.pos, HLD2Loc)
            airplane.dest = HLD2Loc
            #FList.append(Event("HLD", event.time + np.round(timereq), event.airplane))
        else:
            self.LNDPLANES.remove(event.airplane)
            FList.append(Event("EXT", event.time, event.airplane))
        return

    def proceedLand(self,event):
        global RunwayLoc, FList
        airplane = event.airplane
        airplane.hdg = heading(airplane.pos, RunwayLoc)
        airplane.dest = RunwayLoc
        self.LNDCLR = airplane
        #FList.append(Event("LND", event.time + np.round(timereq), event.airplane))
        return


    def TCAS(self, airplane):
        collidingPlanes = [i for i in self.LNDPLANES if dist(i, airplane.curPosition) <= 1 and i.ID != airplane.ID]
        for i in collidingPlanes:
            if abs(i.alt - airplane.alt) <= 1000:
                i.alt -= 1000
                airplane.alt += 1000
        return

def setup():
    global FList, atc, allAirplanes, gui
    atc = ATC()
    trigger = np.array([1])
    while (trigger[-1] < 1800):
        trigger = np.append(trigger, trigger[-1] + int(np.random.exponential(20) + 1))
    trigger = np.delete(trigger, obj=-1)
    trigger = np.delete(trigger, obj=0)
    for i in trigger:
        newPlane = Airplane(i)
        allAirplanes.append(newPlane)
        FList.append(Event('ARR', i, newPlane))
    tk = Tk()
    gui = GUI(tk)
    gui.addObject(R25a)
    return

def run(iterations):
    global FList, atc, allAirplanes, gui
    print(FList)
    for x in range(iterations):
        gui.updatePosition()
        if len(atc.HLD) != 0:
            atc.checkLanding(x)
        events = [i for i in FList if i.time == x]
        print("Events for clock: ", x, " : ", events) if len(events) != 0 else 2
        if len(events) == 0:
            generatePlanes = [i for i in allAirplanes if i.arrival <= x]
            for y in generatePlanes:
                y.step(x)
                # sleep(0.001)
            continue
        atc.manage([i for i in FList if i.time == x], x)
        generatePlanes = [i for i in allAirplanes if i.arrival <= x]
        for y in generatePlanes:
            y.step(x)
        print("\rClock = %d" % x, end="\r")
        # sleep(0.001)
    return



if __name__ == '__main__':
    #times = []
    # for i in range(10):
    setup()
    run(1800)
    #times.append(np.mean(np.array(LandTimes)))
    print(FList)
    print(LandTimes)
    print(np.mean(LandTimes))
    #
    # print("Average Times required for landing",times)
    # print(atc.LNDPLANES)
    # print(atc.HLD1)
    # print(atc.HLD2)
    # print(atc.HLD)
    # print("Future List", FList)
    # print(LandTimes)
    # print(np.mean(np.array(LandTimes)))
    # cessna = Airplane(0)
    # print(cessna.pos)
    # print(cessna.hdg)
    # atc.manage([Event("ARR",0,cessna)],0)
    # print(cessna.hdg)
    # i = 0
    # while not(np.array_equal(np.round(cessna.pos),RunwayLoc)):
    #     cessna.step(i)
    #     print(cessna.pos)
    #     i+=1
    # print(i)
    # print(FList)


