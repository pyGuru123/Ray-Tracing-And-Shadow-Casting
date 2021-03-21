import pygame
from objects import Edge, Cell, convertTileMapToPolyMap, draw_grid

pygame.init()
win = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Shadow Casting')

clock = pygame.time.Clock()
FPS = 30

# world variabls

WORLDWIDTH = 40
WORLDHEIGHT = 30
TILE_SIZE = 16

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

world = [Cell() for i in range(WORLDWIDTH * WORLDHEIGHT)]

running = True
while running:
	win.fill(BLACK)
	# draw_grid(win)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONUP:
			x, y = pygame.mouse.get_pos()
			clicked = pygame.mouse.get_pressed()
			if not clicked[0]:
				index = y // TILE_SIZE * WORLDWIDTH + x // TILE_SIZE
				world[index].exist = not world[index].exist

	world, vecEdges = convertTileMapToPolyMap(0,0, 40, 30, TILE_SIZE, WORLDWIDTH, world)

	for i in range(WORLDHEIGHT):
		for j in range(WORLDWIDTH):
			index = i * WORLDWIDTH + j
			if world[index].exist:
				x, y = j * TILE_SIZE, i * TILE_SIZE
				w, h = TILE_SIZE, TILE_SIZE
				pygame.draw.rect(win, BLUE, (x,y,w,h))

	for edge in vecEdges:
		pygame.draw.line(win, WHITE, (edge.sx, edge.sy), (edge.ex, edge.ey))
		pygame.draw.circle(win, RED, (edge.sx, edge.sy), 3)
		pygame.draw.circle(win, RED, (edge.ex, edge.ey), 3)


	clock.tick(FPS)
	pygame.display.update()

pygame.quit()