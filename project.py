"""
Bus Management System
A simple program to manage bus bookings, routes, and seat availability.
"""

import json
import os


# File to store bus data
DATA_FILE = "buses.json"


def load_buses():
    """
    Load bus data from buses.json file.
    Returns a dictionary with bus information, or empty dict if file doesn't exist.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}


def save_buses(buses):
    """
    Save bus data to buses.json file.
    Args:
        buses (dict): Dictionary containing all bus information
    """
    with open(DATA_FILE, "w") as file:
        json.dump(buses, file, indent=4)


def add_bus():
    """
    Add a new bus to the system.
    Validates that bus number is unique and seat count is positive.
    """
    buses = load_buses()
    
    # Get bus number input
    while True:
        try:
            bus_number = input("\nEnter bus number: ").strip()
            
            if not bus_number:
                print("Error: Bus number cannot be empty.")
                continue
                
            if bus_number in buses:
                print(f"Error: Bus number {bus_number} already exists.")
                continue
                
            break
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Get route input
    while True:
        try:
            route = input("Enter route (e.g., New York to Boston): ").strip()
            
            if not route:
                print("Error: Route cannot be empty.")
                continue
                
            break
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Get total seats input
    while True:
        try:
            total_seats = int(input("Enter total number of seats: ").strip())
            
            if total_seats <= 0:
                print("Error: Total seats must be a positive number.")
                continue
                
            break
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Add route to dictionary
    buses[bus_number] = {
        "route": route,
        "total_seats": total_seats,
        "available_seats": total_seats,
        "booked_tickets": 0
    }
    
    save_buses(buses)
    print(f"✓ Bus {bus_number} added successfully!")


def book_ticket():
    """
    Book a ticket for a passenger on a bus.
    Validates that the bus exists and seats are available.
    """
    buses = load_buses()
    
    if not buses:
        print("Error: No buses available in the system.")
        return
    
    # Get bus number input
    while True:
        try:
            bus_number = input("\nEnter bus number to book a ticket: ").strip()
            
            if bus_number not in buses:
                print("Error: Bus number not found.")
                continue
                
            break
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    bus = buses[bus_number]
    
    # Check if seats are available
    if bus["available_seats"] <= 0:
        print(f"Error: No available seats on bus {bus_number}.")
        return
    
    # Get number of tickets to book
    while True:
        try:
            num_tickets = int(input("Enter number of tickets to book: ").strip())
            
            if num_tickets <= 0:
                print("Error: Number of tickets must be positive.")
                continue
                
            if num_tickets > bus["available_seats"]:
                print(f"Error: Only {bus['available_seats']} seats available.")
                continue
                
            break
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Update bus information
    bus["available_seats"] -= num_tickets
    bus["booked_tickets"] += num_tickets
    
    save_buses(buses)
    print(f"✓ Successfully booked {num_tickets} ticket(s) on bus {bus_number}!")


def cancel_ticket():
    """
    Cancel tickets for a passenger on a bus.
    Validates that the bus exists and tickets have been booked.
    """
    buses = load_buses()
    
    if not buses:
        print("Error: No buses available in the system.")
        return
    
    # Get bus number input
    while True:
        try:
            bus_number = input("\nEnter bus number to cancel a ticket: ").strip()
            
            if bus_number not in buses:
                print("Error: Bus number not found.")
                continue
                
            break
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    bus = buses[bus_number]
    
    # Check if there are any booked tickets
    if bus["booked_tickets"] <= 0:
        print(f"Error: No booked tickets on bus {bus_number}.")
        return
    
    # Get number of tickets to cancel
    while True:
        try:
            num_tickets = int(input("Enter number of tickets to cancel: ").strip())
            
            if num_tickets <= 0:
                print("Error: Number of tickets must be positive.")
                continue
                
            if num_tickets > bus["booked_tickets"]:
                print(f"Error: Only {bus['booked_tickets']} tickets are booked.")
                continue
                
            break
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    # Update bus information
    bus["available_seats"] += num_tickets
    bus["booked_tickets"] -= num_tickets
    
    save_buses(buses)
    print(f"✓ Successfully cancelled {num_tickets} ticket(s) on bus {bus_number}!")


def delete_route():
    """
    Delete a route entry from the system.
    Validates that the bus exists before removing it.
    """
    buses = load_buses()

    if not buses:
        print("Error: No buses available in the system.")
        return

    while True:
        try:
            bus_number = input("\nEnter bus number to delete route: ").strip()

            if bus_number not in buses:
                print("Error: Bus number not found.")
                continue

            break
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return

    removed_route = buses[bus_number]["route"]
    del buses[bus_number]

    save_buses(buses)
    print(f"✓ Route '{removed_route}' removed successfully!")


def view_buses():
    """
    Display all buses with their details including route, total seats,
    available seats, and booked tickets.
    """
    buses = load_buses()
    
    if not buses:
        print("\nNo buses in the system.")
        return
    
    print("\n" + "=" * 80)
    print(f"{'Bus #':<10} {'Route':<30} {'Total':<8} {'Available':<12} {'Booked':<8}")
    print("=" * 80)
    
    for bus_number, bus_info in buses.items():
        print(f"{bus_number:<10} {bus_info['route']:<30} {bus_info['total_seats']:<8} "
              f"{bus_info['available_seats']:<12} {bus_info['booked_tickets']:<8}")
    
    print("=" * 80)


def main():
    """
    Main function to run the Bus Management System.
    Displays a menu and handles user interactions.
    """
    print("\n" + "=" * 50)
    print("  Welcome to Bus Management System")
    print("=" * 50)
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Add Route")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. Delete Route")
        print("5. View All Buses")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            add_bus()
        elif choice == "2":
            book_ticket()
        elif choice == "3":
            cancel_ticket()
        elif choice == "4":
            delete_route()
        elif choice == "5":
            view_buses()
        elif choice == "6":
            print("\n✓ Thank you for using Bus Management System. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
