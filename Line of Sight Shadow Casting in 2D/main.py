import pygame
from objects import Edge, Cell, convertTileMapToPolyMap, calculateVisibilityPolygon, draw_grid

pygame.init()
win = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Shadow Casting')

clock = pygame.time.Clock()
FPS = 18

font = pygame.font.SysFont('Verdana', 14) 

light_image = pygame.image.load('light_cast.png')
light_image = pygame.transform.scale(light_image, (32,32))

# world variabls

WORLDWIDTH = 40
WORLDHEIGHT = 30
TILE_SIZE = 16

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


world = [Cell() for i in range(WORLDWIDTH * WORLDHEIGHT)]
for x in range(1, WORLDWIDTH - 1):
	world[1 * WORLDWIDTH + x].exist = True
	world[(WORLDHEIGHT - 2) * WORLDWIDTH + x].exist = True
for x in range(1, (WORLDHEIGHT - 1)):
	world[x * WORLDWIDTH + 1].exist = True
	world[x * WORLDWIDTH + (WORLDWIDTH - 2)].exist = True

running = True
vecVisibilityPolygonPoints = []
raysCasted = 0
while running:
	win.fill(BLACK)
	# draw_grid(win)

	x, y = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
		if pygame.mouse.get_pressed()[0] == 1:
			if 32 <= x <= 608 and 32 <= y <= 448:
				index = y // TILE_SIZE * WORLDWIDTH + x // TILE_SIZE
				world[index].exist = not world[index].exist

	if pygame.mouse.get_pressed()[2] == 1:
		if 32 <= x <= 608 and 32 <= y <= 448:
			img_rect = light_image.get_rect(center=(x,y))
			win.blit(light_image, img_rect)

			vecVisibilityPolygonPoints = calculateVisibilityPolygon(x, y, 1000, vecEdges)
			if vecVisibilityPolygonPoints:
				for i in range(len(vecVisibilityPolygonPoints) - 1):
					point1 = vecVisibilityPolygonPoints[i]
					point2 = vecVisibilityPolygonPoints[i+1]
					point3 = vecVisibilityPolygonPoints[len(vecVisibilityPolygonPoints) - 1]
					point4 = vecVisibilityPolygonPoints[0]

					pygame.draw.polygon(win, WHITE, [(x, y), (point1[1], point1[2]),
								(point2[1], point2[2])])
					pygame.draw.polygon(win, WHITE, [(x, y), (point3[1], point3[2]),
								(point4[1], point4[2])])
				pygame.draw.polygon(win, WHITE, [(x, y), (point1[1], point1[2]),
								(point2[1], point2[2])])

			raysCasted = len(vecVisibilityPolygonPoints)
	else:
		raysCasted = 0

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

	pygame.draw.rect(win, BLACK, (0,0,640,16))
	pygame.draw.rect(win, BLACK, (0,0,16,480))
	pygame.draw.rect(win, BLACK, (0,464,640,16))
	pygame.draw.rect(win, BLACK, (624,0,16,480))

	text = font.render(f'Rays Casted : {raysCasted}', True, WHITE)
	rect = text.get_rect(center=(70,5))
	win.blit(text, rect)

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()