from Foundation import NSObject, NSRunLoop, NSDate
import objc
from AppKit import NSWorkspace, NSWorkspaceDidActivateApplicationNotification
import threading
import asyncio
import time

class ApplicationMonitor(NSObject):

    def init(self):
        # Register for workspace notifications
        self = objc.super(ApplicationMonitor, self).init()

        notification_center = NSWorkspace.sharedWorkspace().notificationCenter()
        notification_center.addObserver_selector_name_object_(self, 
            self.applicationActivated, NSWorkspaceDidActivateApplicationNotification, None)
        
        self.terminate_time = 20  # Terminate Messenger after 30 minutes (1800 seconds)
        self.period = 5
        self.counter = 0
        self.timeOnTarget = 0
        self.onMessenger = False
        self.targetApplication = "mgba"
        self.applicationToMonitor = None
        self.applicationName = ""
        self.onTarget = False
        self.run_loop_running = True



        self.start_asyncio_task()
        return self
    

    def stop_run_loop(self):
        self.run_loop.stop()

    def start_asyncio_task(self):
        asyncio_thread = threading.Thread(target=self.run_asyncio_loop)
        asyncio_thread.start()

    def run_asyncio_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.check_time_spent_on_messenger())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
    
    async def check_time_spent_on_messenger(self):
        while True:
            await asyncio.sleep(self.period)

            # print("checking time")
            isOn = (self.applicationName == self.targetApplication)

    
            if isOn:
                # print("full cycle no clicks, add " + str(self.period) + " seconds")
                # print(self.currentTime)
                # print(time.time())
                # self.currentTime += self.period
                # self.timeOnTarget += self.period
                # print(self.timeOnTarget)
            # elif not wasOn and isOn:
                self.timeOnTarget += (time.time() - self.currentTime)
                self.currentTime = time.time()
                print(self.timeOnTarget)
            else:
                print(self.timeOnTarget)
    
            # if wasOn and isOn and (self.counter != prevCounter):
            #     print("clicked off then on, first part calculated from clickoff, add " + str(self.period*1/4) + " seconds")
            # if not wasOn and not isOn and (self.counter == prevCounter):
            #     print("stayed off, no time added")
            # if not wasOn and not isOn and (self.counter != prevCounter):
            #     print("clicked on then off, time already calculated from clickoff")
            # if not wasOn and isOn:
            #     print("clicked on, add " + str(self.period/2) + " seconds")
            # if wasOn and not isOn:
            #     print("clicked off, time already calculated from clickoff")

            # self.currentTime += self.period
            # self.timeOnTarget += self.period

            if self.timeOnTarget > self.terminate_time:
                print("mgba detected. Terminating...")
                self.applicationToMonitor.terminate()
                #terminate mgba
                break
                # self.applicationToMonitor.terminate()
                # asyncio.create_task(self.reset_time_on_messenger)
            
        self.run_loop_running = False


        print(self.run_loop_running)
            #was I off mgba?
            #start of loop
            #time gap of 5 seconds, maximum error

            #if not on mgba, don't add time
            #if on mgba, add time

            #was I on mgba?

            # print(self.counter)
            # print(self.timeOnTarget)

            # print(self.applicationName)
            # print(self.targetApplication)
            # if self.applicationName == self.targetApplication and :
            #     self.timeOnTarget += time.time() - self.currentTime
            # self.onTarget = False
            # print("Time on " + self.targetApplication + ": " + str(self.timeOnTarget))
            # print("Number of times on " + self.targetApplication + ": " + str(self.counter))
            # self.currentTime = 0
            # and self.timeOnTarget > self.terminate_time:
            #     print("mgba detected. Terminating...")
            #     # self.applicationToMonitor.terminate()
            #     # asyncio.create_task(self.reset_time_on_messenger)
            # wasOn = isOn

    # async def reset_time_on_messenger(self):
    #     await asyncio.sleep(10)
    #     print("Resetting time on Messenger...")
    #     self.time_on_messenger = 0

    # Method to check if the run loop should keep running
    # def checkRunLoopRunning_(self, timer):
    #     if not self.run_loop_running:
    #         timer.invalidate()     


    def applicationActivated(self):
        workspace = NSWorkspace.sharedWorkspace()
        frontmost_application = workspace.frontmostApplication()

        # if frontmost_application == self.applicationActivated:
        #     workspace = NSWorkspace.sharedWorkspace()
        #     frontmost_application = workspace.frontmostApplication()

        # print("frontmost application: ", frontmost_application.localizedName())

        self.applicationName = str(frontmost_application.localizedName().lower())
        if self.applicationName == self.targetApplication:
            
            if self.applicationToMonitor is None:
                self.applicationToMonitor = frontmost_application
        #     self.applicationToMonitor = frontmost_application
        
            print("on mgba")
            self.onTarget = True
            self.currentTime = time.time()
            self.counter += 1

        elif self.onTarget:
            self.timeOnTarget += time.time() - self.currentTime
            self.onTarget = False
            # print("Time on " + self.targetApplication + ": " + str(self.timeOnTarget))
            # print("Number of times on " + self.targetApplication + ": " + str(self.counter))
            # self.currentTime = 0

        #     # if self.timeOnTarget > 5:
        #     #     print("Messenger detected. Terminating...")
        #     #     frontmost_application.terminate()

        # elif self.onMessenger:
        #     self.timeOnTarget += time.time() - self.currentTime
        #     self.onMessenger = False
        #     print("Time on Messenger: ", self.timeOnTarget)
        #     print("Number of times on Messenger: ", self.counter)
        #     self.currentTime = 0

def main():
    monitor = ApplicationMonitor.alloc().init()
    run_loop = NSRunLoop.currentRunLoop()

    print("Run Loop Beginning")

    # timer = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
    #     0.1, monitor, "checkRunLoopRunning:", None, True)
    
    # run_loop.addTimer_forMode_(timer, NSDefaultRunLoopMode)


    while monitor.run_loop_running:
    # Run the run loop with a timeout of 0.1 seconds
        run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))
        if not monitor.run_loop_running:
            print("Loop Exited")
        
    print("Task Finished Successfully!")
 

# When you want to stop the run loop:
# monitor.stop_run_loop()
if __name__ == '__main__':
    main()