import json

class Scenario:
    
    def __init__(self, name, description, base, images, type):
        self.name = name
        self.description = description
        self.base = base
        self.images = images
        self.type = type

    def __str__(self):
        scenario = {}
        scenario['name'] = self.name
        scenario['description'] = self.description
        scenario['base'] = self.base
        scenario['images'] = self.images
        scenario['type'] = self.type
        return scenario


if __name__ == "__main__":
    pass