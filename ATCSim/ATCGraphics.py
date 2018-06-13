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
    return degrees(atan((a[1] - b[1]) / (a[0] - b[0])))


def nextCoordinates(heading, currentPosition, airSpeed):
    airDistance = airSpeed / 1.0
    nextX = currentPosition[0] + airDistance * cos(radians(heading))
    nextY = currentPosition[1] + airDistance * sin(radians(heading))
    return [nextX, nextY]


class Airplane:
    def __init__(self, arrival):
        global INDEX, RunwayLoc
        self.ID = INDEX
        INDEX += 1
        self.action = "LND"  #np.random.choice(["LND", "TOF"])
        if self.action == "LND":
            self.hdg = np.random.randint(0, 90)
            self.airspeed = np.random.randint(1, 4)
            self.alt = np.random.randint(1000, 10000)
            self.arrival = arrival
            self.hldctr = 0
            self.landing = 0
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
        return ("Airplane %s at position [%d,%d] and altitude %d, heading %d" % (
            self.ID, self.pos[0], self.pos[1], self.alt, self.hdg))

    def step(self, clock):
        self.landing += 1
        if self.action == "LND":
            # print("Landing Advance")
            self.pos = np.array(np.round(nextCoordinates(self.hdg, self.pos, self.airspeed)))
        elif self.action == "HLD":
            self.airspeed = 1
            # print("Holding Advance")
            self.hldctr = self.hldctr + 1 if self.hldctr < 5 else 0
            if self.hldctr == 0:
                self.hdg = self.hdg + 90 if self.hdg <= 270 else 0
            self.pos = np.array(np.round(nextCoordinates(self.hdg, self.pos, self.airspeed)))
        elif self.action == "TOF":
            self.pos = RunwayLoc

    def startTaxi(self, clock):
        taxiTime = np.floor(np.random.normal(120, 60))
        return np.ceil(clock + taxiTime)


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
        self.LNDQ = []
        self.TOFQ = []
        self.mode = RunwayMode.LANDING
        self.last_tick = 0
        self.runwayclr = True
        self.runway_c = 0

    def clearToLand(self, events, clock):
        global FList, RunwayLoc, allAirplanes, gui
        if len(self.HLD1)!=0:
            if len(self.LNDQ)==0:
                self.assignLand(self.HLD1.pop(0))

        elif len(self.HLD2)!=0:
            if len(self.LNDQ)==0:
                self.assignLand(self.HLD2.pop(0))

    def manage(self, events, clock):
        global FList, RunwayLoc, allAirplanes, gui

        while len(events) != 0:
            ev = events.pop(0)
            #print(ev)
            if ev.action == "ARR":
                if self.totalcap >= 100:
                    events.append(Event("EXT", clock, ev.airplane))
                else:
                    gui.addObject(ev.airplane)
                    self.totalcap += 1
                    events.append(Event("ASN", clock, ev.airplane))
            elif ev.action == "WAA":
                if np.array_equal(ev.airplane.pos, RunwayLoc):
                    self.initiateLanding(ev.airplane)

            elif ev.action == "ASN":
                if ev.airplane.action == "LND":
                    self.LNDPLANES.append(ev.airplane)
                    retevent = self.assignflightplan(ev)
                    FList.append(retevent)
                else:
                    retevent = self.assignTakeoff(ev)
                    FList.append(retevent)
            elif ev.action == "ADJ":
                self.TCAS(events.airplane)
            elif ev.action == "LCLR":
                testFail = np.random.sample()
                if testFail <= 0.998:
                    FList.append(Event("RNC", np.ceil(clock + np.random.normal(60, 20)), ev.airplane))
                    print(FList[-1])
                else:
                    self.assignflightplan(ev)
            elif ev.action == "TOF":
                testFail = np.random.sample()
                if testFail <= 0.998:
                    FList.append(Event("RNC", clock + np.random.normal(60, 20), ev.airplane))
            elif ev.action == "RNC":
                print("Plane successfully landed", ev.airplane)
                ev.airplane.landing = clock
                self.runway_c = self.runway_c + 1 if self.runway_c < 5 else 0
                self.LNDPLANES.remove(ev.airplane)
                self.runwayclr = True
                self.totalcap -= 1
                gui.removeObject(ev.airplane)
            elif ev.action == "HLD1":
                ev.airplane.action = "HLD"
            elif ev.action == "HLD2":
                ev.airplane.action = "HLD"
            elif ev.action == "EXT":
                print("Airplane exceeded the ARR limit", ev.airplane)
                gui.removeObject(ev.airplane)

    def assignLand(self, airplane):
        global RunwayLoc, HLD1Loc, HLD2Loc
        curPosition = airplane.pos
        newHeading = heading(curPosition, RunwayLoc)
        print("New Landing Heading from Holding:", newHeading, airplane)
        distance = dist(curPosition, RunwayLoc)
        timereq = distance / airplane.airspeed
        airplane.hdg = newHeading
        self.runwayclr = False
        return

    def assignflightplan(self, event):
        global RunwayLoc, HLD1Loc, HLD2Loc
        if len(self.LNDQ) == 0 and self.runwayclr == True:
            curPosition = event.airplane.pos
            newHeading = heading(curPosition, RunwayLoc)
            print("New Landing Heading :", newHeading, event.airplane)
            distance = dist(curPosition, RunwayLoc)
            timereq = distance / event.airplane.airspeed
            event.airplane.hdg = newHeading
            self.LNDQ.append(event.airplane)
            print(self.LNDQ)
            self.runwayclr = False
            print("Landing at ", np.ceil(event.time + timereq))
            return Event("LCLR", np.ceil(event.time + timereq), event.airplane)
        elif len(self.HLD1) <= 23:
            curPosition = event.airplane.pos
            newHeading = heading(curPosition, HLD1Loc)
            print("New HLD1 Heading :", newHeading, event.airplane)
            distance = dist(curPosition, HLD1Loc)
            timereq = distance / event.airplane.airspeed
            event.airplane.hdg = newHeading
            self.HLD1.append(event.airplane)
            return Event("HLD1", np.ceil(event.time + timereq), event.airplane)
        elif len(self.HLD2) <= 23:
            curPosition = event.airplane.pos
            newHeading = heading(curPosition, HLD2Loc)
            print("New HLD2 Heading :", newHeading, event.airplane)
            distance = dist(curPosition, HLD1Loc)
            timereq = distance / event.airplane.airspeed
            self.HLD1.append(event.airplane)
            event.airplane.hdg = newHeading
            return Event("HLD2", np.ceil(event.time + timereq), event.airplane)
        else:
            return Event("EXT", event.time, event.airplane)

    def TCAS(self, airplane):
        collidingPlanes = [i for i in self.LNDPLANES if dist(i, airplane.curPosition) <= 1 and i.ID != airplane.ID]
        for i in collidingPlanes:
            if abs(i.alt - airplane.alt) <= 1000:
                i.alt -= 1000
                airplane.alt += 1000
        return

    def assignTakeoff(self, event):
        airplane = event.airplane
        return Event("TOF", airplane.startTaxi(event.time), airplane)

def setup():
    global FList, atc, allAirplanes, gui, tk, RunwayObj
    atc = ATC()
    trigger = np.array([1])
    while (trigger[-1] < 7200):
        trigger = np.append(trigger, trigger[-1] + int(np.random.exponential(scale=120) + 1))
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
    global FList, atc, allAirplanes, tk, gui
    print(FList)
    for x in range(iterations):
        gui.updatePosition()
        events = [i for i in FList if i.time == x]
        #print("Events for clock: ", x, " : ", events) if len(events) != 0 else 2
        if len(events) == 0:
            generatePlanes = [i for i in allAirplanes if i.arrival <= x]
            for y in generatePlanes:
                y.step(x)
                sleep(0.001)
            continue
        atc.manage([i for i in FList if i.time == x], x)
        generatePlanes = [i for i in allAirplanes if i.arrival <= x]
        for y in generatePlanes:
            y.step(x)
        sleep(0.001)
        print("\rClock = %d" % x, end="\r")
    return


if __name__ == '__main__':
    setup()
    run(7200)
    print([i.arrival for i in allAirplanes])
    gui.root.mainloop()
