"""
hotel.py
"""

from datetime import date
from reservation import Reservation


class Room(object):
    def __init__(self, room_num):
        self.number = room_num
        self.reservations = []
        # Add more room attributes (capacity, price, floor level, description)

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

