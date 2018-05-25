from datetime import date
from reservation import *

database = Hotel_DB()
golden_hotel = Hotel("Golden", "Cairo", 50)

print(database.add_hotel(golden_hotel))
print(database.add_hotel("Galaxy", "Moscow", 100))
print(database.add_hotel("Galaxy", "Cairo", 150))
print("=" * 50)

print(golden_hotel.book_room(11, "Mohamed", date(2018, 5, 19), date(2018, 5, 23)))
print(golden_hotel.room(22).book("Ahmed", date(2018, 5, 18), date(2018, 5, 25)))
print(database.get_hotel("Cairo", "Golden").book_room(44, "Mahmud", date(2018, 6, 28), date(2018, 7, 3)))
print(database.get_hotel("Cairo", "Golden").book_room(44, "Karem", date(2018, 7, 1), date(2018, 7, 5)))
print("=" * 50)

print(golden_hotel.room(11).available(date(2018, 5, 23)))
print(golden_hotel.room(22).available(date(2018, 5, 7), date(2018, 5, 12)))
print(golden_hotel.room(44).available(date(2018, 6, 25), date(2018, 7, 1)))
print(golden_hotel.available_rooms())
print("=" * 50)

print(golden_hotel.room(25))
print("=" * 50)

print(database.in_city("Cairo"))
print("=" * 50)

print(database.in_city("Rostov"))
print("=" * 50)

print(database)
print("=" * 50)

print(database.available_rooms("Cairo", "Golden", detailed=True))
print(database.available_rooms("Moscow", "Golden"))
print("=" * 50)

print(database.booked_rooms("Cairo", "Golden"))

