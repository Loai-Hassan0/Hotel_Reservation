"""
customer.py
"""

import string


class Customer(object):
    new_id = 0
    customers = {}

    def __init__(self, first_name: str, last_name: str, phone_number: str) -> None:
        self.__test_inputs(first_name=first_name, last_name=last_name, phone_number=phone_number)
        self.id_number = "C_"
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.phone_number = phone_number
        self.reservations = []

    @staticmethod
    def __test_inputs(**kwargs) -> None:
        # "First name must be a string!"
        # "First name must only contain letters!"
        # "First name must be a string!"
        # "Last name must only contain letters!"
        # "Phone number must be a string!"
        # "Phone number must only contain digits!"
        inputs = {"first_name", "last_name", "phone_number"}
        if inputs.intersection(set(kwargs)) != set(kwargs):
            raise ValueError("{} aren't attributes of Customer!".format(list(set(kwargs).difference(inputs))))
        type_tests = dict(first_name=str, last_name=str, phone_number=str)
        for case in kwargs:
            if not isinstance(kwargs[case], type_tests[case]):
                raise TypeError("{} must be a {}!".format(case, type_tests[case]))

        value_tests = dict(first_name=lambda x: not all(y in string.ascii_letters for y in x),
                           last_name=lambda x: not all(y in string.ascii_letters for y in x),
                           phone_number=lambda x: not all([x[0] in "+0123456789"] + [y in "0123456789" for y in x[1:]]))
        for case in kwargs:
            if value_tests[case](kwargs[case]):
                raise ValueError("Incorrect input value for {}!".format(case))

    def add_customer(self) -> None:
        if self.get_customer(self.phone_number) is self:
            raise ValueError("This customer already exists!")
        if self.phone_number in self.customers:
            raise ValueError("The phone number is already used!")
        self.id_number += str(Customer.new_id)
        self.customers[self.phone_number] = self
        Customer.new_id += 1

    @classmethod
    def get_customer(cls, phone_number: str) -> object:
        cls.__test_inputs(phone_number=phone_number)
        return cls.customers.get(phone_number, {})

    def edit_customer(self, **kwargs) -> None:
        self.__test_inputs(**kwargs)
        self.first_name = kwargs.get("first_name", self.first_name).title()
        self.last_name = kwargs.get("last_name", self.last_name).title()
        new_phone_number = kwargs.get("phone_number", self.phone_number)
        if new_phone_number != self.phone_number:
            if self in self.customers.values():
                if self.customers.get(new_phone_number, self) is not self:
                    raise ValueError("This phone number is already used!")
                else:
                    del self.customers[self.phone_number]
                    self.phone_number = new_phone_number
                    self.customers[self.phone_number] = self
            else:
                self.phone_number = new_phone_number

    def delete_customer(self) -> None:
        if self.get_customer(self.phone_number) is not self:  # self.phone_number not in self.customers or
            raise ValueError("The customer you're trying to delete doesn't exist!")
        temp_reservations = self.reservations.copy()
        for reservation in temp_reservations:
            reservation.delete_reservation()
        del self.customers[self.phone_number]

    def update_reservations(self, reservation, action) -> None:
        actions = [list.append, list.remove]
        if reservation.customer is not self:
            raise ValueError("This reservation doesn't belong to this customer!")
        if action not in actions:
            raise ValueError("Invalid action us passed!")
        if reservation in self.reservations and action is list.append:
            raise ValueError("This reservation already exists!")
        if reservation not in self.reservations and action is list.remove:
            raise ValueError("The reservation you're trying to delete doesn't exist!")
        action(self.reservations, reservation)
