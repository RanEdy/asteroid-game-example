from pyglet.graphics import Batch
from pyglet.math import Vec2
from pyglet.window import key
from entity import Entity

class Player:
  def __init__(self, batch: Batch) -> None:
    self.player_entity: Entity = Entity('player.png', batch)
    self.keys: dict[int, bool]

    self.player_entity.add_lives(3)
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

  def check_shoot(self) -> None:
    if self.keys[key.SPACE]:
      self.shoot()

  def shoot(self) -> Entity:
    pass
  
  def set_keys(self, keys: dict[int, bool]) -> None:
    self.keys = keys

  def set_pos(self, pos: Vec2) -> None:
    self.player_entity.set_pos(pos)

  def set_size(self, width: int, height: int) -> None:
    self.player_entity.set_size(width, height)

  def set_limits(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
    self.limit_x_max = max_x - self.player_entity.get_width()//2
    self.limit_x_min = min_x + self.player_entity.get_width()//2
    self.limit_y_max = max_y - self.player_entity.get_height()//2
    self.limit_y_min = min_y + self.player_entity.get_height()//2

  def get_y(self) -> int:
    return self.player_entity.get_y()
  
  def get_x(self) -> int:
    return self.player_entity.get_x()

  def check_bounds(self) -> None:
    if self.player_entity.get_x() >= self.limit_x_max:
      self.player_entity.set_x(self.limit_x_max)
    if self.player_entity.get_x() <= self.limit_x_min:
      self.player_entity.set_x(self.limit_x_min)
    if self.player_entity.get_y() >= self.limit_y_max:
      self.player_entity.set_y(self.limit_y_max)
    if self.player_entity.get_y() <= self.limit_y_min:
      self.player_entity.set_y(self.limit_y_min)

  def update(self, dt: float) -> None:
    self.handle_move(dt)
    self.check_bounds()

    