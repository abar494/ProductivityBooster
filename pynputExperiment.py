from pynput.mouse import Button, Controller, Listener

counter = 0


mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

mouse.move(5, -5)

# Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)

# Double click; this is different from pressing and releasing
# twice on macOS
# mouse.click(Button.left, 2)

# Scroll two steps down
mouse.scroll(0, 2)


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    #add counter for how many times been clicked
    global counter
    global mouse
    if pressed:
        counter += 1
        print('Mouse clicked at ({0}, {1}) with {2}'.format(
            x, y, button))
        print('Counter: {0}'.format(counter))

        mouse.move(5, -5)
        mouse.scroll(0, 2)


def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))



# Collect events until released
with Listener(
        # on_move=on_move,
        on_click=on_click
        # on_scroll=on_scroll
        ) as listener:
    listener.join()

