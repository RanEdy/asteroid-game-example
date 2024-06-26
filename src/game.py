import pyglet, random
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.math import Vec2
from entity import Entity
from player import Player
from gamewindow_constants import WINDOW_WIDTH, WINDOW_HEIGHT

class Game:
  def __init__(self, keys: dict[int, bool], batch: Batch) -> None:

    self.asteroid_list: list[Entity] = []
    self.asteroids_time_interval: int = random.randint(500, 800)
    self.ticks: int = 0
    self.keys: dict[int, bool] = keys
    self.batch: Batch = batch
    self.score: int = 0
    self.score_label: Label = pyglet.text.Label(text='Score: ' + str(self.score), font_size=18, x=10, y=560, batch=batch)
    self.lives_label: Label = pyglet.text.Label(text='Lives: 3', font_size=18, x=10, y= 500, batch=batch)
    self.player: Player
    self.ENDED: bool = False

    self.init_player()

  def update(self, dt: float) -> None:
    if not self.player.alive:
      self.end()
      return
    
    self.update_entities(dt)
    self.spawn_asteroids()
    self.update_gui()
    self.ticks += 1


  def init_player(self) -> None:
    self.player: Player = Player(self.batch)
    self.player.set_pos(Vec2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    self.player.set_size(60, 60)
    self.player.set_keys(self.keys)
    self.player.set_limits(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    self.player.set_enemy_list(self.asteroid_list)

  def spawn_asteroids(self) -> None:
    if self.ticks == self.asteroids_time_interval:
      asteroids_count: int = random.randint(3, 8)
      for i in range(asteroids_count):
        asteroid: Entity = Entity('asteroid.png', self.batch)
        asteroid.set_enemy_list(self.player.bullet_list)
        a_size: int = random.randint(50, 150)
        asteroid.add_lives(a_size//30)
        asteroid.points = a_size//20
        asteroid.set_size(a_size + random.randint(-10, 10), a_size + random.randint(-10, 10))
        asteroid.set_pos(Vec2(random.randint(-200, WINDOW_WIDTH+200), random.randint(WINDOW_HEIGHT+100, WINDOW_HEIGHT+200)))
        asteroid.set_rotation(random.randint(-360, 360))
        asteroid.set_speed(Vec2(random.randint(-150, 150), random.randint(-400, -150)))
        self.asteroid_list.append(asteroid)
        #print('Asteroide creado: ', asteroid.get_x(), asteroid.get_y())
      self.asteroids_time_interval = self.ticks + random.randint(50, 400)
  
  def update_entities(self, dt: float) -> None:
    for asteroid in self.asteroid_list + self.player.bullet_list + [self.player]:
      asteroid.update(dt, self.ticks)
      self.check_deletion(asteroid)

  def update_gui(self) -> None:
    self.score_label.text = 'Score: ' + str(self.score)
    self.lives_label.text = 'Lives: ' + str(self.player.lives)
        

  def check_deletion(self, entity: Entity) -> None:
    entity_out_of_bounds: bool = entity.get_y() < -200 or entity.get_y() > WINDOW_HEIGHT + 300
    if entity_out_of_bounds or not entity.alive:
      entity.delete()

      try:
        self.player.bullet_list.remove(entity)
      except ValueError:
        pass

      try:
        self.asteroid_list.remove(entity)
        if not entity.alive:
          self.score += entity.points
      except ValueError:
        pass

  def clear(self) -> None:
    for entity in self.asteroid_list + self.player.bullet_list:
      entity.delete()
    self.asteroid_list.clear()
    self.player.bullet_list.clear()
    self.lives_label.delete()
    self.score_label.delete()

  def end(self) -> None:
    self.ENDED = True
    self.clear()
    self.end_label: Label = pyglet.text.Label(text='PRESS \'R\' TO RESTART THE GAME OR \'ESC\' TO EXIT',
                                          font_size=20,
                                          x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2,
                                          color=(255, 255, 255, 255),
                                          anchor_x='center',
                                          batch=self.batch
                                          )
    self.end_label.position = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2, self.end_label.z)