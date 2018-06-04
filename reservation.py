"""
reservation.py
"""

from customer import Customer
from datetime import date


class Reservation(object):
    new_id = 0
    reservations = []

    def __init__(self, customer, hotel, room, check_in_date, check_out_date):
        self.id_number = "R_"
        self.customer = customer
        self.hotel = hotel
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def update(self, action):
        # Might need to check if the reservation excites or not!
        self.customer.update_reservations(self, action)
        self.hotel.update_reservations(self, action)
        self.room.update_reservations(self, action)

    def add_reservation(self):
        if self not in self.reservations:
            self.id_number += str(Reservation.new_id)
            self.reservations.append(self)
            self.update(list.append)
            Reservation.new_id += 1

    @classmethod
    def get_reservation(cls, **kwargs):
        pass

    def edit_reservation(self, **kwargs):
        # Must check availability of the new information!
        # Must update the reservations accordingly!
        self.hotel = kwargs.get("hotel", self.hotel)
        self.room = kwargs.get("room", self.room)
        self.check_in_date = kwargs.get("check_in_date", self.check_in_date)
        self.check_out_date = kwargs.get("check_out_date", self.check_out_date)

    def delete_reservation(self):
        if self in self.reservations:
            self.reservations.remove(self)
            self.update(list.remove)


if __name__ == "__main__":
    from hotel import Hotel, Room
