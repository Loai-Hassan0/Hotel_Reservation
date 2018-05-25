from datetime import date


class Customer(object):
    def __init__(self, name, phone_num):
        self.name = name
        self.phone = phone_num

    def confirm_reservation(self):
        # Sends a text message to the customer confirming there reservation
        pass


class Reservation(object):
    def __init__(self, guest, from_date, till_date=None):
        self.guest = guest
        self.start = from_date
        self.end = till_date

    def get_dates(self):
        return (self.start, self.end) if self.end else (self.start,)


class Room(object):
    def __init__(self, room_num):
        self.number = room_num
        self.reservations = []
        # Add room (capacity, price, floor level, description)

    def available(self, *args):
        days = sorted(args[:]) if len(args) > 0 else [date.today()]
        avail = True
        for reservation in self.reservations:
            avail = days[-1] < reservation.get_dates()[0] or reservation.get_dates()[-1] < days[0]
            if not avail:
                break
        return avail

    def book(self, guest, *args):
        # Modify to include all input cases. <DONE>
        if self.available(*args):
            self.reservations.append(Reservation(guest, *args))
            return self.reservations[-1]  # "booked successfully!".title()
        return False  # "room unavailable!".title()

    def find_reservation(self, guest):
        for reservation in self.reservations:
            if reservation.guest == guest:
                return reservation
        return False

    def cancel_reservation(self, guest):
        for i, reservation in enumerate(self.reservations):
            if reservation.guest == guest:
                return self.reservations.pop(i)  # "your reservation has been canceled successfully!".title()
        return False  # "couldn't find your reservation!".title()

    def edit_reservation(self, guest, *args):
        # find reservation by guest then make changes if available or return an unavailable message if not. <DONE>
        old = self.cancel_reservation(guest)
        new = self.book(guest, *args)
        if new:
            return new
        if old:
            self.reservations.append(old)
        return False

    def info(self):
        # Returns a dictionary of the room's information
        pass

    def __str__(self):
        # Modify to use the info method
        return "*Room({})".format(self.number)


class Hotel(object):
    def __init__(self, name, city, num_rooms):
        self.name = name
        self.city = city
        self.rooms = [Room(i + 1) for i in range(num_rooms)]

    def room(self, room_num):
        return self.rooms[room_num - 1]

    def num_rooms(self):
        return len(self.rooms)

    def available_rooms(self, *args, detailed=False):
        # Modify to include any dates. <DONE>
        # Modify to display overall available rooms.
        if detailed:
            # Change to display room info instead of just the number
            return [room.number for room in self.rooms if room.available(*args)]
        return sum(room.available(*args) for room in self.rooms)

    def booked_rooms(self, *args, detailed=False):
        # Modify to include any dates. <DONE>
        # Modify to display overall reservations.
        if detailed:
            # Change to display room info instead of just the number
            return [room.number for room in self.rooms if not room.available(*args)]
        return sum(not room.available(*args) for room in self.rooms)

    def book_room(self, room_num, guest, *args):
        # Modify to include all input cases. <DONE>
        return self.room(room_num).book(guest, *args)

    def info(self):
        return {"name": self.name,
                "city": self.city,
                "number of rooms": self.num_rooms()}

    def __str__(self):
        return str(self.info())


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
