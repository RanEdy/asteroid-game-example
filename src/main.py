import pyglet, gamewindow
# TODO
# * Crear una hitbox reducida para verficar la colision con esa hitbox
# - Que el chequeo de colisiones sea del lado de la entidad y no del juego
# - Agregar la invulnerabilidad del lado de la entidad
#
def main() -> None:
  FPS: int = 144
  game = gamewindow.GameWindow()
  pyglet.clock.schedule(game.update)
  pyglet.app.run(1/(FPS*2))

if __name__ == '__main__':
  main()