from Foundation import NSObject, NSRunLoop
import objc
from AppKit import NSWorkspace, NSWorkspaceDidActivateApplicationNotification
import threading
import asyncio

class ApplicationMonitor(NSObject):

    def init(self):
        # Register for workspace notifications
        self = objc.super(ApplicationMonitor, self).init()

        notification_center = NSWorkspace.sharedWorkspace().notificationCenter()
        notification_center.addObserver_selector_name_object_(self, 
            self.applicationActivated, NSWorkspaceDidActivateApplicationNotification, None)
        
        self.start_asyncio_task()
        return self
    

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
            await asyncio.sleep(5)
            print("checking time")


    def applicationActivated(self):
        workspace = NSWorkspace.sharedWorkspace()
        frontmost_application = workspace.frontmostApplication()

        print("frontmost application: ", frontmost_application.localizedName())

def main():
    monitor = ApplicationMonitor.alloc().init()
    run_loop = NSRunLoop.currentRunLoop()
    run_loop.run()

if __name__ == '__main__':
    main()