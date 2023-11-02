import os, json


def LoadFile():
    with open("./local/local.json", "r") as file:
        return json.load(file)

def WriteFile(data: dict):
    with open("./local/local.json", "w") as file:
        json.dump(data, file, indent=4)
    return None


class Generator:
    def newItem(name: str, size: int):
        newItem = {
            "id": "juniper:{0}".format(name.lower().replace(" ", "_")),
            "name": name,
            "size": size
        }
        return newItem
    
    def newEnchantment(name: str, max_lvl: int):
        newEnchantment = {
            "id": "juniper:{0}".format(name.lower().replace(" ", "_")),
            "name": name,
            "max_lvl": max_lvl
        }
        return newEnchantment

    def newEquipment(name: str, durability: int):
        newEquipment = {
            "id": "juniper:{0}".format(name.lower().replace(" ", "_")),
            "name": name,
            "durability": durability
        }
        return newEquipment


# Gets the json data
Local                   = LoadFile()
LocalEquipment          = Local["Equipment"]
LocalItems              = Local["Items"]
LocalEnchantments       = Local["Enchantments"]

print(">> Generate Local Data")
while True:
    Type = input("Enter Type: ")

    if Type == "Equipment":
        Name = input("Name: ")
        Durability = input("Durability: ")

    elif Type == "Item":
        Name = input("Name: ")
        Size = input("Size: ")

    elif Type == "Enchantment":
        Name = input("Name: ")
        Max_Lvl = input("Max Lvl: ")

    elif Type == "#EXIT" or Type == "#exit" or Type == "#Exit":
        break

    else:
        pass


Local["Equipment"]           = LocalEquipment
Local["Items"]               = LocalItems
Local["Enchantments"]        = LocalEnchantments

WriteFile(Local)