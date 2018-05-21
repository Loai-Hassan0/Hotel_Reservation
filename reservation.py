from datetime import date


class Room(object):
    def __init__(self, room_num):
        self.number = room_num
        self.start = None
        self.end = None
        self.guest = None

    def book(self, from_date, till_date, guest_name):
        self.start = from_date
        self.end = till_date
        self.guest = guest_name

    def available(self, check_date= date.today()):
        return not self.start <= check_date <= self.end if self.start and self.end else True

    def __str__(self):
        return "Room("+str(self.number)+")"


class Hotel(object):
    def __init__(self, name, city, num_rooms):
        self.name = name
        self.city = city
        self.rooms = [Room(i+1) for i in range(num_rooms)]

    def room(self, room_num):
        return self.rooms[room_num - 1]

    def book_room(self, room_num, from_date, till_date, gest_name):
        self.room(room_num).book(from_date, till_date, gest_name)

    def avail_rooms(self):
        return [room.number for room in self.rooms if room.available()]

    def num_avail_rooms(self):
        return sum(room.available() for room in self.rooms)

    def __str__(self):
        return self.name


class Hotel_DB(object):
    def __init__(self):
        self.hotels = []

    def add_hotel(self, *args):
        if type(args[0]) == Hotel:
            self.hotels.append(args[0])
        else:
            self.hotels.append(Hotel(args[0], args[1], args[2]))

    def in_city(self, city):
        return [hotel.name for hotel in self.hotels if hotel.city == city]

    def avail_rooms(self, hotel_name, city):
        for hotel in self.hotels:
            if hotel.name == hotel_name and hotel.city == city:
                return hotel.avail_rooms()
        else:
            return "Hotel Not Found!"


hotels = Hotel_DB()
golden_hotel = Hotel("Golden", "Cairo", 250)
hotels.add_hotel(golden_hotel)
hotels.add_hotel("Galaxy", "Moscow", 360)
hotels.add_hotel("Galaxy", "Cairo", 400)
golden_hotel.book_room(11, date(2018, 5, 19), date(2018, 5, 23), "Mohamed")
golden_hotel.room(101).book(date(2018, 5, 17), date(2018, 5, 22), "Ahmed")
golden_hotel.book_room(110, date(2018, 5, 21), date(2018, 5, 24), "Mahmud")

print(golden_hotel.room(11).available(date(2018, 5, 23)))
print(golden_hotel.room(101).available(date(2018, 5, 7)))
print(golden_hotel.room(110).available(date(2018, 6, 28)))
print(golden_hotel.num_avail_rooms())
print(golden_hotel.room(123))
print(hotels.in_city("Cairo"))
print(hotels.avail_rooms("Golden", "Cairo"))

