import pyglet
from pyglet.graphics import Batch
from pyglet.window import key
from game import Game
from gamewindow_constants import WINDOW_WIDTH, WINDOW_HEIGHT

class GameWindow(pyglet.window.Window):
  def __init__(self):
    super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption='Asteroid Game')
    # Inicializar recursos
    pyglet.resource.path = ['../resources']
    pyglet.resource.reindex()

    self.main_batch: Batch = pyglet.graphics.Batch()
    self.directions: dict[int, bool] = { key.A : False, key.D : False, key.W: False, key.S: False, key.SPACE: False }
    self.game: Game = Game(keys=self.directions, batch=self.main_batch)


  def on_key_press(self, symbol: int, modifiers: int):
    match(symbol):
      case key.A | key.D | key.W | key.S | key.SPACE:
        self.directions[symbol] = True
      case key.R:
        self.game.ENDED = True
        self.game.clear()
        self.game = Game(keys=self.directions, batch=self.main_batch)
      case key.ESCAPE:
        self.game.ENDED = True
        self.game.clear()
        self.clear()
        self.close()
  
  def on_key_release(self, symbol: int, modifiers: int):
    match(symbol):
      case key.A | key.D | key.W | key.S | key.SPACE:
        self.directions[symbol] = False

  def on_draw(self) -> None:
    self.clear()
    self.main_batch.draw()
  
  def update(self, dt: float) -> None:
    if not self.game.ENDED:
      self.game.update(dt)