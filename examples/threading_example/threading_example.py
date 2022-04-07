from threading import Timer


def hello_world():
    print("Hello World")


timer = Timer(5, hello_world)
timer.start()
