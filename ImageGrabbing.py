from PIL import ImageGrab, Image
import subprocess

def get_top_menu_bar_image(topBarHeight):
    # Get screen resolution
    resolution = subprocess.check_output("system_profiler SPDisplaysDataType | grep Resolution", shell=True).decode("utf-8")
    print(resolution)
    strippedRes = resolution.strip().split(" ")
    width, height = int(strippedRes[1]), int(strippedRes[-2])
    # Capture the screen
    screen = ImageGrab.grab(bbox=(0, 0, int(width/4.3), topBarHeight))  # Adjust 22 based on your menu bar's height

    return screen


topImage = get_top_menu_bar_image(32)
fullImage = ImageGrab.grab()

topImage.save("topImage.png")
fullImage.save("fullImage.png")

# # object_methods = [method_name for method_name in dir(imagearray)
# #                   if callable(getattr(imagearray, method_name)) and not method_name.startswith("__")]


# # print(object_methods)


# # print(imagearray.size)
# # # print(type(imagearray))

# # for y in range(0, 100, 10):
# #     for x in range(0, 100, 10):
# #         color = image.getpixel((x, y))
# #         print(color)
# # b = time.time()
# # print(b-a)
