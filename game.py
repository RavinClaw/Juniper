import os, sys
import json
import socket
import select
import selectors
import pickle
import uuid
import zipfile
import pygame
import random
from datetime import datetime

#from structures.asset import Structure


pygame.init()
pygame.display.init()
pygame.font.init()


def LoadJSONFile(filename: str):
    with open(filename, "r") as file:
        return json.load(file)

def LoadFile(filename: str):
    with open(filename, "r") as file:
        return file.read().split("\n")

def LoadPlayerData():
    with open("./local/player-data.json", "r") as file:
        data = json.load(file)
    return data

def WritePlayerData(data: dict):
    with open("./local/player-data.json", "w") as file:
        json.dump(data, file, indent=4)
    return

def LoadDataFile(filename: str):
    with open(filename, "r") as file:
        return json.load(file)


Local           = LoadDataFile("./local/local.json")
# Loads in the items and enchantments
Items           = Local["Items"]
Enchantments    = Local["Enchantments"]


class GUI:
    def __init__(self, res: list=[700, 700]):
        self.session_id = uuid.uuid4()
        self.title = "|Juniper| Session: {0}".format(self.session_id)
        self.username = "default"
        self.player_id = "0000-0000-0000-0000"
        self.pos = [0, 0]
        self.playerSize = 32
        self.player_colour = (255, 0, 0)
        self.screen = pygame.display.set_mode(res)
        pygame.display.set_caption(self.title)
        self.InInv = False
        self.InMain = True
        self.InShop = False
        self.InForge = False
        self.InChest = False
        self.money = 0
        self.level = 0
        self.health = 100
        self.attack = 10
        self.defense = 12
        self.reputation = 0
        self.temp = Temp()
        
        self.temp.data["id"] = self.player_id
        self.last_input = ""
        
        self.Run()

    
    def Run(self):
        pygame.mouse.set_visible(False)
        chest1 = Chest(27)
        chest1.Generate()
        slotText = ""
        slotFont = pygame.font.Font(None, 16)
        slotColour = (75, 0, 130)
        filepath = "./structures/house"
        structure = LoadFile(filepath + "/structure.map")
        cont = LoadJSONFile(filepath + "/cont.json")
        Player = Character(self.screen, (255, 0, 0))
        chest = chest1.GetTable()
        default_chest_x = self.screen.get_width() / 3.5
        default_chest_y = self.screen.get_height() / 2
        size = 27
        slot_size = 32
        perline = 9
        lines = 0
        
        run = True
        while run:
            Cursor = pygame.mouse.get_pos()
            Click = pygame.mouse.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and self.InMain:
                        Player.UpdatePos(0, -32)
                        self.last_input = "W"
                    elif event.key == pygame.K_s and self.InMain:
                        Player.UpdatePos(0, 32)
                        self.last_input = "S"
                    elif event.key == pygame.K_a and self.InMain:
                        Player.UpdatePos(-32, 0)
                        self.last_input = "A"
                    elif event.key == pygame.K_d and self.InMain:
                        Player.UpdatePos(32, 0)
                        self.last_input = "D"
                    
                    
                    elif event.key == pygame.K_e:
                        if self.InMain and not self.InInv:
                            self.InInv = True
                            self.InMain = False
                        elif not self.InMain and self.InInv:
                            self.InInv = False
                            self.InMain = True
                    
                    elif event.key == pygame.K_l:
                        if self.InMain and not self.InChest:
                            self.InChest = True
                            self.InMain = False
                        elif not self.InMain and self.InChest:
                            self.InChest = False
                            self.InMain = True
            
            if self.InInv:
                ...
            
            if self.InChest:
                chest_x = default_chest_x
                chest_y = default_chest_y
                lines = 0
                for x in range(0, size):
                    if lines >= perline:
                        chest_y += slot_size
                        chest_x = default_chest_x
                        lines = 0
                    
                    Slot1 = chest[x]
                    Slot2 = Slot1["Slot"]
                    Slot = Slot2["Slot"]
                    slotText = Slot["name"]
                    SlotRect = pygame.Rect(chest_x + 10, chest_y + 10, slot_size / 1.2, slot_size / 1.2)
                    if slotText != "Empty":
                        if SlotRect.collidepoint((Cursor[0], Cursor[1])):
                            slotRender = slotFont.render(slotText, True, slotColour)
                            self.screen.blit(slotRender, (Cursor[0], Cursor[1] - 30))
                            
                        if SlotRect.collidepoint((Cursor[0], Cursor[1])) and Click[0]:
                            self.temp.data["Inventory"].append(Slot)
                            Slot = { "id": "juniper:empty", "name": "Empty", "size": 126, "color": [255, 255, 255] }
                            Slot2["Slot"] = Slot
                            Slot1["Slot"] = Slot2
                            chest[x] = Slot1
                    pygame.draw.rect(self.screen, Slot["color"], SlotRect)
                    chest_x += slot_size
                    lines += 1
            
            if self.InMain:
                pos_x = 0
                pos_y = 0
                for struct_line in structure:
                    pos_y += 32
                    pos_x = 0
                    for block in struct_line:
                        pos_x += 32
                        if not block == " ": # Checks if the Block isn't Floor
                            block_rect = pygame.Rect(pos_x, pos_y, 32, 32)
                            if Player.Collide(block_rect) and not block == "D":
                                if self.last_input == "W":
                                    Player.UpdatePos(0, 32)
                                elif self.last_input == "S":
                                    Player.UpdatePos(0, -32)
                                elif self.last_input == "A":
                                    Player.UpdatePos(32, 0)
                                elif self.last_input == "D":
                                    Player.UpdatePos(-32, 0)
                        if block == "W": # Window
                            pygame.draw.rect(self.screen, (123, 190, 239), (pos_x, pos_y, 32, 32))
                        elif block == "D": # Door
                            pygame.draw.rect(self.screen, (132, 65, 16), (pos_x, pos_y, 32, 32))
                        elif block == "#": # Wall
                            pygame.draw.rect(self.screen, (74, 74, 74), (pos_x, pos_y, 32, 32))
                        else:
                            pygame.draw.rect(self.screen, (174, 106, 57), (pos_x, pos_y, 32, 32))
                
                Player.Render()

            pygame.draw.rect(self.screen, (0, 255, 0), (Cursor[0] -4, Cursor[1] -4, 8, 8))
            pygame.display.update()
            if self.InMain:
                self.screen.fill((86, 125, 70))
            if self.InChest:
                self.screen.fill((0, 0, 0))
            self.temp.data["position"] = self.pos
            self.temp.data["money"] = self.money
            self.temp.data["level"] = self.level
            self.temp.data["health"] = self.health
            self.temp.data["attack"] = self.attack
            self.temp.data["defense"] = self.defense
            self.temp.data["reputation"] = self.reputation
        
        #print(self.temp.data)
        givenTime = datetime.now()
        day = givenTime.strftime("%d")
        month = givenTime.strftime("%m")
        year = givenTime.strftime("%Y")
        minute = givenTime.strftime("%M")
        hour = givenTime.strftime("%H")
        self.temp.data["SavedData"]["Last Played"].append({
            "hour": hour,
            "minute": minute,
            "day": day,
            "month": month,
            "year": year
        })
        with open("./temp/{0}-{1}.json".format(self.session_id, self.player_id), "w") as file:
            json.dump(self.temp.data, file, indent=4)


class Temp:
    #? Store Temporary Data
    data = {
        "id": "",
        "state": "$temp",
        "SavedData": {"Last Played": []}, 
        "Inventory": [],
        "money": 0,
        "level": 0,
        "health": 100,
        "attack": 10,
        "defense": 12,
        "reputation": 0,
        "op": False,
        "position": [0, 0]
    }


class Inventory:
    ''' Grabs the inventory from Temp.data '''
    def GrabItem(Temp: object, itemName: str, itemID: str):
        Inventory = Temp.data["Inventory"]
        
        for Slot in Inventory:
            if Slot["name"] == itemName and Slot["id"] == itemID:
                return  Slot
    
    
    def SetItem(Temp: object, itemData: dict):
        Inventory = Temp.data["Inventory"]
        
        Inventory.append(itemData)
        
        Temp.data["Inventory"] = Inventory
    
    def ModifyItem(Temp: object):
        ...

class Character:
    def __init__(self, screen, colour):
        self.pos = [0, 0]
        self.colour = colour
        self.size = 32
        self.screen = screen

    def Render(self):
        pygame.draw.rect(self.screen, self.colour, (self.pos[0], self.pos[1], self.size, self.size))
        return None

    def UpdatePos(self, x, y):
        px = self.pos[0]
        py = self.pos[1]
        self.pos[0] = px + x
        self.pos[1] = py + y
        return None
    
    def Collide(self, other):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        collide = rect.colliderect(other)
        return collide
    
    def GetPos(self):
        return self.pos
    
    def GetColour(self):
        return self.colour
    
    def GetSize(self):
        return self.size

class Chest:
    def __init__(self, size):
        self.size = size
        self.table = {}
        self.rarity = random.random()
        self.Local = LoadJSONFile("./local/local.json")
        self.LocalEquipment = self.Local["Equipment"]
        self.LocalEnchantments = self.Local["Enchantments"]
        self.LocalItems = self.Local["Items"]

    def Generate(self):
        newTable = []
        
        for x in range(0, self.size):
            regSlot = self.GenSlot()
            newSlot = {
                "ID": x,
                "Slot": regSlot
            }
            newTable.append(newSlot)
        
        self.table = newTable
    
    def GenSlot(self):
        if random.randint(1, 10) >= 7:
            choice = random.choice(self.LocalEquipment + self.LocalItems)
            slot = { "Slot": choice }
        else:
            slot = { "Slot": { "id": "juniper:empty", "name": "Empty", "size": 0, "color": [255 ,255, 255] } }
        return slot
    
    def GetTable(self):
        return self.table


if __name__ == "__main__":
    gui = GUI()