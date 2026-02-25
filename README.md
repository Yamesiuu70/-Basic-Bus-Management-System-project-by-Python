# Bus Management System

## Project Description

The Bus Management System is a Python-based console application designed to manage bus transportation operations efficiently. This project allows users to add new buses to the system, book passenger tickets, cancel bookings, and view detailed information about all buses including their routes, seating capacity, and availability. The system uses persistent data storage through JSON files to ensure that all bus information and booking data is saved and can be retrieved between program sessions.

This project demonstrates core programming concepts including data persistence, user input validation, menu-driven interfaces, and JSON file handling. It is designed to be beginner-friendly while maintaining professional coding standards with clear variable names, comprehensive comments, and proper error handling.

## Video Demo

**Demo URL:** https://youtube.com/your_video_link_here

## Core Features

### 1. **Add Bus Function**
The `add_bus()` function allows administrators to add new buses to the system. When adding a bus, users must provide:
- **Bus Number:** A unique identifier for each bus (validates that duplicates cannot be added)
- **Route:** The travel route/destination (e.g., "New York to Boston")
- **Total Seats:** The seating capacity of the bus (must be a positive integer)

The function validates all inputs and prevents duplicate bus numbers from being added to the system. Once a bus is successfully added, it is immediately saved to the `buses.json` file.

### 2. **Book Ticket Function**
The `book_ticket()` function enables passengers to reserve seats on available buses. The function:
- Verifies that the bus exists in the system
- Checks if seats are available before allowing booking
- Accepts the number of tickets to book
- Prevents overbooking (validates that requested tickets don't exceed available seats)
- Decrements the available seat count
- Increments the booked tickets count
- Throws an error if no seats are available

This function ensures data integrity by validating all conditions before modifying the bus data.

### 3. **Cancel Ticket Function**
The `cancel_ticket()` function allows passengers to cancel their reservations. The function:
- Verifies that the bus exists
- Checks if there are any booked tickets to cancel (prevents cancelling when no bookings exist)
- Accepts the number of tickets to cancel
- Prevents invalid cancellations (validates that cancelled tickets don't exceed booked tickets)
- Increments the available seat count
- Decrements the booked tickets count

### 4. **View Buses Function**
The `view_buses()` function displays all buses in a formatted table showing:
- Bus number
- Route information
- Total seat capacity
- Available seats
- Number of booked tickets

This provides users with a complete overview of the fleet status and availability at any time.

### 5. **Data Persistence with buses.json**
The `buses.json` file serves as the persistent data storage for the Bus Management System. This JSON file stores all bus information in a structured format:

```json
{
    "BUS001": {
        "route": "New York to Boston",
        "total_seats": 50,
        "available_seats": 48,
        "booked_tickets": 2
    },
    "BUS002": {
        "route": "Boston to Philadelphia",
        "total_seats": 40,
        "available_seats": 35,
        "booked_tickets": 5
    }
}
```

The `load_buses()` function reads this file at the start of operations or when needed, while the `save_buses()` function writes updated information back to the file after any modifications. This ensures that all data persists even after the program is closed.

### 6. **Menu-Driven Interface**
The `main()` function provides an interactive menu that displays the following options:
1. Add Bus - Create a new bus entry
2. Book Ticket - Reserve seats on a bus
3. Cancel Ticket - Remove a reservation
4. View All Buses - Display fleet information
5. Exit - Close the application

Users can navigate through the menu by entering numbers 1-5, making the system intuitive and user-friendly.

## Input Validation Features

The system includes comprehensive input validation to ensure data quality:
- **Empty Input Prevention:** All text inputs are trimmed and validated to ensure they are not empty
- **Duplicate Bus Number Prevention:** The system checks for existing bus numbers before adding new ones
- **Positive Integer Validation:** Seat counts and ticket numbers are validated as positive integers
- **Seat Availability Checks:** The system prevents booking when no seats are available
- **Booking Status Verification:** The system prevents cancelling tickets when none have been booked
- **Overbooking Prevention:** Validates that booking/cancellation quantities don't exceed available/booked counts

## Testing with pytest

The project includes a comprehensive test suite in `test_project.py` that covers all major functionality using the pytest framework. The test suite includes:

### **TestDataPersistence Class**
- `test_load_buses_empty_system()` - Verifies that loading from a non-existent file returns an empty dictionary
- `test_save_and_load_buses()` - Ensures that saved bus data can be correctly loaded back

### **TestAddBus Class**
- `test_add_bus_success()` - Validates successful bus addition with correct data initialization
- `test_add_duplicate_bus_number()` - Ensures duplicate bus numbers are rejected
- `test_add_multiple_buses()` - Verifies that multiple buses can be added sequentially

### **TestBookTicket Class**
- `test_book_ticket_success()` - Tests successful ticket booking and seat/booking count updates
- `test_book_ticket_all_seats()` - Validates booking when all available seats are booked
- `test_book_ticket_no_availability()` - Ensures booking fails with zero available seats
- `test_book_exceed_available_seats()` - Prevents overbooking attempts

### **TestCancelTicket Class**
- `test_cancel_ticket_success()` - Validates successful ticket cancellation
- `test_cancel_all_tickets()` - Tests cancelling the entire booking allocation
- `test_cancel_no_booked_tickets()` - Prevents cancellation when no tickets are booked

### **TestIntegration Class**
- `test_complete_workflow()` - Integration test covering add, book, and cancel operations in sequence

To run the tests, execute: `pytest test_project.py -v`

## Installation and Usage

### Requirements
- Python 3.10 or higher
- pytest (for running tests)

### Setup Instructions
1. Navigate to the project directory
2. Install pytest: `pip install -r requirements.txt`
3. Run the application: `python project.py`
4. Follow the on-screen menu prompts

### Running Tests
```bash
pytest test_project.py -v
```

## Technical Highlights

- **Modular Design:** Functions are separate and focused on single responsibilities
- **Error Handling:** Comprehensive try-except blocks handle user input errors gracefully
- **JSON Persistence:** All data automatically persists between sessions
- **Type Safety:** Functions validate input types before processing
- **Documentation:** Comprehensive docstrings explain purpose and parameters
- **Code Quality:** Clear variable names and inline comments enhance readability

## Author Notes

This project was designed as a practical demonstration of fundamental Python programming concepts including function design, file I/O, data validation, and test-driven development. The modular structure and comprehensive comments make it an excellent reference for beginners learning Python programming principles.
