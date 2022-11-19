class InputData:
    def __init__(self, url, day, direction):
        self.url = url
        self.day = day
        self.direction = direction

    def __repr__(self):
        return f'(url: {self.url}, day: {self.day}, direction: {self.direction})'
