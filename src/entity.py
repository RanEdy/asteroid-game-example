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

    self.life: int = 0

    self.speed : Vec2 = Vec2(0, 0)

    self.type: int = EntityType.PASSIVE

  def set_pos(self, pos: Vec2) -> None:
    self.sprite.x = pos.x
    self.sprite.y = pos.y

  def set_speed(self, speed: Vec2) -> None:
    self.speed = speed
  
  def set_type(self, type: int) -> None:
    self.type = type

  def set_size(self, width: int, height: int) -> None:
    self._scale_sprite(self.sprite, width, height)

  def add_life(self, amount: int) -> None:
    self.life += amount

  def move(self, dx: int, dy: int) -> None:
    self.sprite.x += dx
    self.sprite.y += dy

  def _auto_move(self) -> None:
    self.sprite.x += self.speed.x
    self.sprite.y += self.speed.y

  def _center_image(self, image: Texture) -> None:
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

  def _scale_sprite(self, sprite: Sprite, width: int, height: int) -> None:
    h_factor: float = height / sprite.height
    w_factor: float = width / sprite.width
    sprite.scale_y = h_factor
    sprite.scale_x = w_factor

  def update(self, dt: float) -> None:
    pass