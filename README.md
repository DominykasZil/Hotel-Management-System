# Hotel Management System

## Introduction
This is a simple hotel management system developed using Python. The system allows users to book rooms, view available rooms, and manage reservations. The system is designed with **Object-Oriented Programming (OOP)** principles, ensuring scalability and maintainability. Data is stored in **CSV files** to maintain persistence.

Key Features:
- **Room Booking**: Allows guests to book rooms with check-in and check-out dates.
- **Room Availability**: Allows staff to view available rooms for a given date range.
- **Reservation Cancellation**: Enables guests or staff to cancel reservations.
- **Persistence**: Room and booking data is saved in and loaded from CSV files.

Technologies Used:
- Python 3.x
- **Tkinter** for GUI
- **unittest** for unit testing
- **CSV** for data persistence

## Functional Requirements

### OOP Principles:
- **Encapsulation**: The `Room`, `Guest`, and `Booking` classes encapsulate their respective data. Methods like `book_room()` and `cancel_booking()` modify internal data while keeping implementation hidden.
- **Inheritance**: The `StandardRoom` and `DeluxeRoom` classes inherit from the abstract `Room` class, allowing for shared functionality while specializing for different room types.
- **Polymorphism**: The `room_type()` method is overridden in the `StandardRoom` and `DeluxeRoom` subclasses to return specific room types.
- **Abstraction**: The `Room` class is abstract, requiring subclasses to implement room-specific behavior, such as returning the room type.

### Design Pattern:
- **Factory Design Pattern**: The Factory pattern is used to create rooms. It allows easy extension of new room types in the future without changing the existing code. For instance, creating a new room type like `SuiteRoom` can be done by adding a new class without modifying the core logic of the booking system.

### CSV Operations:
- The system reads and writes room and booking data from **CSV files**:
  - `rooms.csv`: Stores the room number, type, and price.
  - `bookings.csv`: Stores guest names, room numbers, check-in, and check-out dates.
  The `load_bookings()` and `save_bookings()` methods handle loading and saving this data to ensure persistence across sessions.

## Testing
To ensure the reliability of the system, **unit tests** were created using Python’s `unittest` framework. The following functionalities were tested:
- **Room Booking**: A test checks if a room can be successfully booked by a guest and if the booking is saved correctly.
- **Room Availability**: A test checks if rooms are correctly marked as unavailable when already booked during a given date range.
- **Canceling a Reservation**: A test checks if a reservation can be canceled correctly and removed from the system.
- **CSV Persistence**: Tests were also written to ensure that room and booking data is correctly saved and loaded from CSV files. These tests validate the integrity of data persistence.

The tests were executed in a **clean environment** to ensure no side effects between test runs.

## Results and Conclusions

The Hotel Management System was successfully developed and meets the functional requirements. The system supports:
- Room bookings with date validation.
- Checking room availability based on date ranges.
- Canceling reservations and updating the system accordingly.
- Persistence of room and booking data via CSV files.
