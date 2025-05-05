
import unittest
from datetime import datetime
from HOTEL_MANAGEMENT import Hotel, Guest, StandardRoom, DeluxeRoom, Booking

class TestHotelManagementSystem(unittest.TestCase):

    def setUp(self):
        self.hotel = Hotel("Test Hotel")
        self.room1 = StandardRoom(101, 100)
        self.room2 = DeluxeRoom(102, 150)
        self.hotel.rooms = [self.room1, self.room2]
        self.guest = Guest("John Doe")

    def test_add_booking(self):
        check_in = "2025-05-01"
        check_out = "2025-05-05"
        booking = Booking(self.guest, self.room1, check_in, check_out)
        self.hotel.bookings.append(booking)

        self.assertEqual(len(self.hotel.bookings), 1)
        self.assertEqual(self.hotel.bookings[0].guest.name, "John Doe")
        self.assertEqual(self.hotel.bookings[0].room.room_number, 101)

    def test_room_unavailability(self):
        check_in = "2025-05-01"
        check_out = "2025-05-05"
        self.hotel.bookings.append(Booking(self.guest, self.room1, check_in, check_out))

        available = self.hotel.list_available_rooms_on_date_range(check_in, check_out)

        self.assertNotIn(self.room1, available)
        self.assertIn(self.room2, available)

    def test_cancel_booking(self):
        check_in = "2025-05-01"
        check_out = "2025-05-05"
        booking = Booking(self.guest, self.room1, check_in, check_out)
        self.hotel.bookings.append(booking)
        self.hotel.bookings.remove(booking)

        self.assertEqual(len(self.hotel.bookings), 0)

if __name__ == '__main__':
    unittest.main()
