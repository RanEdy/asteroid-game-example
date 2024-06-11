import pyglet
from pyglet.window import Window

game_window: Window = pyglet.window.Window(800, 600)

if __name__ == '__main__':
  pyglet.app.run()