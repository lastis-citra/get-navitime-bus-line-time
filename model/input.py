class InputData:
    def __init__(self, url, day, direction, destination_list):
        self.url = url
        self.day = day
        self.direction = direction
        self.destination_list = destination_list

    def __repr__(self):
        return f'(url: {self.url}, day: {self.day}, direction: {self.direction}), destination_list: {self.destination_list})'


class InputRouteData:
    def __init__(self, route_url, day, destination_list):
        self.route_url = route_url
        self.day = day
        self.destination_list = destination_list

    def __repr__(self):
        return f'(route_url: {self.route_url}, day: {self.day}, destination_list: {self.destination_list})'


class BusLineData:
    def __init__(self, bus_url, destination_list):
        self.bus_url = bus_url
        self.destination_list = destination_list

    def __repr__(self):
        return f'(bus_url: {self.bus_url}, destination_list: {self.destination_list})'
