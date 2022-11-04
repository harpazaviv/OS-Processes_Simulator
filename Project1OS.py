import math
import random
import sys


class Process:
    def __init__(self):
        self.startT = 0 
        self.endT = 0 
        self.arrivalT = 0 
        self.serviceT= 0 
        self.HRRNratio = 0 
        self.serviceTimeLeft = 0


class Event:
    def __init__(self):
        self.time = 0
        self.type = 0 #1=arrival, 2=departure 3=swapping
        self.process = Process()

class CPU:
    def __init__(self):
        self.clock = 0
        self.busy = False
        self.currentProcess = Process()

class run_sim:
    def __init__(self, scheduler, lambda_val, avgServiceTime, q, endC):
        self.readyQueue = []
        self.eventQueue = []
        self.cpu = CPU()
        self.scheduler = scheduler 
        self.avgServiceTime = avgServiceTime 
        self.lambda_val = lambda_val
        self.q = q 
        self.endC = endC
        self.completedProcesses = 0
        self.turnaroundTime = 0 
        self.totalService = 0
        self.processesReadyQ = 0

    def FCFS(self):

        process1 = self.getProcess() 
        event1 = self.getEvent(process1.arrivalT, 1 , process1) #transfer process to event
        self.eventQueue.append(event1) #put the event in the event queue

        while self.completedProcesses < self.endC: 
            self.eventQueue.sort(key=lambda x: x.time)   #sort event queue with the event time 
            event = self.eventQueue.pop(0) #get event
            self.cpu.clock = event.time #clock=time of current event

            if event.type==1: #event is arrival 
                if self.cpu.busy == False: #if the cpu is not busy and ready queue is empty
                    self.cpu.busy = True # make the cpu busy and and change the event from an arrival to a departure (schedule the departure)
                    event.type = 2
                    event.process.endT = self.cpu.clock + event.process.serviceT
                    event.time = event.process.endT
                    self.eventQueue.append(event) 

                elif self.cpu.busy==True: #cpu is busy
                    self.readyQueue.append(event.process)
                else:
                    print("ERROR")
               
                newProcess = self.getProcess()
                newEventArr = self.getEvent(newProcess.arrivalT, 1 , newProcess)
                self.eventQueue.append(newEventArr) 

            elif event.type==2: #event is departure
                self.processesReadyQ += len(self.readyQueue) # number of completed process goes up
                self.completedProcesses += 1
                self.turnaroundTime += (self.cpu.clock - event.process.arrivalT)
                self.totalService += event.process.serviceT
                if len(self.readyQueue)==0:
                    self.cpu.busy = False

                else:
                    processDep = self.readyQueue.pop(0)
                    processDep.startT = self.cpu.clock
                    processDep.endT = processDep.startT + processDep.serviceT
                    newEventDep = self.getEvent(processDep.endT, 2 , processDep)
                    self.eventQueue.append(newEventDep)
            else:
                print("ERROR")

        self.completedProcesses = 0
        self.readyQueue.clear()
        self.eventQueue.clear()

    def SRTF(self):

        first_process = self.getProcess()
        first_event = self.getEvent(first_process.arrivalT, 1 , first_process)
        self.eventQueue.append(first_event)
        while self.completedProcesses < self.endC:
            self.eventQueue.sort(key=lambda x: x.time)  # sort the event queue
            event = self.eventQueue.pop(0)
            self.cpu.clock = event.time
            if event.type==1:
                if self.cpu.busy==False:
                    self.cpu.busy = True
                    event.type = 2
                    event.process.endT = self.cpu.clock + event.process.serviceTimeLeft
                    event.time = event.process.endT
                    self.eventQueue.append(event)
                    self.cpu.currentProcess = event.process

                elif self.cpu.busy==True:
                    self.readyQueue.append(event.process)
                    self.SRTFCalc()

                else:
                    print("ERROR")

                newProcess = self.getProcess()
                newEventArr = self.getEvent(newProcess.arrivalT, 1 , newProcess)
                self.eventQueue.append(newEventArr)

            elif event.type==2:
                self.processesReadyQ += len(self.readyQueue)
                self.completedProcesses += 1
                self.turnaroundTime += (self.cpu.clock - event.process.arrivalT)
                self.totalService += event.process.serviceT
                self.cpu.currentProcess = None

                if len(self.readyQueue)==0: #ready Q empty
                    self.cpu.busy = False
                else:
                    self.readyQueue.sort(key=lambda x: x.serviceTimeLeft)
                    processDep = self.readyQueue.pop(0)
                    processDep.startT = self.cpu.clock
                    processDep.endT = processDep.startT + processDep.serviceTimeLeft
                    self.cpu.currentProcess = processDep
                    newEventDep = self.getEvent(processDep.endT, 2 , processDep)
                    self.eventQueue.append(newEventDep)

            else:
                print("ERROR")

        self.completedProcesses = 0
        self.readyQueue.clear()
        self.eventQueue.clear()

    def HRRN(self):

        process1 = self.getProcess()
        event1 = self.getEvent(process1.arrivalT, 1 , process1)
        self.eventQueue.append(event1)

        while self.completedProcesses < self.endC:
            self.eventQueue.sort(key=lambda x: x.time)
            event = self.eventQueue.pop(0)
            self.cpu.clock = event.time

            if event.type==1:
                if self.cpu.busy==False:
                    self.cpu.busy = True
                    event.type = 2
                    event.process.endT = self.cpu.clock + event.process.serviceT
                    event.time = event.process.endT
                    self.eventQueue.append(event)

                elif self.cpu.busy==True:
                    self.readyQueue.append(event.process)
                else:
                    print("ERROR")

                newProcess = self.getProcess()
                newEventArr = self.getEvent(newProcess.arrivalT, 1 , newProcess)
                self.eventQueue.append(newEventArr)

            elif event.type==2:
                self.completedProcesses += 1
                self.processesReadyQ += len(self.readyQueue)
                self.turnaroundTime += (self.cpu.clock - event.process.arrivalT)
                self.totalService += event.process.serviceT
               
                if len(self.readyQueue)==0: #nothing ready to execute
                    self.cpu.busy = False
                else:
                    self.ratioCalc()
                    self.readyQueue.sort(key=lambda x: x.HRRNratio, reverse=True)
                    processDep = self.readyQueue.pop(0)
                    processDep.startT = self.cpu.clock
                    processDep.endT = processDep.startT + processDep.serviceT
                    newEventDep = self.getEvent(processDep.endT, 2 , processDep)
                    self.eventQueue.append(newEventDep) #put the new departure event
            else:
                print("ERROR")

        self.completedProcesses = 0
        self.readyQueue.clear()
        self.eventQueue.clear()

    def RR(self):
        process1 = self.getProcess()
        event1 = self.getEvent(process1.arrivalT, 1 , process1)
        self.eventQueue.append(event1)

        while self.completedProcesses < self.endC:
            self.eventQueue.sort(key=lambda x: x.time)
            event = self.eventQueue.pop(0)
            self.cpu.clock = event.time
            event.process.startT = self.cpu.clock

            if event.type==1:
                if self.cpu.busy==False:
                    self.cpu.busy = True
                
                    if event.process.serviceTimeLeft > self.q:
                        event.type = 3
                        event.time = self.cpu.clock + self.q
                        event.process.serviceTimeLeft -= self.q

                    else:
                        event.type = 2
                        event.process.endT = self.cpu.clock + event.process.serviceTimeLeft
                        event.time = event.process.endT
                    
                    self.cpu.currentProcess = event.process
                    self.eventQueue.append(event)
                else:
                    self.readyQueue.append(event.process)
                newProcess = self.getProcess()
                newEventArr = self.getEvent(newProcess.arrivalT, 1 , newProcess)
                self.eventQueue.append(newEventArr)

            elif event.type==3:
                if len(self.readyQueue)==0:
                    if event.process.serviceTimeLeft > self.q:
                        event.process.serviceTimeLeft -= self.q
                        event.time += self.q
                        self.eventQueue.append(event)
                    else:
                        event.type = 2
                        event.time = event.process.serviceTimeLeft + self.cpu.clock
                        self.eventQueue.append(event)

                else:
                    self.readyQueue.append(self.cpu.currentProcess)
                    self.cpu.currentProcess = None
                    processNext = self.readyQueue.pop()

                    if processNext.serviceTimeLeft < self.q:
                        eventDep = self.getEvent((self.cpu.clock + event.process.serviceTimeLeft), 2 , processNext)
                        eventDep.process.endT = eventDep.time
                        self.cpu.currentProcess = eventDep.process
                        self.cpu.currentProcess.startT = self.cpu.clock
                        self.eventQueue.append(eventDep)

                    else:
                        swapEvent = self.getEvent((self.cpu.clock + self.q), 3 , processNext)
                        swapEvent.process.serviceTimeLeft -= self.q
                        self.cpu.currentProcess = swapEvent.process
                        self.cpu.currentProcess.startT = self.cpu.clock
                        self.eventQueue.append(swapEvent)

            elif event.type==2:
                self.completedProcesses += 1
                self.processesReadyQ += len(self.readyQueue)
                self.turnaroundTime += (self.cpu.clock - event.process.arrivalT)
                self.totalService += event.process.serviceT

                if len(self.readyQueue)==0: # if the readyQueue is empty
                    self.cpu.busy = False
                else:
                    processNext = self.readyQueue.pop(0)
                    if processNext.serviceTimeLeft < self.q:
                        cl= self.cpu.clock + event.process.serviceTimeLeft
                        eventDep = self.getEvent(cl, 2 , processNext)
                        eventDep.process.endT = eventDep.time
                        self.cpu.currentProcess = eventDep.process
                        self.cpu.currentProcess.startT= self.cpu.clock
                        self.eventQueue.append(eventDep)
                    else:
                        cl=self.cpu.clock + self.q
                        eventChange = self.getEvent(cl , 3 , processNext)
                        eventChange.process.serviceTimeLeft -= self.q
                        self.cpu.currentProcess = eventChange.process
                        self.cpu.currentProcess.startT= self.cpu.clock
                        self.eventQueue.append(eventChange)
            else:
                print("ERROR")

        self.completedProcesses = 0
        self.readyQueue.clear()
        self.eventQueue.clear()

    def run(self):
        if self.scheduler==1:
            self.FCFS()
        elif self.scheduler==2:
            self.SRTF()
        elif self.scheduler==3:
            self.HRRN()
        elif self.scheduler==4:
            self.RR()
        else:
            print("Not a valid scheduler type")

    def ratioCalc(self):
        for i in range(len(self.readyQueue)):
            ratio= ((self.cpu.clock - self.readyQueue[i].arrivalT) + self.readyQueue[i].serviceT) / self.readyQueue[i].serviceT
            self.readyQueue[i].HRRNratio = ratio

    def SRTFCalc(self):
        self.readyQueue.sort(key=lambda x: x.serviceTimeLeft)
        self.cpu.currentProcess.serviceTimeLeft = self.cpu.currentProcess.endT - self.cpu.clock
        if len(self.readyQueue) > 0 and self.cpu.currentProcess.serviceTimeLeft > self.readyQueue[0].serviceTimeLeft:
            for i in range(len(self.eventQueue)):
                if self.eventQueue[i].process is self.cpu.currentProcess:
                    self.eventQueue.pop(i)
            self.readyQueue.append(self.cpu.currentProcess)
            newEvent = self.getEvent((self.cpu.clock + self.readyQueue[0].serviceTimeLeft), 2 , self.readyQueue.pop(0))
            self.eventQueue.append(newEvent)
            self.cpu.currentProcess = newEvent.process

    def generateReport(self):

        if self.scheduler==1:
            s="FCFS"
        elif self.scheduler==2:
            s="SRTF"
        elif self.scheduler==3:
            s="HRRN"
        elif self.scheduler==4:
            s="RR"
        else:
            print("Not a valid scheduler type")

        avgTurnaroundTime = round((self.turnaroundTime / self.endC), 2)
        throughput = round((self.endC / self.cpu.clock), 2)
        cpuUtilization = round(self.totalService / self.cpu.clock, 2)
        avgProcessesReadyQ = round(self.processesReadyQ / self.endC, 2)
       
        if self.lambda_val==10:
            with open("sim.txt", "a+") as results:
                results.write("Scheduler\tLambda\tAvgServiceTime\tAvgTurnaroundTime\tThroughput\tCPUUtil\tAvg#ProcReadyQ\tQuantum\n")

        with open("sim.txt", "a+") as results:
            results.write(format(s) + str("\t")+str("\t"))
            results.write(format(str(self.lambda_val)) + str("\t")+str("\t"))
            results.write(format(str(self.avgServiceTime)) + str("\t")+str("\t")+str("\t"))
            results.write(format(str(avgTurnaroundTime)) + str("\t")+str("\t")+str("\t"))
            results.write(format(str(throughput)) + str("\t")+str("\t"))
            results.write(format(str(cpuUtilization)) + str("\t")+str("\t"))
            results.write(format(str(avgProcessesReadyQ)) + str("\t")+str("\t")+str("\t"))
            results.write(format(str(self.q)) + str("\n"))
            results.close()

    def getTime(self):
        time = math.log(1 - float(random.uniform(0, 1))) / (-self.lambda_val)
        return time

    def getProcess(self):
        process = Process()
        initialT= self.getTime()
        process.arrivalT = self.cpu.clock + initialT
        process.serviceT = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.avgServiceTime))
        process.serviceTimeLeft = process.serviceT
        process.endT = process.arrivalT + process.serviceT
        process.startT = 0
        return process

    def getEvent(self, time, type, process):
        event = Event()
        event.time = time
        event.type = type
        event.process = process
        return event


    
if __name__ == "__main__":
    
    scheduler=int(sys.argv[1])
    lmda=int(sys.argv[2])
    avgServiceTime=float(sys.argv[3])

    if scheduler==1:
        print("Running FCFS Scheduler")
        simulator = run_sim(scheduler, lmda, avgServiceTime, 0, 1000)
        simulator.run()
        simulator.generateReport()

    elif scheduler==2:
        print("Running SRTF Scheduler ")
        simulator = run_sim(scheduler, lmda, avgServiceTime, 0, 1000)
        simulator.run()
        simulator.generateReport()

    elif scheduler==3:
        print("Running HRRN Scheduler")
        sim = run_sim(scheduler, lmda, avgServiceTime, 0, 1000)
        sim.run()
        sim.generateReport()

    elif scheduler==4:
        print("Running RR Scheduler")
        sim = run_sim(scheduler, lmda, avgServiceTime, float(sys.argv[4]) , 1000)
        sim.run()
        sim.generateReport()

    else:
        print("Invalid input")