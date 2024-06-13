import pyglet, random
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.math import Vec2
from entity import Entity
from player import Player
from gamewindow_constants import WINDOW_WIDTH, WINDOW_HEIGHT

class Game:
  def __init__(self, keys: dict[int, bool], batch: Batch) -> None:

    self.entity_list = []
    self.asteroids_time_interval: int = random.randint(500, 800)
    self.ticks: int = 0
    self.keys: dict[int, bool] = keys

    self.batch: Batch = batch
    self.score_label: Label = pyglet.text.Label(text="Score: 0", x=10, y=460, batch=batch)
    self.player: Player

    self.init_player()

  def init_player(self) -> None:
    self.player: Player = Player(self.batch)
    self.player.set_pos(Vec2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    self.player.set_size(80, 80)
    self.player.set_keys(self.keys)
    self.player.set_limits(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    self.entity_list.append(self.player)

  def spawn_asteroids(self) -> None:
    if self.ticks == self.asteroids_time_interval:
      asteroids_count: int = random.randint(3, 6)
      for i in range(asteroids_count):
        asteroid: Entity = Entity('asteroid.png', self.batch)
        a_size: int = random.randint(40, 150)
        asteroid.set_size(a_size + random.randint(-10, 10), a_size + random.randint(-10, 10))
        asteroid.set_pos(Vec2(random.randint(-200, WINDOW_WIDTH+200), random.randint(WINDOW_HEIGHT+100, WINDOW_HEIGHT+200)))
        asteroid.set_rotation(random.randint(-360, 360))
        asteroid.set_speed(Vec2(random.randint(-100, 100), random.randint(-300, -100)))
        self.entity_list.append(asteroid)
        #print('Asteroide creado: ', asteroid.get_x(), asteroid.get_y())
      self.next_asteroids_time_interval()
  
  def next_asteroids_time_interval(self) -> None:
    self.asteroids_time_interval = self.ticks + random.randint(300, 800)

  def update_entities(self, dt: float) -> None:
    for entity in self.entity_list:
      entity.update(dt) 
      self.remove_entity_out_of_bounds(entity)

  def remove_entity_out_of_bounds(self, entity: Entity) -> None:
    if entity.get_y() < -100:
      entity.delete()
      self.entity_list.remove(entity)
      #print('Entidad removida')

  def update(self, dt: float) -> None:
    self.update_entities(dt)
    self.spawn_asteroids()
    self.ticks += 1
    print(len(self.entity_list))