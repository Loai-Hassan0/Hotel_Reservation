"""
app.py
"""

from customer import Customer
from datetime import date
from hotel import Hotel, Room
from reservation import Reservation
import random


def start_app():
    hotels = ["Best Western", "Hilton", "Hyatt", "InterContinental", "Radisson", "Sheraton", "Westin"]
    cities = ["New York", "Dubai", "Cairo", "Moscow", "Paris", "London", "Tokyo"]
    names = ["Mohamed", "Ahmed", "Mahoud", "Sad", "Ali", "Kaream", "Hussein", "Omar", "Hazem", "Ibrahim"]
    i = 0
    while i < 25:
        try:
            user = Customer(random.choice(names), random.choice(names),
                            "".join(str(random.randint(0, 9)) for _ in range(10)))
            hotel = Hotel(random.choice(hotels), random.choice(cities), random.randint(50, 100))
            user.add_customer()
            hotel.add_hotel()
            i += 1
        except ValueError:
            pass

    for number in Customer.customers:
        user = Customer.get_customer(number)
        print("{} {}: {}".format(user.first_name, user.last_name, user.phone_number))
        print("=" * 100)

    for city in Hotel.hotels:
        print("="*100)
        print("{}:".format(city))
        print(list(Hotel.get_hotels_in_city(city).keys()))

start_app()
