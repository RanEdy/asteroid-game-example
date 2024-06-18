import pyglet
from pyglet.image import Texture
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.graphics import Batch
from pyglet.math import Vec2
from pyglet.shapes import Box
from enum import Enum


DEBUG: bool = False
class EntityType(Enum):
  PLAYER: int = 0
  FRIENDLY: int = 1
  HOSTILE: int = 2

class Entity:
  def __init__(self, img_path: str, batch: Batch) -> None:
    self.batch: Batch = batch
    self.entity_img: Texture = pyglet.resource.image(img_path)
    self._center_image(self.entity_img)
    self.sprite: Sprite = pyglet.sprite.Sprite(img=self.entity_img, x=-5000, y=0, batch=batch)
    self.lives: int = 1
    self.lives_label: Label
    self.speed: Vec2 = Vec2(0, 0)
    self.type: int = EntityType.HOSTILE
    self.alive: bool = True
    self.immunity: bool = False
    self.immunity_time: int = 0
    self.auto_rotation_angle: float = 0
    self.enemy_list: list['Entity'] = []
    self.points: int = 1
    # --------- HitBox -----------
    self.hitbox_w_factor: float = 0.7
    self.hitbox_h_factor: float = 0.7
    self.hitbox_width: float = self.sprite.width * self.hitbox_w_factor
    self.hitbox_height: float = self.sprite.height * self.hitbox_h_factor
    self.hitbox_right_corner: Vec2 = Vec2(self.sprite.x + self.hitbox_width/2, self.sprite.y - self.hitbox_height/2)
    self.hitbox_left_corner: Vec2 = Vec2(self.sprite.x - self.hitbox_width/2, self.sprite.y + self.hitbox_height/2)
    self.hitbox_shape: Box = Box(
      x=self.hitbox_left_corner.x, y= self.hitbox_left_corner.y - self.hitbox_height,
      width=self.hitbox_width, height=self.hitbox_height,
      thickness=2.0, color=(255, 0, 0, 0), batch=batch
      )
    
    # ------ DEBUG ----------
    if DEBUG:
      self.lives_label = pyglet.text.Label(text=str(self.lives), x=self.sprite.x, y=self.sprite.y, color=(255, 0, 0, 255), batch=batch)
      self.hitbox_shape.opacity = 255

  def update(self, dt: float, ticks: int) -> None:
    self._check_immunity(ticks)
    self._auto_move(dt)
    self._auto_rotate(dt)
    self._check_collision(ticks)

    if DEBUG:
      self.lives_label.text = str(self.lives)

  def delete(self) -> None:
    self.hitbox_shape.delete()
    self.sprite.delete()

  def set_enemy_list(self, list: list['Entity']) -> None:
    self.enemy_list = list

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
    self._scale_sprite(width, height)
  
  def get_width(self) -> int:
    return self.sprite.width

  def get_height(self) -> int:
    return self.sprite.height

  def add_lives(self, amount: int) -> None:
    self.lives += amount
    self.alive = self.lives > 0

  def move(self, dx: int, dy: int) -> None:
    self.sprite.x += dx
    self.sprite.y += dy
    self._update_hitbox()

    if DEBUG:
      self.lives_label.x = self.sprite.x
      self.lives_label.y = self.sprite.y

  def _intersects(self, entity: 'Entity') -> bool:
    on_side = self.hitbox_left_corner.x > entity.hitbox_right_corner.x or entity.hitbox_left_corner.x > self.hitbox_right_corner.x
    on_top_or_below = self.hitbox_right_corner.y > entity.hitbox_left_corner.y or entity.hitbox_right_corner.y > self.hitbox_left_corner.y
    return not(on_side or on_top_or_below)
  
  def _collision_with(self, entity: 'Entity') -> bool:
    return self._intersects(entity)

  def _on_collision(self, entity: 'Entity', ticks: int) -> None:
    if self.type != entity.type:
      self.add_lives(-1)
      self.immunity_time = ticks + 10

  def _check_collision(self, ticks: int) -> None:
    if not self.immunity:
      for entity in self.enemy_list:
        if self._collision_with(entity):
          self._on_collision(entity, ticks)

  def _check_immunity(self, ticks) -> None:
    self.immunity = self.immunity_time > ticks

  def _auto_move(self, dt: float) -> None:
    self.move(self.speed.x * dt, self.speed.y * dt)

  def _auto_rotate(self, dt: float) -> None:
    self.auto_rotation_angle += (self.speed.y * dt * 0.5) % 360
    self.set_rotation(self.auto_rotation_angle)

  def _center_image(self, image: Texture) -> None:
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

  def _scale_sprite(self, width: int, height: int) -> None:
    h_factor: float = height / self.sprite.height
    w_factor: float = width / self.sprite.width
    self.sprite.scale_y = h_factor
    self.sprite.scale_x = w_factor
    self._update_hitbox()
    self.hitbox_shape.width = self.hitbox_width
    self.hitbox_shape.height = self.hitbox_height

  def _update_hitbox(self) -> None:
    self.hitbox_width = self.sprite.width * self.hitbox_w_factor
    self.hitbox_height = self.sprite.height * self.hitbox_h_factor
    self.hitbox_right_corner = Vec2(self.sprite.x + self.hitbox_width/2, self.sprite.y - self.hitbox_height/2)
    self.hitbox_left_corner = Vec2(self.sprite.x - self.hitbox_width/2, self.sprite.y + self.hitbox_height/2)
    self.hitbox_shape.position = (self.hitbox_left_corner.x, self.hitbox_left_corner.y - self.hitbox_height)
