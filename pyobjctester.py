# from Foundation import NSWorkspace

# def get_frontmost_application_name():
#     workspace = NSWorkspace.sharedWorkspace()
#     frontmost_application = workspace.frontmostApplication()
#     return frontmost_application.localizedName()

# if __name__ == "__main__":
#     # print(get_frontmost_application_name())

import Foundation
# import AppKit

def modnames(module):
    object_methods = [method_name for method_name in dir(module)
                      if not callable(getattr(module, method_name)) and not method_name.startswith("__") and "nsapplication" in method_name.lower() and method_name.endswith("application")]
    print(object_methods)


from AppKit import NSWorkspace
# import time

def starter():
    # while True:
    workspace = NSWorkspace.sharedWorkspace()

    apps = workspace.runningApplications()
    for app in apps:
        # print(app.localizedName())
        if app.localizedName() == "Messenger":
            app.terminate()
            print("terminated")
            # print("Found Chrome")
            # object_methods = [method_name for method_name in dir(app)
            #                 if callable(getattr(app, method_name)) and not method_name.startswith("__") and "quit" in method_name.lower()]
            # print(object_methods)
            break

    
    # print()
    # workspace = NSWorkspace.sharedWorkspace()
    # frontmost_application = workspace.frontmostApplication()
    # return str(frontmost_application.localizedName())

if __name__ == "__main__":
    # time.sleep(2)
    # print(get_frontmost_application_name())
    # workspace = NSWorkspace.sharedWorkspace()
    # modnames(workspace)
    starter()
    # modnames(AppKit)