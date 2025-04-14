class InputData:
    def __init__(self, url, day, direction, origin, destination_list):
        self.url = url
        self.day = day
        self.direction = direction
        self.origin = origin
        self.destination_list = destination_list

    def __repr__(self):
        return (f'(url: {self.url}, day: {self.day}, direction: {self.direction}),'
                f' origin: {self.origin}, destination_list: {self.destination_list})')


class InputRouteData:
    def __init__(self, route_url, day, origin, destination_list):
        self.route_url = route_url
        self.day = day
        self.origin = origin
        self.destination_list = destination_list

    def __repr__(self):
        return (f'(route_url: {self.route_url}, day: {self.day}, origin: {self.origin}, '
                f'destination_list: {self.destination_list})')


class BusLineData:
    def __init__(self, bus_url, origin, destination_list):
        self.bus_url = bus_url
        self.origin = origin
        self.destination_list = destination_list

    def __repr__(self):
        return f'(bus_url: {self.bus_url}, origin: {self.origin}, destination_list: {self.destination_list})'
