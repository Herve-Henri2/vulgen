import json

class Scenario:
    
    def __init__(self, name, description, instructions, base, images, CVE, type, sources):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.base = base
        self.images = images
        self.cve = CVE
        self.type = type
        self.sources = sources

    def __str__(self):
        scenario = {}
        scenario['name'] = self.name
        scenario['description'] = self.description
        scenario['instructions'] = self.instructions
        scenario['base'] = self.base
        scenario['images'] = self.images
        scenario['CVE'] = self.cve
        scenario['type'] = self.type
        scenario['sources'] = self.sources
        return scenario


if __name__ == "__main__":
    pass