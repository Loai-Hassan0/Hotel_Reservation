"""
hotel.py
"""

from customer import Customer
from datetime import date
from reservation import Reservation


class Room(object):
    def __init__(self, number: int) -> None:
        self.number = number
        self.reservations = []

    def available(self, check_in_date: date, check_out_date: date) -> bool:
        for reservation in self.reservations:
            if not any([check_out_date < reservation.check_in_date, reservation.check_out_date < check_in_date]):
                return False
        return True

    def update_reservations(self, reservation, action) -> None:
        actions = [list.append, list.remove]
        if reservation.room is not self:
            raise ValueError("This reservation doesn't belong to this room!")
        if action not in actions:
            raise ValueError("Invalid action us passed!")
        if reservation in self.reservations and action is list.append:
            raise ValueError("This reservation already exists!")
        if reservation not in self.reservations and action is list.remove:
            raise ValueError("The reservation you're trying to delete doesn't exist!")
        action(self.reservations, reservation)


class Hotel(object):
    new_id = 0
    hotels = {}

    def __init__(self, name: str, city: str, number_of_rooms: int) -> None:
        self.__test_inputs(name=name, city=city, number_of_rooms=number_of_rooms)
        self.id_number = "H_"
        self.name = name
        self.city = city
        self.rooms = {number + 1: Room(number + 1) for number in range(number_of_rooms)}
        self.reservations = []

    @staticmethod
    def __test_inputs(**kwargs) -> None:
        inputs = {"name", "city", "number_of_rooms", "check_in_date", "check_out_date", "room", "customer"}
        if inputs.intersection(set(kwargs)) != set(kwargs):
            raise ValueError("{} aren't attributes of Hotel!".format(list(set(kwargs).difference(inputs))))
        type_tests = dict(name=str, city=str, number_of_rooms=int, check_in_date=date, check_out_date=date,
                          room=Room, customer=Customer)
        for case in kwargs:
            if not isinstance(kwargs[case], type_tests[case]):
                raise TypeError("{} must be a {}!".format(case, type_tests[case]))
        value_tests = dict(name=lambda x: len(x) > 100,
                           city=lambda x: len(x) > 50,
                           number_of_rooms=lambda x: x <= 0,
                           check_in_date=lambda x: x < date.today(),
                           check_out_date=lambda x: x <= kwargs.get("check_in_date", date.today()),
                           room=False,  # Must check that the room is in the hotel!
                           customer=lambda x: not Customer.get_customer(x.phone_number) is x)
        for case in kwargs:
            if value_tests[case](kwargs[case]):
                raise ValueError("Incorrect input value for {}!".format(case))

    def add_hotel(self) -> None:
        if self.get_hotel(self.city, self.name) is self:
            raise ValueError("This hotel already exists!")
        if self.name in self.get_hotels_in_city(self.city):
            raise ValueError("There's already a hotel called {} in {}!".format(self.name, self.city))
        self.id_number += str(Hotel.new_id)
        self.hotels[self.city] = self.hotels.get(self.city, {})
        self.hotels[self.city][self.name] = self.hotels[self.city].get(self.name, self)
        Hotel.new_id += 1

    @classmethod
    def get_hotels_in_city(cls, city: str) -> dict:
        cls.__test_inputs(city=city)
        return cls.hotels.get(city, {})

    @classmethod
    def get_hotel(cls, city: str, hotel_name: str) -> object:
        cls.__test_inputs(city=city, name=hotel_name)
        return cls.get_hotels_in_city(city).get(hotel_name, {})

    def edit_hotel(self, **kwargs) -> None:
        # Mustn't have conflict with reservations!
        pass

    def delete_hotel(self) -> None:
        if self.get_hotel(self.city, self.name) is not self:  # self.name not in self.get_hotels_in_city(self.city) or
            raise ValueError("the hotel you're trying to delete doesn't exist!")
        temp_reservations = self.reservations.copy()
        temp_rooms = self.rooms.copy()
        for reservation in temp_reservations:
            reservation.delete_reservation()
        for room in temp_rooms:
            del self.rooms[room]
        del self.hotels[self.city][self.name]

    def get_room(self, room_number: int) -> object:
        self.__test_inputs(number_of_rooms=room_number)
        return self.rooms.get(room_number, {})

    def get_available_rooms(self, check_in_date: date, check_out_date: date) -> dict:
        self.__test_inputs(check_in_date=check_in_date, check_out_date=check_out_date)
        return {n: self.rooms[n] for n in self.rooms if self.rooms[n].available(check_in_date, check_out_date)}

    def book_room(self, room_number: int, customer: object, check_in_date: date, check_out_date: date) -> None:
        if self.get_hotel(self.city, self.name) is not self:
            raise ValueError("This hotel isn't in the database!")
        self.__test_inputs(number_of_rooms=room_number, customer=customer,
                           check_in_date=check_in_date, check_out_date=check_out_date)
        if room_number not in self.get_available_rooms(check_in_date, check_out_date):
            raise ValueError("This room isn't available from {} to {}!".format(check_in_date, check_out_date))
        Reservation(customer, self, self.get_room(room_number), check_in_date, check_out_date)

    def update_reservations(self, reservation, action) -> None:
        actions = [list.append, list.remove]
        if reservation.hotel is not self:
            raise ValueError("This reservation doesn't belong to this hotel!")
        if action not in actions:
            raise ValueError("Invalid action us passed!")
        if reservation in self.reservations and action is list.append:
            raise ValueError("This reservation already exists!")
        if reservation not in self.reservations and action is list.remove:
            raise ValueError("The reservation you're trying to delete doesn't exist!")
        action(self.reservations, reservation)
