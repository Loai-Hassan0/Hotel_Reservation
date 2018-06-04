"""
tester.py
"""

from datetime import date
from customer import Customer
from hotel import Hotel, Room
import unittest


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.user = Customer("A", "B", "+123")
        self.user1 = Customer("mohamed", "Saleh", "+79613206083")
        self.user2 = Customer("Ahmed", "Eleslamboly", "89618305057")
        self.user3 = Customer("Mahmoud", "Ali", "89618305057")  # +201062479370
        self.user1.add_customer()
        self.user2.add_customer()

    def tearDown(self):
        Customer.customers.clear()

    def test_create_customer(self):
        #                       --<Incorrect Inputs>--
        self.assertRaises(TypeError, Customer, "Mohamed", "Saleh", 89613206083)
        self.assertRaises(TypeError, Customer, "Mohamed", 123, "89613206083")
        self.assertRaises(ValueError, Customer, "Mo7amed", "Saleh", "+201020899838")
        self.assertRaises(ValueError, Customer, "Mohamed", "Saleh", "2+01020899838")

    def test_add_customer(self):
        #                       --<Returned Values>--
        self.assertIsNone(self.user.add_customer(), msg="Adding a customer shouldn't return anything!")
        #                       --<Incorrect Inputs>--
        self.assertRaises(ValueError, self.user1.add_customer)
        self.assertRaises(ValueError, self.user3.add_customer)
        #                   --<Effect on the Database>--
        self.assertIn(self.user1.phone_number, Customer.customers, msg="User 1 wasn't added to the database!")
        self.assertIn(self.user2.phone_number, Customer.customers, msg="User 2 wasn't added to the database!")
        self.assertIs(Customer.customers[self.user2.phone_number], self.user2, msg="User 2 isn't assigned to its phone "
                                                                                   "number!")
        self.assertNotIn(self.user3, Customer.customers.values(), msg="Adding this customer should've failed!")
        self.assertIs(Customer.customers[self.user2.phone_number], self.user2, msg="After trying to add user 3, user 2 "
                                                                                   "is no longer assigned to its phone "
                                                                                   "number!")

    def test_get_customer(self):
        #                       --<Incorrect Inputs>--
        self.assertRaises(TypeError, Customer.get_customer, 89613206083)
        self.assertRaises(ValueError, Customer.get_customer, "Ahmed")
        self.assertRaises(ValueError, Customer.get_customer, "1+2")
        #                       --<Returned Values>--
        self.assertIs(Customer.get_customer(self.user1.phone_number), self.user1, msg="Didn't return User 1!")
        self.assertNotIsInstance(Customer.get_customer("+0123456789"), Customer, msg="Phone number shouldn't excise!")
        self.assertEqual(Customer.get_customer("89613206083"), {}, msg="Should return an empty dictionary!")

    def test_edit_customer(self):
        #                       --<Returned Values>--
        self.assertIsNone(self.user.edit_customer(), msg="Editing a customer shouldn't return anything!")
        #                       --<Incorrect Inputs>--
        self.assertRaises(TypeError, self.user1.edit_customer, phone_number=89613206083)
        self.assertRaises(ValueError, self.user1.edit_customer, age=32)
        self.assertRaises(ValueError, self.user2.edit_customer, first_name="A7med")
        self.assertRaises(ValueError, self.user2.edit_customer, phone_number=self.user1.phone_number)
        #                       --<Effect on the Database>--
        self.assertIs(Customer.get_customer(self.user1.phone_number), self.user1,msg="After trying to assign the "
                                                                                        "phone number of user 1 to user"
                                                                                        " 2, user 1 is no longer "
                                                                                        "assigned to its phone number!")
        #                       ============================
        self.user1.edit_customer(phone_number="+79613206083", last_name="ragaey", first_name="Mohammed")
        self.assertEqual(self.user1.first_name, "Mohammed", msg="First name incorrectly edited!")
        self.assertEqual(self.user1.last_name, "Ragaey", msg="Last name incorrectly edited!")
        self.assertEqual(self.user1.phone_number, "+79613206083", msg="Phone number incorrectly edited!")
        #                       ============================
        self.user3.edit_customer(phone_number=self.user1.phone_number)
        self.assertEqual(self.user3.phone_number, self.user1.phone_number, msg="Phone number not assigned even though "
                                                                               "user 3 isn't in the database!")
        #                       ============================
        self.user3.edit_customer(phone_number="+201062479370")
        self.assertEqual(self.user3.phone_number, "+201062479370", msg="Phone number incorrect after editing!")

    def test_delete_customer(self):
        #                       --<Returned Values>--
        self.assertIsNone(self.user1.delete_customer(), msg="Deleting a customer shouldn't return anything!")
        #                       -<Effect on the Database>-
        self.assertNotIn(self.user1.phone_number, Customer.customers, msg="User 1 was deleted so it shouldn't exist!")
        self.assertRaises(ValueError, self.user1.delete_customer)
        self.assertRaises(ValueError, self.user3.delete_customer)
        self.assertIn(self.user2.phone_number, Customer.customers, msg="User 2 should still be in the database!")
        self.assertIs(Customer.get_customer(self.user2.phone_number), self.user2, msg="Trying to delete user 1 while "
                                                                                      "having the same phone number as "
                                                                                      "user 2 effected user 2!")


class TestHotel(unittest.TestCase):
    def setUp(self):
        self.yolo = Hotel("YOLO", "Utopia", 13)
        self.tcu = Hotel("The Crack Up", "Laughter", 55)
        self.swit = Hotel("Swing It", "Laughter", 69)
        self.tcu_ = Hotel("The Crack Up", "Laughter", 24)
        self.yolo.add_hotel()
        self.tcu.add_hotel()

    def tearDown(self):
        Hotel.hotels.clear()

    def test_create_hotel(self):
        #                       --<Incorrect Inputs>--
        self.assertRaises(TypeError, Hotel, "Horizon", "Rio", 12.5)
        self.assertRaises(TypeError, Hotel, "Red Rose", 5, 12)
        self.assertRaises(ValueError, Hotel, "4 Seasons", "Cairo", -10)
        self.assertRaises(ValueError, Hotel, "Continental", "city"*13, 11)

    def test_add_hotel(self):
        #                       --<Returned Values>--
        self.assertIsNone(self.swit.add_hotel(), msg="Adding a hotel shouldn't return anything!")
        #                       --<Incorrect Inputs>--
        self.assertRaises(ValueError, self.yolo.add_hotel)
        self.assertRaises(ValueError, self.tcu_.add_hotel)
        #                       -<Effect on the Database>-
        self.assertIn(self.yolo.city, Hotel.hotels, msg="If the city doesn't exist where is the hotel then?!")
        self.assertIn(self.tcu.name, Hotel.hotels[self.tcu.city], msg="There's no hotel with that name in this city!")
        self.assertIs(self.yolo, Hotel.hotels[self.yolo.city][self.yolo.name], msg="The hotel is not the hotel!")
        self.assertNotIn(self.tcu_, Hotel.hotels[self.tcu_.city].values(), msg="Adding this hotel should've failed!")
        self.assertIs(self.tcu, Hotel.hotels[self.tcu.city][self.tcu.name], msg="Trying to add a hotel with the same"
                                                                                   " name and city messed thing up for"
                                                                                   " the original hotel!")

    def test_get_hotel(self):
        #                       --<Incorrect Inputs>--
        self.assertRaises(TypeError, Hotel.get_hotels_in_city, ["Delhi"])
        self.assertRaises(ValueError, Hotel.get_hotels_in_city, "Cairo" * 11)
        self.assertRaises(TypeError, Hotel.get_hotel, "Delhi", 17)
        self.assertRaises(ValueError, Hotel.get_hotel, "Madagascan", "Banana House" * 9)
        #                       --<Returned Values>--
        self.assertIs(Hotel.get_hotel(self.yolo.city, self.yolo.name), self.yolo, msg="YOLO isn't what we thought!")
        self.assertEqual(Hotel.get_hotel("Hesitance", self.yolo.name), {}, msg="Hesitance and YOLO don't go together!")
        self.assertEqual(Hotel.get_hotels_in_city("Mars"), {}, msg="Elon Musk hasn't made it to Mars yet!")
        self.assertIsInstance(Hotel.get_hotels_in_city(self.tcu.city), dict, msg="The hotels aren't stored in a "
                                                                                 "dictionary!")

    def test_edit_hotel(self):
        pass

    def test_delete_hotel(self):
        #                       --<Returned Values>--
        self.assertIsNone(self.yolo.delete_hotel(), msg="Deleting a hotel shouldn't return anything!")
        #                       --<Incorrect Inputs>--
        self.assertRaises(ValueError, self.yolo.delete_hotel)
        self.assertRaises(ValueError, self.tcu_.delete_hotel)
        #                       --<Effect on the Database>--
        self.assertNotIn(self.yolo.name, Hotel.get_hotels_in_city(self.yolo.city), msg="YOLO was deleted so it "
                                                                                       "shouldn't exist!")
        self.assertIn(self.tcu.name, Hotel.get_hotels_in_city(self.tcu.city), msg="Where did \"The Crack up\" go?!")
        self.assertIs(Hotel.get_hotel(self.tcu.city, self.tcu.name), self.tcu, msg="Who changed The Crack up?!")

    def test_get_room(self):
        #                       --<Incorrect Inputs>--
        self.assertRaises(TypeError, self.yolo.get_room, "Room11")
        self.assertRaises(ValueError, self.tcu.get_room, -11)
        self.assertRaises(TypeError, self.swit.get_available_rooms, date.today, date(2020, 1, 1))
        self.assertRaises(ValueError, self.tcu_.get_available_rooms, date(2020, 1, 1), date.today())
        #                       --<Returned Values>--
        self.assertEqual(self.swit.get_room(70), {}, msg="Who replace the empty dictionary?!")
        self.assertIsInstance(self.yolo.get_room(5), Room, msg="I asked for a room not a pizza!")
        self.assertIsInstance(self.tcu.get_available_rooms(date.today(), date(2020, 1, 1)), dict, msg="I want my order "
                                                                                                      "in a dictionary!")

    def test_book_room(self):
        user = Customer("Mohamed", "Saleh", "+79613203083")
        #                       --<Incorrect Inputs>--
        self.assertRaises(ValueError, self.tcu.book_room, 5, user, date.today(), date(2020, 1, 1))
        user.add_customer()
        self.assertRaises(ValueError, self.tcu_.book_room, 3, user, date.today(), date(2020, 1, 1))
        self.assertRaises(ValueError, self.swit.book_room, 7, user, date.today(), date(2020, 1, 1))
        self.swit.add_hotel()
        self.assertRaises(TypeError, self.yolo.book_room, "11", user, date.today(), date(2020, 1, 1))
        self.assertRaises(TypeError, self.swit.book_room, 13, user, (2019, 12, 21), date(2020, 1, 1))
        #                       --<Returned Values>--
        self.assertIsNone(self.yolo.book_room(1, user, date.today(), date(2020, 1, 1)), msg="Booking a room shouldn't "
                                                                                            "return anything!")


class TestReservation(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_reservation(self):
        pass

    def test_add_reservation(self):
        pass

    def test_get_customer(self):
        pass

    def test_edit_reservation(self):
        pass

    def test_delete_reservation(self):
        pass


if __name__ == "__main__":
    unittest.main()
