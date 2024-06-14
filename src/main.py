import pyglet, gamewindow
# TODO
#
#
def main() -> None:
  FPS: int = 144
  game = gamewindow.GameWindow()
  pyglet.clock.schedule(game.update)
  pyglet.app.run(1/(FPS*2))

if __name__ == '__main__':
  main()