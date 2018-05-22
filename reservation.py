from datetime import date


class Room(object):
    def __init__(self, room_num):
        self.number = room_num
        self.start = None
        self.end = None
        self.guest = None

    def available(self, check_date=date.today()):
        return not self.start <= check_date <= self.end if self.start and self.end else True

    def book(self, from_date, till_date, guest_name):
        self.start = from_date
        self.end = till_date
        self.guest = guest_name

    def __str__(self):
        return "*Room({}):\n\t-Available: {}".format(self.number, self.available())


class Hotel(object):
    def __init__(self, name, city, num_rooms):
        self.name = name
        self.city = city
        self.rooms = [Room(i+1) for i in range(num_rooms)]

    def room(self, room_num):
        return self.rooms[room_num - 1]

    def avail_rooms(self):
        return [room.number for room in self.rooms if room.available()]

    def num_avail_rooms(self):
        return sum(room.available() for room in self.rooms)

    def book_room(self, room_num, from_date, till_date, gest_name):
        self.room(room_num).book(from_date, till_date, gest_name)

    def __str__(self):
        return self.name


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
        return self.hotels[city]

    def avail_rooms(self, hotel, city):
        if city in self.hotels:
            if hotel in self.hotels[city]:
                return self.hotels[city][hotel].avail_rooms()
        return "hotel not found!".title()

    def __str__(self):
        return str(self.hotels)


hotels = Hotel_DB()
golden_hotel = Hotel("Golden", "Cairo", 250)

print(hotels.add_hotel(golden_hotel))
print(hotels.add_hotel("Galaxy", "Moscow", 360))
print(hotels.add_hotel("Galaxy", "Cairo", 400))

golden_hotel.book_room(11, date(2018, 5, 19), date(2018, 5, 23), "Mohamed")
golden_hotel.room(101).book(date(2018, 5, 17), date(2018, 5, 22), "Ahmed")
golden_hotel.book_room(110, date(2018, 5, 21), date(2018, 5, 24), "Mahmud")

print(golden_hotel.room(11).available(date(2018, 5, 23)))
print(golden_hotel.room(101).available(date(2018, 5, 7)))
print(golden_hotel.room(110).available(date(2018, 6, 28)))
print(golden_hotel.num_avail_rooms())
print(golden_hotel.room(123))
print(hotels.in_city("Cairo"))
print(hotels)
# print(hotels.avail_rooms("Golden", "Cairo"))
print(hotels.avail_rooms("Golden", "Moscow"))
