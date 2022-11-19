class StopData:
    def __init__(self, name: str, time: str):
        self.name = name
        self.time = time

    def __repr__(self):
        return f'(name: {self.name}, time: {self.time})'


class BusData:
    def __init__(self, destination: str, stop_list: list[StopData]):
        self.destination = destination
        self.stop_list = stop_list

    def __repr__(self):
        return f'(destination: {self.destination}, stop_list: {self.stop_list})'

    def get_name_list(self):
        name_list = []
        for stop in self.stop_list:
            name_list.append(stop.name)

        return name_list
