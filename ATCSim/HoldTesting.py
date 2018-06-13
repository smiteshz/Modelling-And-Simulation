import numpy as np
from tkinter import Frame, Canvas, Tk
from enum import Enum
from collections import namedtuple, defaultdict
from math import atan, degrees, cos, sin, radians
from time import sleep

INDEX = 0
FList = []
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
    try:
        retval = degrees(atan((a[1] - b[1]) / (a[0] - b[0])))
    except:
        retval = 90
    return retval


def nextCoordinates(hdg, currentPosition, airSpeed):
    # print(currentPosition)
    airDistance = airSpeed / 1.0
    # print(airDistance)
    # print(hdg)
    # print(cos(radians(hdg)))
    # print(sin(radians(hdg)))
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
            self.landing = 0
            self.ctr = 0
            self.dest = None
            if np.random.sample() < 0.5:
                self.pos = np.array([0, np.random.randint(0, 40)])
            else:
                self.pos = np.array([np.random.randint(0, 40), 0])
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
                        FList.append(Event("LND", clock+1,  self))
                    elif np.array_equal(self.dest, HLD1Loc) or np.array_equal(self.dest,HLD2Loc):
                        FList.append(Event("HLD", clock+1, self))


        elif self.action == "HLD":
            # self.airspeed = 1
            # print(self.hldctr)
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
            # print("Holding Advance")
            # self.hldctr = self.hldctr + 1 if self.hldctr < 5 else 0
            # if self.hldctr == 0:
            #     self.hdg = self.hdg + 90 if self.hdg <= 270 else 0
            # self.pos = np.array(nextCoordinates(self.hdg, self.pos, self.airspeed))
            # print(self.pos)
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

    def checkLanding(self,clock):
        global FList
        if self.mode == RunwayMode.LANDING and self.LNDCLR == None:
            print("Dequeuing hld plane at ",clock)
            airplane = self.HLD.pop(0)
            try:
                self.HLD1.remove(airplane)
            except:
                self.HLD2.remove(airplane)
            self.LNDCLR = airplane
            airplane.action = "LND"
            self.proceedLand(Event("HLDEXT", clock, airplane))
        else:
            return

    def manage(self, events, clock):
        global FList, RunwayLoc, allAirplanes, gui
        print(events)
        while len(events) != 0:
            ev = events.pop(0)
            print(ev)
            if ev.action == "ARR":
                allAirplanes.append(ev.airplane)
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
                sample_lnd_time = np.random.normal(120,30)
                print("Landing airplane",ev.airplane," at ",clock + sample_lnd_time)
                FList.append(Event("RNC", np.round(clock + sample_lnd_time), ev.airplane))
            elif ev.action == "HLD":
                ev.airplane.initiateHolding(ev.time)
            elif ev.action == "EXT":
                ev.airplane.hdg = heading(ev.airplane.pos,[0,0])
                FList.append(Event("DEL",ev.time + dist(ev.airplane.pos,[0,0]), ev.airplane))
            elif ev.action == "TOF":
                pass
            elif ev.action == "DEL":
                allAirplanes.remove(ev.airplane)
                del ev.airplane
            elif ev.action == "RNC":
                # if ev.airplane.action == "LND":
                self.LNDCLR = None
                self.LNDPLANES.remove(ev.airplane)


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
            #FList.append(Event("EXT", event.time, event.airplane))
        return

    def proceedLand(self,event):
        global RunwayLoc, FList
        airplane = event.airplane
        # if airplane.action == "HLD":
        #     airplane.action = "LND"
        #     self.HLD.remove(airplane)
        #     try:
        #         self.HLD1.remove(airplane)
        #     except:
        #         self.HLD2.remove(airplane)
        airplane.hdg = heading(airplane.pos, RunwayLoc)
        # distance = dist(airplane.pos, RunwayLoc)
        # timereq = distance/airplane.airspeed
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
    global FList, atc, allAirplanes
    atc = ATC()
    trigger = np.array([1])
    while (trigger[-1] < 7200):
        trigger = np.append(trigger, trigger[-1] + int(np.random.exponential(scale=360) + 1))
    trigger = np.delete(trigger, obj=-1)
    trigger = np.delete(trigger, obj=0)
    for i in trigger:
        newPlane = Airplane(i)
        allAirplanes.append(newPlane)
        FList.append(Event('ARR', i, newPlane))
    # tk = Tk()
    # gui = GUI(tk)
    # gui.addObject(R25a)
    return

def run(iterations):
    global FList, atc, allAirplanes
    print(FList)
    for x in range(iterations):
        # gui.updatePosition()
        events = [i for i in FList if i.time == x]
        print("Events for clock: ", x, " : ", events) if len(events) != 0 else 2
        if len(events) == 0:
            generatePlanes = [i for i in allAirplanes if i.arrival <= x]
            for y in generatePlanes:
                y.step(x)
                # sleep(0.001)
            continue
        if len(atc.HLD) != 0:
            atc.checkLanding(x)
        atc.manage([i for i in FList if i.time == x], x)
        generatePlanes = [i for i in allAirplanes if i.arrival <= x]
        for y in generatePlanes:
            y.step(x)
        print("\rClock = %d" % x, end="\r")
    return



if __name__ == '__main__':
    # setup()
    # run(7200)
    atc = ATC()
    cessna = Airplane(0)
    boeing = Airplane(0)
    print(cessna.pos)
    print(cessna.hdg)
    FList = [Event("ARR",0,cessna),Event("ARR",0,boeing)]
    run(1000)
    print(FList)
