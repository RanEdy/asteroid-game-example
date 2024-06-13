import pyglet, gamewindow

def main() -> None:
  game = gamewindow.GameWindow()
  pyglet.clock.schedule(game.update)
  pyglet.app.run(1/144)

if __name__ == '__main__':
  main()