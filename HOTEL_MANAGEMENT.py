
import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from typing import List
import csv
import os
from datetime import datetime

ROOMS_FILE = "rooms.csv"
BOOKINGS_FILE = "bookings.csv"

class Guest:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class Room(ABC):
    def __init__(self, room_number: int, price: float):
        self.room_number = room_number
        self.price = price

    @abstractmethod
    def room_type(self) -> str:
        pass

    def __str__(self):
        return f"{self.room_type()} Room {self.room_number} - ${self.price}"

class StandardRoom(Room):
    def room_type(self) -> str:
        return "Standard"

class DeluxeRoom(Room):
    def room_type(self) -> str:
        return "Deluxe"

class RoomFactory:
    @staticmethod
    def create_room(room_type: str, room_number: int, price: float) -> Room:
        if room_type == "Standard":
            return StandardRoom(room_number, price)
        elif room_type == "Deluxe":
            return DeluxeRoom(room_number, price)
        else:
            raise ValueError("Invalid room type")

class Booking:
    def __init__(self, guest: Guest, room: Room, check_in: str, check_out: str):
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out

    def __str__(self):
        return f"{self.guest} | Room {self.room.room_number} | {self.check_in} to {self.check_out}"

class Hotel:
    def __init__(self, name: str):
        self.name = name
        self.rooms: List[Room] = []
        self.bookings: List[Booking] = []

    def add_room(self, room: Room):
        self.rooms.append(room)
        self.save_rooms()

    
    def book_room(self, guest: Guest, room_type: str, check_in: str, check_out: str, requested_room_number: int = None) -> str:
        available_rooms = self.list_available_rooms_on_date_range(check_in, check_out)
        for room in available_rooms:
            if room.room_type() == room_type:
                if requested_room_number is None or room.room_number == requested_room_number:
                    booking = Booking(guest, room, check_in, check_out)
                    self.bookings.append(booking)
                    return f"Room {room.room_number} booked successfully for {guest.name}"
        return "No available rooms match the criteria"
    
        for room in self.list_available_rooms_on_date(check_in):
            if room.room_type() == room_type:
                booking = Booking(guest, room, check_in, check_out)
                self.bookings.append(booking)
                return f"Room {room.room_number} booked successfully for {guest.name}"
        return "No available rooms of requested type"

    def list_available_rooms_on_date(self, current_date_str: str):
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        unavailable_rooms = set()

        for booking in self.bookings:
            check_in = datetime.strptime(booking.check_in, "%Y-%m-%d")
            check_out = datetime.strptime(booking.check_out, "%Y-%m-%d")
            if check_in <= current_date <= check_out:
                unavailable_rooms.add(booking.room.room_number)

        return [room for room in self.rooms if room.room_number not in unavailable_rooms]

    
    def list_available_rooms_on_date_range(self, from_str: str, until_str: str):
        from_date = datetime.strptime(from_str, "%Y-%m-%d")
        until_date = datetime.strptime(until_str, "%Y-%m-%d")

        unavailable_rooms = set()
        for booking in self.bookings:
            check_in = datetime.strptime(booking.check_in, "%Y-%m-%d")
            check_out = datetime.strptime(booking.check_out, "%Y-%m-%d")
            if check_in <= until_date and check_out >= from_date:
                unavailable_rooms.add(booking.room.room_number)

        return [room for room in self.rooms if room.room_number not in unavailable_rooms]

    def export_bookings(self, filename=BOOKINGS_FILE):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Guest", "Room", "Type", "Price", "Check-in", "Check-out"])
            for booking in self.bookings:
                writer.writerow([
                    booking.guest.name,
                    booking.room.room_number,
                    booking.room.room_type(),
                    booking.room.price,
                    booking.check_in,
                    booking.check_out
                ])

    def save_rooms(self):
        with open(ROOMS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["room_number", "room_type", "price"])
            for room in self.rooms:
                writer.writerow([room.room_number, room.room_type(), room.price])


def load_bookings_from_csv(hotel, filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            guest = Guest(row["Guest"])
            room_number = int(row["Room"])
            matching_room = next((r for r in hotel.rooms if r.room_number == room_number), None)
            if matching_room:
                booking = Booking(guest, matching_room, row["Check-in"], row["Check-out"])
                hotel.bookings.append(booking)


def load_rooms_from_csv(filepath):
    rooms = []
    with open(filepath, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            room = RoomFactory.create_room(row["room_type"], int(row["room_number"]), float(row["price"]))
            rooms.append(room)
    return rooms

class HotelApp:
    def __init__(self, root, hotel: Hotel):
        self.hotel = hotel
        self.root = root
        self.root.title("Hotel Management System")
        self.setup_gui()

    def setup_gui(self):
        self.tabControl = ttk.Notebook(self.root)

        # Book Room tab
        self.tab_book = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_book, text='Book Room')

        ttk.Label(self.tab_book, text="Full Name:").grid(column=0, row=0)
        self.entry_name = ttk.Entry(self.tab_book)
        self.entry_name.grid(column=1, row=0)

        ttk.Label(self.tab_book, text="Room Type:").grid(column=0, row=1)
        self.combo_room_type = ttk.Combobox(self.tab_book, values=["Standard", "Deluxe"])
        self.combo_room_type.grid(column=1, row=1)
        self.combo_room_type.bind("<<ComboboxSelected>>", self.update_room_number_dropdown)

        ttk.Label(self.tab_book, text="Check-in (YYYY-MM-DD):").grid(column=0, row=2)
        self.entry_checkin = ttk.Entry(self.tab_book)
        self.entry_checkin.grid(column=1, row=2)

        ttk.Label(self.tab_book, text="Check-out (YYYY-MM-DD):").grid(column=0, row=3)
        ttk.Label(self.tab_book, text="Room Number (optional):").grid(column=0, row=4)
        self.combo_room_number = ttk.Combobox(self.tab_book)
        self.combo_room_number.grid(column=1, row=4)
        self.entry_checkout = ttk.Entry(self.tab_book)
        self.entry_checkout.grid(column=1, row=3)

        ttk.Button(self.tab_book, text="Book Room", command=self.book_room).grid(column=0, row=5, columnspan=2, pady=10)

        # View Available Rooms
        self.tab_view = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_view, text='Available Rooms')

        ttk.Label(self.tab_view, text="From (YYYY-MM-DD):").pack()
        self.entry_from = ttk.Entry(self.tab_view)
        self.entry_from.pack()

        ttk.Label(self.tab_view, text="Until (YYYY-MM-DD):").pack()
        self.entry_until = ttk.Entry(self.tab_view)
        self.entry_until.pack()

        self.rooms_listbox = tk.Listbox(self.tab_view, width=50)
        self.rooms_listbox.pack(pady=10)

        ttk.Button(self.tab_view, text="Refresh", command=self.update_rooms_list).pack()

        # Reservations Tab
        self.tab_reservations = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_reservations, text='All Reservations')
        self.reservation_listbox = tk.Listbox(self.tab_reservations, width=80)
        self.reservation_listbox.pack(pady=10)
        ttk.Button(self.tab_reservations, text="Refresh", command=self.update_reservations).pack()

        ttk.Button(self.tab_reservations, text="Cancel Selected", command=self.cancel_selected_reservation).pack()


    # Add Room
        self.tab_add = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_add, text='Add Room')

        ttk.Label(self.tab_add, text="Room Number:").grid(column=0, row=0)
        self.entry_room_number = ttk.Entry(self.tab_add)
        self.entry_room_number.grid(column=1, row=0)

        ttk.Label(self.tab_add, text="Room Type:").grid(column=0, row=1)
        self.combo_new_room_type = ttk.Combobox(self.tab_add, values=["Standard", "Deluxe"])
        self.combo_new_room_type.grid(column=1, row=1)

        ttk.Label(self.tab_add, text="Price:").grid(column=0, row=2)
        self.entry_price = ttk.Entry(self.tab_add)
        self.entry_price.grid(column=1, row=2)

        ttk.Button(self.tab_add, text="Add Room", command=self.add_room).grid(column=0, row=3, columnspan=2, pady=10)

        self.tabControl.pack(expand=1, fill="both")

    
    def book_room(self):
        name = self.entry_name.get()
        room_type = self.combo_room_type.get()
        check_in = self.entry_checkin.get()
        check_out = self.entry_checkout.get()
        room_number_str = self.combo_room_number.get().strip()

        if not name or not room_type or not check_in or not check_out:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must be in YYYY-MM-DD format.")
            return

        try:
            room_number = int(room_number_str) if room_number_str else None
        except ValueError:
            messagebox.showerror("Input Error", "Room number must be an integer.")
            return

        guest = Guest(name)
        message = self.hotel.book_room(guest, room_type, check_in, check_out, room_number)
    
        self.hotel.export_bookings()
        messagebox.showinfo("Booking Result", message)
        self.update_rooms_list()

    
    
    def update_rooms_list(self):
        from_str = self.entry_from.get()
        until_str = self.entry_until.get()

        if not from_str:
            from_str = datetime.now().strftime("%Y-%m-%d")
        if not until_str:
            until_str = from_str

        try:
            from_date = datetime.strptime(from_str, "%Y-%m-%d")
            until_date = datetime.strptime(until_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format.")
            return

        self.rooms_listbox.delete(0, tk.END)

        unavailable_rooms = set()
        for booking in self.hotel.bookings:
            check_in = datetime.strptime(booking.check_in, "%Y-%m-%d")
            check_out = datetime.strptime(booking.check_out, "%Y-%m-%d")
            if check_in <= until_date and check_out >= from_date:
                unavailable_rooms.add(booking.room.room_number)

        available_rooms = [room for room in self.hotel.rooms if room.room_number not in unavailable_rooms]
        if not available_rooms:
            self.rooms_listbox.insert(tk.END, "No rooms available.")
        else:
            for room in available_rooms:
                self.rooms_listbox.insert(tk.END, str(room))

    def update_reservations(self):
        self.reservation_listbox.delete(0, tk.END)
        for booking in self.hotel.bookings:
            self.reservation_listbox.insert(tk.END, str(booking))
    
    def update_room_number_dropdown(self, event=None):
        room_type = self.combo_room_type.get()
        check_in = self.entry_checkin.get()
        check_out = self.entry_checkout.get()
        if not room_type:
            return
        if not check_in:
            check_in = datetime.now().strftime("%Y-%m-%d")
        if not check_out:
            check_out = check_in
        try:
            available_rooms = self.hotel.list_available_rooms_on_date_range(check_in, check_out)
            filtered = [str(r.room_number) for r in available_rooms if r.room_type() == room_type]
            self.combo_room_number['values'] = filtered
        except Exception:
            self.combo_room_number['values'] = []


    def cancel_selected_reservation(self):
        selected_index = self.reservation_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a reservation to cancel.")
            return
        idx = selected_index[0]
        del self.hotel.bookings[idx]
        self.hotel.export_bookings()
        self.update_reservations()
        self.update_rooms_list()

    def add_room(self):
        try:
            room_number = int(self.entry_room_number.get())
            room_type = self.combo_new_room_type.get()
            price = float(self.entry_price.get())
        except ValueError:
            messagebox.showerror("Input Error", "Room number must be int, price must be float.")
            return

        room = RoomFactory.create_room(room_type, room_number, price)
        self.hotel.add_room(room)
        messagebox.showinfo("Success", f"Room {room_number} added.")
        self.entry_room_number.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.update_rooms_list()

# Setup & Run
if not os.path.exists(ROOMS_FILE):
    with open(ROOMS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["room_number", "room_type", "price"])


hotel = Hotel("Hotel")
rooms = load_rooms_from_csv(ROOMS_FILE)
for room in rooms:
    hotel.add_room(room)

load_bookings_from_csv(hotel, BOOKINGS_FILE)

root = tk.Tk()
app = HotelApp(root, hotel)
root.mainloop()
