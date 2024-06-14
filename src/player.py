from pyglet.graphics import Batch
from pyglet.math import Vec2
from pyglet.window import key
from entity import Entity, EntityType

class Player(Entity):
  def __init__(self, batch: Batch) -> None:
    super().__init__('player.png', batch)
    self.keys: dict[int, bool]
    self.lives = 3
    self.speed= Vec2(250, 180)
    self.fire_rate: int = 60
    self.next_fire_time: int = 0
    self.type: int = EntityType.PLAYER
    self.bullet_list = []
    self.limit_x_min: int
    self.limit_x_max: int
    self.limit_y_min: int
    self.limit_y_max: int

  def update(self, dt: float, ticks: int) -> None:
    self._check_immunity(ticks)
    self.handle_keys(dt, ticks)
    self.check_bounds()
    self._check_collision(ticks)
    #print(f'Bullets: {len(self.bullet_list)}')

  def handle_keys(self, dt: float, ticks: int) -> None:
    if self.keys[key.A]:
      self.move(-self.speed.x * dt, 0)
      self.set_rotation(-10)
    elif not self.keys[key.D]:
      self.set_rotation(0)

    if self.keys[key.D]:
      self.move(self.speed.x * dt, 0)
      self.set_rotation(10)
    elif not self.keys[key.A]:
      self.set_rotation(0)

    if self.keys[key.W]:
      self.move(0, self.speed.y * dt)

    if self.keys[key.S]:
      self.move(0, -self.speed.y * dt)
    
    if self.keys[key.SPACE] and ticks > self.next_fire_time:
      self.shoot()
      self.next_fire_time = ticks + self.fire_rate

  def shoot(self) -> None:
    bullet: Entity = Entity('bullet.png', self.batch)
    bullet.set_type(EntityType.FRIENDLY)
    bullet.set_pos(Vec2(self.sprite.x, self.sprite.y+20))
    bullet.set_size(15, 15)
    bullet.add_lives(1)
    bullet.set_speed(Vec2(0, 350))
    bullet.set_enemy_list(self.enemy_list)
    self.bullet_list.append(bullet)
    #print('Bala creada')

  def set_keys(self, keys: dict[int, bool]) -> None:
    self.keys = keys

  def set_limits(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
    self.limit_x_max = max_x - self.get_width()//2
    self.limit_x_min = min_x + self.get_width()//2
    self.limit_y_max = max_y - self.get_height()//2
    self.limit_y_min = min_y + self.get_height()//2

  def check_bounds(self) -> None:
    if self.get_x() >= self.limit_x_max:
      self.set_x(self.limit_x_max)
    if self.get_x() <= self.limit_x_min:
      self.set_x(self.limit_x_min)
    if self.get_y() >= self.limit_y_max:
      self.set_y(self.limit_y_max)
    if self.get_y() <= self.limit_y_min:
      self.set_y(self.limit_y_min)

  def _on_collision(self, entity: Entity, ticks: int) -> None:
    if entity.type == EntityType.HOSTILE:
      self.add_lives(-1)
      self.immunity_time = ticks + 300
  
  def _check_immunity(self, ticks) -> None:
    self.immunity = self.immunity_time > ticks

    if self.immunity:
      self.sprite.opacity = 50
    else:
      self.sprite.opacity = 255
  

    