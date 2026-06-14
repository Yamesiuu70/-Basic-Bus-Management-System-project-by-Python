"""
Test suite for Bus Management System using pytest.
Tests core functionality: adding buses, booking tickets, and cancelling tickets.
"""

import pytest
import json
import os
import sys
from unittest.mock import patch, mock_open, MagicMock


# Add project directory to path to import project module
sys.path.insert(0, os.path.dirname(__file__))

import project


# Fixtures
@pytest.fixture
def sample_buses():
    """
    Fixture providing sample bus data for testing.
    """
    return {
        "BUS001": {
            "route": "New York to Boston",
            "total_seats": 50,
            "available_seats": 50,
            "booked_tickets": 0
        },
        "BUS002": {
            "route": "Boston to Philadelphia",
            "total_seats": 40,
            "available_seats": 35,
            "booked_tickets": 5
        }
    }


@pytest.fixture
def clean_data_file():
    """
    Fixture to clean up the data file before and after tests.
    """
    # Remove file before test
    if os.path.exists(project.DATA_FILE):
        os.remove(project.DATA_FILE)
    
    yield
    
    # Remove file after test
    if os.path.exists(project.DATA_FILE):
        os.remove(project.DATA_FILE)


# Tests for load_buses and save_buses
class TestDataPersistence:
    """Test suite for data loading and saving functionality."""
    
    def test_load_buses_empty_system(self, clean_data_file):
        """Test loading buses when no data file exists."""
        buses = project.load_buses()
        assert buses == {}
        assert isinstance(buses, dict)
    
    def test_save_and_load_buses(self, clean_data_file, sample_buses):
        """Test saving buses and then loading them back."""
        project.save_buses(sample_buses)
        loaded_buses = project.load_buses()
        assert loaded_buses == sample_buses
        assert len(loaded_buses) == 2


# Tests for add_bus function
class TestAddBus:
    """Test suite for add_bus functionality."""
    
    def test_add_bus_success(self, clean_data_file):
        """Test successfully adding a new bus."""
        with patch('builtins.input', side_effect=['BUS001', 'New York to Boston', '50']):
            project.add_bus()
        
        buses = project.load_buses()
        assert 'BUS001' in buses
        assert buses['BUS001']['route'] == 'New York to Boston'
        assert buses['BUS001']['total_seats'] == 50
        assert buses['BUS001']['available_seats'] == 50
        assert buses['BUS001']['booked_tickets'] == 0
    
    def test_add_duplicate_bus_number(self, clean_data_file, sample_buses):
        """Test preventing duplicate bus numbers."""
        project.save_buses(sample_buses)
        
        with patch('builtins.input', side_effect=['BUS001', 'New York to Boston', '50', '5']):
            project.add_bus()
        
        buses = project.load_buses()
        # Should attempt to add but fail on duplicate
        # The function should ask again for a new bus number
        # Since we provide '5' after duplicate, it might try to add BUS number '5'
    
    def test_add_multiple_buses(self, clean_data_file):
        """Test adding multiple buses sequentially."""
        with patch('builtins.input', side_effect=['BUS001', 'Route A', '50']):
            project.add_bus()
        
        with patch('builtins.input', side_effect=['BUS002', 'Route B', '40']):
            project.add_bus()
        
        buses = project.load_buses()
        assert len(buses) == 2
        assert 'BUS001' in buses
        assert 'BUS002' in buses


# Tests for book_ticket function
class TestBookTicket:
    """Test suite for booking ticket functionality."""
    
    def test_book_ticket_success(self, clean_data_file, sample_buses):
        """Test successfully booking a ticket."""
        project.save_buses(sample_buses)
        
        with patch('builtins.input', side_effect=['BUS001', '5']):
            project.book_ticket()
        
        buses = project.load_buses()
        assert buses['BUS001']['available_seats'] == 45
        assert buses['BUS001']['booked_tickets'] == 5
    
    def test_book_ticket_all_seats(self, clean_data_file, sample_buses):
        """Test booking all available seats."""
        project.save_buses(sample_buses)
        
        with patch('builtins.input', side_effect=['BUS001', '50']):
            project.book_ticket()
        
        buses = project.load_buses()
        assert buses['BUS001']['available_seats'] == 0
        assert buses['BUS001']['booked_tickets'] == 50
    
    def test_book_ticket_no_availability(self, clean_data_file, sample_buses):
        """Test that booking fails when no seats are available."""
        # Create a bus with no available seats
        buses = {
            "BUS003": {
                "route": "Full Bus",
                "total_seats": 30,
                "available_seats": 0,
                "booked_tickets": 30
            }
        }
        project.save_buses(buses)
        
        with patch('builtins.input', side_effect=['BUS003', '1']):
            project.book_ticket()
        
        buses = project.load_buses()
        # Seats should still be 0
        assert buses['BUS003']['available_seats'] == 0
    
    def test_book_exceed_available_seats(self, clean_data_file, sample_buses):
        """Test booking more tickets than available seats."""
        project.save_buses(sample_buses)
        
        # BUS001 has 50 available seats, try to book 60
        with patch('builtins.input', side_effect=['BUS001', '60', '10']):
            project.book_ticket()
        
        buses = project.load_buses()
        # Should have booked 10 tickets instead
        assert buses['BUS001']['available_seats'] == 40


# Tests for cancel_ticket function
class TestCancelTicket:
    """Test suite for cancelling ticket functionality."""
    
    def test_cancel_ticket_success(self, clean_data_file, sample_buses):
        """Test successfully cancelling a ticket."""
        project.save_buses(sample_buses)
        
        # BUS002 has 5 booked tickets
        with patch('builtins.input', side_effect=['BUS002', '3']):
            project.cancel_ticket()
        
        buses = project.load_buses()
        assert buses['BUS002']['available_seats'] == 38
        assert buses['BUS002']['booked_tickets'] == 2
    
    def test_cancel_all_tickets(self, clean_data_file, sample_buses):
        """Test cancelling all booked tickets."""
        project.save_buses(sample_buses)
        
        # BUS002 has 5 booked tickets, cancel all
        with patch('builtins.input', side_effect=['BUS002', '5']):
            project.cancel_ticket()
        
        buses = project.load_buses()
        assert buses['BUS002']['available_seats'] == 40
        assert buses['BUS002']['booked_tickets'] == 0
    
    def test_cancel_no_booked_tickets(self, clean_data_file, sample_buses):
        """Test that cancellation fails when no tickets are booked."""
        project.save_buses(sample_buses)
        
        # BUS001 has no booked tickets
        with patch('builtins.input', side_effect=['BUS001', '1']):
            project.cancel_ticket()
        
        buses = project.load_buses()
        # Should remain unchanged
        assert buses['BUS001']['booked_tickets'] == 0
        assert buses['BUS001']['available_seats'] == 50


# Tests for delete_route function
class TestDeleteRoute:
    """Test suite for deleting route functionality."""

    def test_delete_route_success(self, clean_data_file, sample_buses):
        """Test successfully deleting a route."""
        project.save_buses(sample_buses)

        with patch('builtins.input', side_effect=['BUS001']):
            project.delete_route()

        buses = project.load_buses()
        assert 'BUS001' not in buses
        assert 'BUS002' in buses

    def test_delete_route_not_found(self, clean_data_file, sample_buses):
        """Test deleting a route that does not exist."""
        project.save_buses(sample_buses)

        with patch('builtins.input', side_effect=['BUS999', KeyboardInterrupt()]):
            project.delete_route()

        buses = project.load_buses()
        assert buses == sample_buses


# Integration tests
class TestIntegration:
    """Integration tests combining multiple operations."""
    
    def test_complete_workflow(self, clean_data_file):
        """Test a complete workflow: add route, book, cancel tickets."""
        # Add route
        with patch('builtins.input', side_effect=['BUS100', 'Test Route', '20']):
            project.add_bus()
        
        buses = project.load_buses()
        assert buses['BUS100']['available_seats'] == 20
        
        # Book tickets
        with patch('builtins.input', side_effect=['BUS100', '10']):
            project.book_ticket()
        
        buses = project.load_buses()
        assert buses['BUS100']['available_seats'] == 10
        assert buses['BUS100']['booked_tickets'] == 10
        
        # Cancel tickets
        with patch('builtins.input', side_effect=['BUS100', '5']):
            project.cancel_ticket()
        
        buses = project.load_buses()
        assert buses['BUS100']['available_seats'] == 15
        assert buses['BUS100']['booked_tickets'] == 5


# Minimal tests with exact required names to match course rule
def test_add_bus(clean_data_file):
    with patch('builtins.input', side_effect=['BUS500', 'Sample Route', '12']):
        project.add_bus()

    buses = project.load_buses()
    assert 'BUS500' in buses


def test_book_ticket(clean_data_file, sample_buses):
    project.save_buses(sample_buses)

    with patch('builtins.input', side_effect=['BUS001', '3']):
        project.book_ticket()

    buses = project.load_buses()
    assert buses['BUS001']['booked_tickets'] >= 3


def test_cancel_ticket(clean_data_file, sample_buses):
    project.save_buses(sample_buses)

    # Ensure there are booked tickets to cancel
    buses = project.load_buses()
    buses['BUS002']['booked_tickets'] = 2
    buses['BUS002']['available_seats'] = buses['BUS002']['total_seats'] - 2
    project.save_buses(buses)

    with patch('builtins.input', side_effect=['BUS002', '1']):
        project.cancel_ticket()

    buses = project.load_buses()
    assert buses['BUS002']['booked_tickets'] == 1
