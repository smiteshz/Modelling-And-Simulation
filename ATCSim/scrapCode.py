# atc = ATC()
    # cessna = Airplane(1)
    # print("\n%s spawned at [%s,%s] with heading %s and airspeed %s" % (
    #     cessna, cessna.pos[0], cessna.pos[1], cessna.hdg, cessna.airspeed))
    # atc.manage([Event("ARR", 1, cessna)], 1)
    # print("\n%s spawned at [%s,%s] with heading %s and airspeed %s" % (
    #     cessna, cessna.pos[0], cessna.pos[1], cessna.hdg, cessna.airspeed))



# if len(self.HLD1) != 0:
                #     airplane = self.HLD1.pop(0)
                #     self.assignLand(airplane)
                #     self.LNDQ.append(airplane)
                #     FList.append(
                #         Event("LCLR", clock + np.ceil(dist(airplane.pos, RunwayLoc)) / airplane.airspeed, airplane))
                # elif len(self.HLD2) != 0:
                #     airplane = self.HLD2.pop(0)
                #     self.assignLand(airplane)
                #     self.LNDQ.append(airplane)
                #     FList.append(
                #         Event("LCLR", clock + np.ceil(dist(airplane.pos, RunwayLoc)) / airplane.airspeed, airplane))


# print("Testing Heading")
#     a = Airplane(1)
#     a.hdg = 45
#     a.airspeed = 1
#     a.action = "LND"
#     a.pos = np.array([2,2])
#     print("Heading:", heading(a.pos,[10,12]))
#     a.hdg = heading(a.pos,[10,12])
#     print("Distance:", dist(a.pos,[10,12]))
#     print("Time:", dist(a.pos,[10,12])/a.airspeed)
#     time = dist(a.pos,[10,12])/a.airspeed
#     i = 0
#     while not(np.array_equal(np.round(a.pos),(10,12))):
#         a.step(i)
#         i+=1
#         print("Current Position",a.pos)