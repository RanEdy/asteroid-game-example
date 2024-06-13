from pyglet.graphics import Batch
from pyglet.math import Vec2
from pyglet.window import key
from entity import Entity

class Player:
  def __init__(self, batch: Batch) -> None:
    self.player_entity: Entity = Entity('player.png', batch)
    self.keys: dict[int, bool]

    self.player_entity.add_life(3)
    self.player_entity.set_speed(Vec2(300, 200))

    self.limit_x_min: int
    self.limit_x_max: int
    self.limit_y_min: int
    self.limit_y_max: int

  def handle_move(self, dt: float) -> None:
    if self.keys[key.A]:
      self.player_entity.move(-self.player_entity.speed.x * dt, 0)
    if self.keys[key.D]:
      self.player_entity.move(self.player_entity.speed.x * dt, 0)
    if self.keys[key.W]:
      self.player_entity.move(0, self.player_entity.speed.y * dt)
    if self.keys[key.S]:
      self.player_entity.move(0, -self.player_entity.speed.y * dt)

  def set_keys(self, keys: dict[int, bool]) -> None:
    self.keys = keys

  def set_pos(self, pos: Vec2) -> None:
    self.player_entity.set_pos(pos)

  def set_size(self, width: int, height: int) -> None:
    self.player_entity.set_size(width, height)

  def set_limits(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
    self.limit_x_max = max_x
    self.limit_x_min = min_x
    self.limit_y_max = max_y
    self.limit_y_min = min_y

  def update(self, dt: float) -> None:
    self.handle_move(dt)

    