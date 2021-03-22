import pygame
import math
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

vecVisibilityPolygonPoints = [None, None, None]

def calculateVisibilityPolygon(ox, oy, radius, vecEdges):
	vecVisibilityPolygonPoints.clear()

	for edge in vecEdges:
		for i in range(2):
			rdx = (edge.sx if i == 0 else edge.ex) - ox
			rdy = (edge.sy if i == 0 else edge.ey) - oy

			base_ang = math.atan2(rdy, rdx)
			ang = 0

			for j in range(3):
				if j == 0:
					ang = base_ang - 0.0001
				if j == 1:
					ang = base_ang
				if j == 2:
					ang = base_ang + 0.0001

				rdx = radius * cos(ang)
				rdy = radius * sin(ang)

				min_t1 = float('inf')
				min_px, min_py, min_ang = 0, 0, 0

				for e2 in vecEdges:
					sdx = e2.ex - e2.sx
					sdy = e2.ey - e2.sy

					if abs(sdx - rdx) > 0.0 and abs(sdy - rdy) > 0.0:
						t2 = (rdx * (e2.sy - oy) + (rdy * (ox - e2.sx))) / (sdx * rdy - sdy * rdx)
						t1 = (e2.sx + sdx * t2 - ox) / rdx

						if t1 > 0 and t2 >= 0 and t2 <= 1:
							if t1 < min_t1:
								min_t1 = t1
								min_px = ox + rdx * t1
								min_py = oy + rdy * t1
								min_ang = math.atan2(min_py - oy, min_px - ox)

			vecVisibilityPolygonPoints.append((min_ang, min_px, min_py))

	vecVisibilityPolygonPoints.sort(key= lambda t : t[0])



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
		if event.type == pygame.MOUSEBUTTONDOWN:
			sourceX, sourceY = pygame.mouse.get_pos()
			clicked = pygame.mouse.get_pressed()
			if clicked[2]:
				calculateVisibilityPolygon(sourceX, sourceY, 1000, vecEdges)
			if clicked[2] and len(vecVisibilityPolygonPoints) > 1:
				for i in range(len(vecVisibilityPolygonPoints) - 1):
					point1 = vecVisibilityPolygonPoints[i]
					point2 = vecVisibilityPolygonPoints[i+1]
					pygame.draw.polygon(win, [(sourceX, sourceY), (point1[1], point1[2]),
								(point2[1], point2[2])])


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