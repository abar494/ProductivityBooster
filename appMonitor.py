from Foundation import NSObject, NSRunLoop, NSDate
import objc
from AppKit import NSWorkspace, NSWorkspaceDidActivateApplicationNotification
import threading
import asyncio
import time
from playsound import playsound

class ApplicationMonitor(NSObject):
    def init(self):
        self = objc.super(ApplicationMonitor, self).init()

        self.counter = 0
        self.timeOnTarget = 0
        self.applicationToMonitor = None
        self.applicationName = ""
        self.onTarget = False
        self.run_loop_running = True

        return self
    
class ApplicationMonitorWithParams(ApplicationMonitor):
    def initWithOtherVariable_(self, params):
        self = objc.super(ApplicationMonitorWithParams, self).init()

        notification_center = NSWorkspace.sharedWorkspace().notificationCenter()
        notification_center.addObserver_selector_name_object_(self, 
            self.applicationActivated, NSWorkspaceDidActivateApplicationNotification, None)
        
        self.targetApplication = params["targetApplication"]
        self.period = params["period"]
        self.terminateTime = params["terminateTime"]
        self.reminderTime = params["reminderTime"]
   
        self.start_asyncio_task()

        return self
    

    def start_asyncio_task(self):
        asyncio_thread = threading.Thread(target=self.run_asyncio_loop)
        asyncio_thread.start()

    def run_asyncio_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.check_time_spent_on_app())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
    
    async def check_time_spent_on_app(self):
        oldTimeOnTarget = -1
        reminderSet = False
        while True:
            await asyncio.sleep(self.period)

            if self.applicationName == self.targetApplication:
                self.timeOnTarget += (time.time() - self.currentTime)
                self.currentTime = time.time()
 
            if oldTimeOnTarget != self.timeOnTarget and round(self.terminateTime - self.timeOnTarget, 2) > 0:
                print(round(self.terminateTime - self.timeOnTarget, 2))

            if round(self.terminateTime - self.timeOnTarget, 2) < self.reminderTime and not reminderSet:
                reminderSet = True
                playsound('readyToWork.mp3', False)

            if self.timeOnTarget > self.terminateTime:
                print(self.targetApplication + " detected. Terminating...")
                self.applicationToMonitor.terminate()
                break

            oldTimeOnTarget = self.timeOnTarget
            
        self.run_loop_running = False

    def applicationActivated(self):
        workspace = NSWorkspace.sharedWorkspace()
        frontmost_application = workspace.frontmostApplication()

        self.applicationName = str(frontmost_application.localizedName().lower())
        if self.applicationName == self.targetApplication:
            
            if self.applicationToMonitor is None:
                self.applicationToMonitor = frontmost_application
        
            print("on " + self.targetApplication)
            self.onTarget = True
            self.currentTime = time.time()
            self.counter += 1

        elif self.onTarget:
            self.timeOnTarget += time.time() - self.currentTime
            self.onTarget = False
            # print("Time on " + self.targetApplication + ": " + str(self.timeOnTarget))
            # print("Number of times on " + self.targetApplication + ": " + str(self.counter))

def convertTime(time):
    if ":" in time:
        time = time.split(":")
        time = [float(i) for i in time]
        return time[0] * 3600 + time[1] * 60 + time[2]
    return float(time)




def main():

    params = {}
    params["targetApplication"] = str(input("What application would you like to set a timer for? "))
    params["terminateTime"] = convertTime(input("How long would you like to allow the application to run? "))
    params["reminderTime"] = convertTime((input("How long before would you like to be reminded? ")))
    params["period"] = float(input("How often would you like to check the time spent on the application? "))


    print("Starting Application Monitor")
    print("\nRun Loop Beginning\n")

    print("-----------------------------------------\n")

    monitor = ApplicationMonitorWithParams.alloc().initWithOtherVariable_(params)

    run_loop = NSRunLoop.currentRunLoop()

    while monitor.run_loop_running:
        run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))
        
    print("Times Up!")
 
if __name__ == '__main__':
    main()