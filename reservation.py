from datetime import date


class Customer(object):
    def __init__(self, name, phone_num):
        self.name = name
        self.phone = phone_num


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

    def available(self, *args):
        days = sorted(args[:]) if len(args) > 0 else [date.today()]
        result = True
        for reservation in self.reservations:
            result = days[-1] < reservation.get_dates()[0] or reservation.get_dates()[-1] < days[0]
            if not result:
                break
        return result

    def book(self, from_date, till_date, guest_name):
        if self.available(from_date, till_date):
            self.reservations.append(Reservation(guest_name, from_date, till_date))
            return "booked successfully!".title()
        return "room unavailable!".title()

    def __str__(self):
        return "*Room({}):\n\t-Available: {}".format(self.number, self.available())


class Hotel(object):
    def __init__(self, name, city, num_rooms):
        self.name = name
        self.city = city
        self.rooms = [Room(i+1) for i in range(num_rooms)]

    def room(self, room_num):
        return self.rooms[room_num - 1]

    def num_rooms(self):
        return len(self.rooms)

    def avail_rooms(self, display=False):
        if display:
            return [room.number for room in self.rooms if room.available()]
        return "number of available rooms: {}".format(sum(room.available() for room in self.rooms)).title()

    def book_room(self, room_num, from_date, till_date, guest_name):
        return self.room(room_num).book(from_date, till_date, guest_name)

    def info(self):
        return {"name": self.name,
                "city": self.city,
                "number of rooms": self.num_rooms()}

    def __str__(self):
        return str(self.info())


class Hotel_DB(object):
    def __init__(self):
        self.hotels = dict()

    def add_hotel(self, *args):
        new_hotel = args[0] if type(args[0]) == Hotel else Hotel(args[0], args[1], args[2])
        city = new_hotel.city
        hotel = new_hotel.name
        if city in self.hotels:
            if hotel in self.hotels[city]:
                return "hotel already exists!".title()
            self.hotels[city][hotel] = new_hotel
            return "hotel added successfully!".title()
        self.hotels[city] = {hotel: new_hotel}
        return "hotel added to a new city successfully!".title()

    def in_city(self, city):
        result = self.hotels.get(city, "city not found!".title())
        return {hotel: result[hotel].info() for hotel in result} if type(result) == dict else result

    def avail_rooms(self, city, hotel, display=False):
        if city in self.hotels:
            if hotel in self.hotels[city]:
                return self.hotels[city][hotel].avail_rooms(display)
        return "hotel not found!".title()

    def __str__(self):
        result = dict()
        for city in self.hotels:
            result[city] = dict()
            for hotel in self.hotels[city]:
                result[city][hotel] = self.hotels[city][hotel].info()
        return str(result)


hotels = Hotel_DB()
golden_hotel = Hotel("Golden", "Cairo", 250)

print(hotels.add_hotel(golden_hotel))
print(hotels.add_hotel("Galaxy", "Moscow", 360))
print(hotels.add_hotel("Galaxy", "Cairo", 400))
print("=" * 50)

print(golden_hotel.book_room(11, date(2018, 5, 19), date(2018, 5, 23), "Mohamed"))
print(golden_hotel.room(101).book(date(2018, 5, 18), date(2018, 5, 25), "Ahmed"))
print(golden_hotel.book_room(110, date(2018, 6, 28), date(2018, 7, 3), "Mahmud"))
print(golden_hotel.book_room(110, date(2018, 7, 1), date(2018, 7, 5), "Mahmud"))
print("=" * 50)

print(golden_hotel.room(11).available(date(2018, 5, 23)))
print(golden_hotel.room(101).available(date(2018, 5, 7), date(2018, 5, 12)))
print(golden_hotel.room(110).available(date(2018, 6, 25), date(2018, 7, 1)))
print(golden_hotel.avail_rooms())
print("=" * 50)

print(golden_hotel.room(123))
print("=" * 50)

print(hotels.in_city("Cairo"))
print("=" * 50)
print(hotels.in_city("Rostov"))
print("=" * 50)
print(hotels)
print("=" * 50)
print(hotels.avail_rooms("Cairo", "Golden", True))
print(hotels.avail_rooms("Moscow", "Golden"))
