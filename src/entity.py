import pyglet
from pyglet.image import Texture
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.math import Vec2
from enum import Enum

class EntityType(Enum):
  PASSIVE: int = 0
  HOSTILE: int = 1

class Entity:
  def __init__(self, img_path: str, batch: Batch) -> None:

    self.entity_img: Texture = pyglet.resource.image(img_path)
    self._center_image(self.entity_img)

    self.sprite: Sprite = pyglet.sprite.Sprite(img=self.entity_img, x=0, y=0, batch=batch)

    self.lives: int = 0

    self.speed : Vec2 = Vec2(0, 0)

    self.type: int = EntityType.PASSIVE

    self.alive: bool = True

  def set_rotation(self, angle_deg: int) -> None:
    self.sprite.rotation = angle_deg

  def set_pos(self, pos: Vec2) -> None:
    self.sprite.x = pos.x
    self.sprite.y = pos.y

  def set_x(self, x: int) -> None:
    self.sprite.x = x

  def get_x(self) -> int:
    return self.sprite.x
  
  def set_y(self, y: int) -> None:
    self.sprite.y = y

  def get_y(self) -> int:
    return self.sprite.y

  def set_speed(self, speed: Vec2) -> None:
    self.speed = speed
  
  def set_type(self, type: int) -> None:
    self.type = type

  def set_size(self, width: int, height: int) -> None:
    self._scale_sprite(self.sprite, width, height)
  
  def get_width(self) -> int:
    return self.sprite.width

  def get_height(self) -> int:
    return self.sprite.height

  def add_lives(self, amount: int) -> None:
    self.lives += amount

  def move(self, dx: int, dy: int) -> None:
    self.sprite.x += dx
    self.sprite.y += dy

  def _auto_move(self, dt: float) -> None:
    self.sprite.x += self.speed.x * dt
    self.sprite.y += self.speed.y * dt

  def _center_image(self, image: Texture) -> None:
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

  def _scale_sprite(self, sprite: Sprite, width: int, height: int) -> None:
    h_factor: float = height / sprite.height
    w_factor: float = width / sprite.width
    sprite.scale_y = h_factor
    sprite.scale_x = w_factor

  def update(self, dt: float) -> None:
    self._auto_move(dt)

  def delete(self) -> None:
    self.sprite.delete