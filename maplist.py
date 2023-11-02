import json
import uuid
import random
from data.Block.Materials import *



class MapData:
    ''' Generates a new chunk of the map '''
    def __init__(self, size: int, block_size: int):
        self.uuid = uuid.uuid4()
        self.size = size
        self.block_size = block_size
    
    def BlockMaterial(self):
        choices = [getStone(), getSand(), getDirt(), getWater(), getLava()]
        choice = random.choice(choices)
        return choice
    
    def genCube(self, x: int, y: int):
        response = {
            "x": x,
            "y": y,
            "type": self.BlockMaterial()
        }
        return response
    
    def Line(self, y: int):
        line = []
        for x in range(0, self.size):
            line.append(self.genCube(x, y))
        return line
    
    def Chunk(self):
        chunk = []
        for y in range(0, self.size):
            chunk.append(self.Line(y))
        return chunk


if __name__ == "__main__":
    import pygame
    
    size = 32
    mapdata = MapData(16, size)
    genMap = mapdata.Chunk()
    
    screen = pygame.display.set_mode([700, 700])
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        for line in genMap:
            for cube in line:
                print(cube)
                pygame.draw.rect(screen, cube["type"], (cube["x"]+size, cube["y"]+size, size, size))
        
        pygame.display.update()
        screen.fill((0, 0, 0))