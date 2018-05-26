"""
database.py
"""

from hotel import Hotel


class Hotel_DB(object):
    def __init__(self):
        self.database = dict()

    def add_hotel(self, *args):
        # Find a better way to take inputs and assign then to new_hotel
        new_hotel = args[0] if type(args[0]) == Hotel else Hotel(args[0], args[1], args[2])
        city = new_hotel.city
        hotel = new_hotel.name
        if city in self.database:
            if hotel in self.database[city]:
                return "hotel already exists!".title()
            self.database[city][hotel] = new_hotel
            return "hotel added successfully!".title()
        self.database[city] = {hotel: new_hotel}
        return "hotel added to a new city successfully!".title()

    def in_city(self, city):
        result = self.database.get(city, "city not found!".title())
        return {hotel: result[hotel].info() for hotel in result} if type(result) == dict else result

    def available_rooms(self, city, hotel, *args, detailed=False):
        # Modify to be compatible with its corresponding method in the hotel class. <DONE>
        if city in self.database:
            if hotel in self.database[city]:
                return self.database[city][hotel].available_rooms(*args, detailed=detailed)
        return "hotel not found!".title()

    def booked_rooms(self, city, hotel, *args, detailed=False):
        # Modify to be compatible with its corresponding method in the hotel class. <DONE>
        if city in self.database:
            if hotel in self.database[city]:
                return self.database[city][hotel].booked_rooms(*args, detailed=detailed)
        return "hotel not found!".title()

    def get_hotel(self, city, hotel):
        try:
            return self.database[city][hotel]
        except KeyError:
            assert "HotelNotFound!"

    def __str__(self):
        result = dict()
        for city in self.database:
            result[city] = dict()
            for hotel in self.database[city]:
                result[city][hotel] = self.database[city][hotel].info()
        return str(result)
