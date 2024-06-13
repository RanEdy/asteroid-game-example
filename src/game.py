import pyglet
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.math import Vec2
from entity import Entity
from player import Player
from gamewindow_constants import WINDOW_WIDTH, WINDOW_HEIGHT

class Game:
  def __init__(self, keys: dict[int, bool], batch: Batch) -> None:
    self.batch: Batch = batch
    self.score_label: Label = pyglet.text.Label(text="Score: 0", x=10, y=460, batch=batch)
    self.keys: dict[int, bool] = keys
    self.player: Player
    
    self.init_player()

  def init_player(self) -> None:
    self.player: Player = Player(self.batch)
    self.player.set_pos(Vec2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    self.player.set_size(80, 80)
    self.player.set_keys(self.keys)
    self.player.set_limits(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
  def update(self, dt: float) -> None:
    self.player.update(dt)