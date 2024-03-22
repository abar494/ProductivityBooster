from Foundation import NSObject, NSRunLoop
import objc
from AppKit import NSWorkspace, NSWorkspaceDidActivateApplicationNotification, NSWindow, NSWorkspaceApplicationKey
import time

class ApplicationMonitor(NSObject):

    def init(self):
        # Register for workspace notifications
        self = objc.super(ApplicationMonitor, self).init()

        notification_center = NSWorkspace.sharedWorkspace().notificationCenter()
        notification_center.addObserver_selector_name_object_(self, 
            self.applicationActivated, NSWorkspaceDidActivateApplicationNotification, None)
        
        self.counter = 0
        self.timeOnMessenger = 0
        self.onMessenger = False

        return self
    
    def applicationActivated(self):
        # Get the activated application

        workspace = NSWorkspace.sharedWorkspace()
        frontmost_application = workspace.frontmostApplication()
        print(str(frontmost_application.localizedName()))
        # print("howdy")
        if str(frontmost_application.localizedName()) == "Messenger":
            self.onMessenger = True
            self.currentTime = time.time()
            self.counter += 1
            # frontmost_application.terminate()
            # print("Messenger detected. Terminating...")

        elif self.onMessenger:
            self.timeOnMessenger += time.time() - self.currentTime
            self.onMessenger = False
            print("Time on Messenger: ", self.timeOnMessenger)
            print("Number of times on Messenger: ", self.counter)
            self.currentTime = 0

def main():
    monitor = ApplicationMonitor.alloc().init()
    # monitor.init()
    
    # # Start the run loop to listen for notifications
    run_loop = NSRunLoop.currentRunLoop()
    run_loop.run()

if __name__ == '__main__':
    main()