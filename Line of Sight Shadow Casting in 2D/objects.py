import math
import pygame

WORLDWIDTH = 40
WORLDHEIGHT = 30
TILE_SIZE = 16

WHITE = (255, 255, 255)

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3


class Edge:
	def __init__(self):
		self.sx, self.sy = (None, None)
		self.ex, self.ey = (None, None)

	def __str__(self):
		return f'Start Point : {(self.sx, self.sy)}, End Point : {(self.ex, self.ey)}'

class Cell:
	def __init__(self):
		self.edge_id = [None for i in range(4)]
		self.edge_exist = [None for i in range(4)]
		self.exist = False

def convertTileMapToPolyMap(sx, sy, w, h, tile_size, pitch, world):
	vecEdges = []

	for x in range(w):
		for y in range(h):
			index = (y + sy) * pitch + (x + sx)
			for j in range(4):
				world[index].edge_exist[j] = False
				world[index].edge_id[j] = 0

	for x in range(1, w-1):
		for y in range(1, h-1):
			i = (y + sy) * pitch + (x + sx)      # Current cell
			n = (y + sy - 1) * pitch + (x + sx)  # northern neighbour
			s = (y + sy + 1) * pitch + (x + sx)  # southern neighbour
			w = (y + sy) * pitch + (x + sx - 1)  # western neighbour
			e = (y + sy) * pitch + (x + sx + 1)  # eastern neighbour

			if world[i].exist:
				if not world[w].exist:
					if world[n].edge_exist[WEST]:
						vecEdges[world[n].edge_id[WEST]].ey += TILE_SIZE
						world[i].edge_id[WEST] = world[n].edge_id[WEST]
						world[i].edge_exist[WEST] = True
					else:
						edge = Edge()
						edge.sx = (sx + x) * TILE_SIZE
						edge.sy = (sy + y) * TILE_SIZE
						edge.ex = edge.sx
						edge.ey = edge.sy + TILE_SIZE

						edge_id = len(vecEdges)
						vecEdges.append(edge)

						world[i].edge_id[WEST] = edge_id
						world[i].edge_exist[WEST] = True



				if not world[e].exist:
					if world[n].edge_exist[EAST]:
						vecEdges[world[n].edge_id[EAST]].ey += TILE_SIZE
						world[i].edge_id[EAST] = world[n].edge_id[EAST]
						world[i].edge_exist[EAST] = True
					else:
						edge = Edge()
						edge.sx = (sx + x + 1) * TILE_SIZE
						edge.sy = (sy + y) * TILE_SIZE
						edge.ex = edge.sx
						edge.ey = edge.sy + TILE_SIZE

						edge_id = len(vecEdges)
						vecEdges.append(edge)

						world[i].edge_id[EAST] = edge_id
						world[i].edge_exist[EAST] = True



				if not world[n].exist:
					if world[w].edge_exist[NORTH]:
						vecEdges[world[w].edge_id[NORTH]].ex += TILE_SIZE
						world[i].edge_id[NORTH] = world[w].edge_id[NORTH]
						world[i].edge_exist[NORTH] = True
					else:
						edge = Edge()
						edge.sx = (sx + x) * TILE_SIZE
						edge.sy = (sy + y) * TILE_SIZE
						edge.ex = edge.sx + TILE_SIZE
						edge.ey = edge.sy

						edge_id = len(vecEdges)
						vecEdges.append(edge)

						world[i].edge_id[NORTH] = edge_id
						world[i].edge_exist[NORTH] = True



				if not world[s].exist:
					if world[w].edge_exist[SOUTH]:
						vecEdges[world[w].edge_id[SOUTH]].ex += TILE_SIZE
						world[i].edge_id[SOUTH] = world[w].edge_id[SOUTH]
						world[i].edge_exist[SOUTH] = True
					else:
						edge = Edge()
						edge.sx = sx + x * TILE_SIZE
						edge.sy = (sy + y + 1) * TILE_SIZE
						edge.ex = edge.sx + TILE_SIZE
						edge.ey = edge.sy

						edge_id = len(vecEdges)
						vecEdges.append(edge)

						world[i].edge_id[SOUTH] = edge_id
						world[i].edge_exist[SOUTH] = True

	return world, vecEdges

def calculateVisibilityPolygon(ox, oy, radius, vecEdges):
	vecVisibilityPolygonPoints= []
	
	for edge in vecEdges:
		for i in range(2):
			bValid = False
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

				rdx = radius * math.cos(ang)
				rdy = radius * math.sin(ang)

				min_t1 = float('inf')
				min_px, min_py, min_ang = 0, 0, 0

				for e2 in vecEdges:
					sdx = e2.ex - e2.sx
					sdy = e2.ey - e2.sy

					if abs(sdx - rdx) > 0 and abs(sdy - rdy) > 0:
						t2 = (rdx * (e2.sy - oy) + (rdy * (ox - e2.sx))) / (sdx * rdy - sdy * rdx)
						t1 = (e2.sx + sdx * t2 - ox) / rdx

						if t1 > 0 and t2 >= 0 and t2 <= 1:
							if t1 < min_t1:
								min_t1 = t1
								min_px = ox + rdx * t1
								min_py = oy + rdy * t1
								min_ang = math.atan2(min_py - oy, min_px - ox)
								bValid = True
				if bValid:
					vecVisibilityPolygonPoints.append((min_ang, min_px, min_py))

	vecVisibilityPolygonPoints = list(set(vecVisibilityPolygonPoints))
	vecVisibilityPolygonPoints.sort(key= lambda t : t[0])
	return vecVisibilityPolygonPoints

def draw_grid(win):
	for i in range(31):
		pygame.draw.line(win, WHITE, (0, i * TILE_SIZE), (640, i * TILE_SIZE))
	for j in range(41):
		pygame.draw.line(win, WHITE, (j * TILE_SIZE, 0), (j * TILE_SIZE, 480))