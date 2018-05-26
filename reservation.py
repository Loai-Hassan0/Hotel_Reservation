"""
reservation.py
"""


class Reservation(object):
    def __init__(self, guest, from_date, till_date=None):
        self.guest = guest
        self.start = from_date
        self.end = till_date

    def get_dates(self):
        return (self.start, self.end) if self.end else (self.start,)

    def confirm_reservation(self):
        # Sends a text message to the customer confirming there reservation
        pass

