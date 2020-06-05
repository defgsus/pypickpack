
def log(*args):
    from .console_renderer import ConsoleRenderer

    if ConsoleRenderer._instance:
        ConsoleRenderer._instance.print(*args)
    else:
        print(*args)
