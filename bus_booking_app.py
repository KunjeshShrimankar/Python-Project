import smtplib
import random
from email.message import EmailMessage
import sqlite3
import hashlib
import streamlit as st

# Database setup
def init_db():
    conn = sqlite3.connect('user_credentials.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password
def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

class BusTicketBooking:
    def __init__(self):
        init_db()  # Initialize the database
        self.NUM_ROWS = 15
        self.SEATS_PER_ROW = 6
        self.starting_point = "Ahmedabad"
        self.available_seats = [['O' for _ in range(self.SEATS_PER_ROW)] for _ in range(self.NUM_ROWS)]
        self.endpoint_prices = {"Bhavnagar": 100, "Rajkot": 200, "Himatnagar": 50, "Amreli": 150}

        # Initialize session state variables
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'email' not in st.session_state:
            st.session_state.email = None
        if 'confirmation_code' not in st.session_state:
            st.session_state.confirmation_code = None
        if 'endpoint' not in st.session_state:
            st.session_state.endpoint = None
        if 'is_ac_bus' not in st.session_state:
            st.session_state.is_ac_bus = False
        if 'is_private_bus' not in st.session_state:
            st.session_state.is_private_bus = True
        if 'bus_type_selected' not in st.session_state:
            st.session_state.bus_type_selected = False
        if 'num_seats' not in st.session_state:
            st.session_state.num_seats = 0
        if 'selected_seats' not in st.session_state:
            st.session_state.selected_seats = []

    def email_alert(self, subject, body, to):
        """
        Sends an email alert to the specified recipient.
        """
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        msg['from'] = "pythonbusbooking@gmail.com"

        user = "pythonbusbooking@gmail.com"
        password = "gotofipllhrmlnqz"  # Use environment variables for security

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)

    def send_confirmation_email(self):
        """
        Sends a confirmation email to the user's email address.
        """
        subject = "Bus Ticket Booking Confirmation Code"
        body = f"Thank you for registering with us!\nYour confirmation code is: {st.session_state.confirmation_code}"
        self.email_alert(subject, body, st.session_state.email)
        st.success(f"Confirmation email has been sent to {st.session_state.email}. Check your inbox.")

    def register(self):
        st.session_state.email = st.text_input("Enter your email address: ")
        username = st.text_input("Enter your username: ")
        password = st.text_input("Enter your password: ", type="password")
        if st.button("Register"):
            if self.check_user_exists(username, st.session_state.email):
                st.error("Username or email already exists. Please choose a different username or email.")
            else:
                hashed_password = hash_password(password)
                self.save_user_to_db(username, st.session_state.email, hashed_password)
                st.session_state.confirmation_code = str(random.randint(1000, 9999))
                self.send_confirmation_email()
                entered_code = st.text_input("Enter the confirmation code: ")
                if entered_code == st.session_state.confirmation_code:
                    st.success("Registration successful!")
                    st.session_state.logged_in = True
                else:
                    st.error("Invalid confirmation code. Registration failed.")

    def check_user_exists(self, username, email):
        """
        Checks if a user with the given username or email already exists in the database.
        """
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        user = c.fetchone()
        conn.close()
        return user is not None

    def save_user_to_db(self, username, email, password):
        """
        Saves a new user to the database.
        """
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()

    def login(self):
        st.sidebar.title("Login / Register")
        choice = st.sidebar.radio("Choose an option", ["Login", "Register"])
        if choice == "Login":
            username = st.sidebar.text_input("Enter your username: ")
            password = st.sidebar.text_input("Enter your password: ", type="password")
            if st.sidebar.button("Login"):
                user = self.get_user_from_db(username)
                if user and verify_password(user[3], password):
                    st.sidebar.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.email = user[2]  # Set the email for the logged-in user
                else:
                    st.sidebar.error("Invalid username or password. Please try again.")
        elif choice == "Register":
            self.register()

    def get_user_from_db(self, username):
        """
        Retrieves a user from the database by username.
        """
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        return user

    def select_bus_type(self):
        """
        Allows the user to select the type of bus.
        """
        st.subheader("Select the type of bus:")
        bus_type = st.radio("Choose bus type", ["Government Bus", "Private Bus"])
        if bus_type == "Government Bus":
            st.session_state.is_private_bus = False
        else:
            st.session_state.is_private_bus = True
        st.session_state.bus_type_selected = True

    def select_ac_type(self):
        st.subheader("Select the type of bus:")
        ac_type = st.radio("Choose AC type", ["AC Bus", "Non-AC Bus"])
        if ac_type == "AC Bus":
            st.session_state.is_ac_bus = True
        else:
            st.session_state.is_ac_bus = False

    def display_seating_chart(self):
        """
        Displays the seating chart.
        """
        st.subheader("Seating Chart:")
        st.write("   " + " ".join(str(i + 1) for i in range(self.SEATS_PER_ROW)))
        for i, row in enumerate(self.available_seats):
            st.write(f"{i + 1}  {' '.join(row)}")

    def book_seat(self, row, seat):
        if 1 <= row <= self.NUM_ROWS and 1 <= seat <= self.SEATS_PER_ROW:
            if self.available_seats[row - 1][seat - 1] == 'O':
                self.available_seats[row - 1][seat - 1] = 'X'  # Mark the seat as booked
                st.session_state.selected_seats.append((row, seat))
                st.success(f"Seat {seat} in row {row} booked successfully.")
            else:
                st.error("Sorry, the selected seat is already taken. Please choose another seat.")
        else:
            st.error("Invalid row or seat number.")

    def book_seats(self):
        st.session_state.num_seats = st.number_input(
            "Enter the number of seats you want to book: ",
            min_value=1,
            max_value=self.SEATS_PER_ROW,
            step=1,
            key="num_seats_input"  # Unique key for this widget
        )
        # Display the seating chart before booking seats
        self.display_seating_chart()

        for i in range(st.session_state.num_seats):
            row = st.number_input(
                f"Enter the row number for seat {i + 1} (1-{self.NUM_ROWS}): ",
                min_value=1,
                max_value=self.NUM_ROWS,
                step=1,
                key=f"row_input_{i}"  # Unique key for each row input
            )
            seat = st.number_input(
                f"Enter the seat number for seat {i + 1} (1-{self.SEATS_PER_ROW}): ",
                min_value=1,
                max_value=self.SEATS_PER_ROW,
                step=1,
                key=f"seat_input_{i}"  # Unique key for each seat input
            )
            if st.button(f"Book Seat {i + 1}", key=f"book_button_{i}"):  # Unique key for each button
                self.book_seat(row, seat)

        # Display the seating chart again after all seats are booked
        if len(st.session_state.selected_seats) == st.session_state.num_seats:
            st.subheader("Updated Seating Chart:")
            self.display_seating_chart()

    def generate_bill(self):
        st.subheader("*** BILL ***")
        st.write(f"Starting Point: {self.starting_point}")

        if st.session_state.endpoint not in self.endpoint_prices:
            st.error("Invalid destination. Please select a valid destination.")
            return

        st.write(f"Destination: {st.session_state.endpoint}")

        # Get the price for the destination
        endpoint_price = self.endpoint_prices[st.session_state.endpoint]

        # Apply a 10% price increase for AC buses
        if st.session_state.is_ac_bus:
            endpoint_price *= 1.10  # 10% price increase for AC buses

        # Calculate total price for each booked seat
        total_price = endpoint_price * st.session_state.num_seats

        st.write(f"Ticket Price to {st.session_state.endpoint}: ₹{endpoint_price:.2f}")
        st.write(f"Total Ticket Price: ₹{total_price:.2f}")

        # Determine GST rate based on bus type
        if st.session_state.is_private_bus:
            gst_rate = 0.18  # 18% GST for private buses
        else:
            gst_rate = 0.05  # 5% GST for government buses

        # Calculate GST amount
        gst_amount = total_price * gst_rate
        st.write(f"GST ({gst_rate * 100}%): ₹{gst_amount:.2f}")

        # Calculate total amount including GST
        total_with_gst = total_price + gst_amount
        st.write(f"Total Amount (including GST): ₹{total_with_gst:.2f}")

        # Send the bill details to the user's email
        subject = "Bus Ticket Booking Bill"
        body = f"Thank you for booking with us!\n\n*** BILL ***\nStarting Point: {self.starting_point}\nDestination: {st.session_state.endpoint}\nTicket Price to {st.session_state.endpoint}: ₹{endpoint_price:.2f}\nTotal Ticket Price: ₹{total_price:.2f}\nGST ({gst_rate * 100}%): ₹{gst_amount:.2f}\nTotal Amount (including GST): ₹{total_with_gst:.2f}"
        self.email_alert(subject, body, st.session_state.email)
        st.success(f"Bill details have been sent to {st.session_state.email}. Check your inbox.")

    def run_booking_system(self):
        st.title("Bus Ticket Booking System")
        if st.session_state.logged_in:
            st.sidebar.success(f"Logged in as {st.session_state.email}")
            if st.sidebar.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.email = None
                st.session_state.endpoint = None
                st.session_state.selected_seats = []
                st.success("Logged out successfully.")

            st.subheader("1. Select Destination")
            st.session_state.endpoint = st.text_input("Enter your destination: ")

            if st.session_state.endpoint:
                st.subheader("2. Select Bus Type")
                self.select_bus_type()

                if st.session_state.bus_type_selected:
                    st.subheader("3. Select AC Type")
                    self.select_ac_type()

                    st.subheader("4. Display Seating Chart and Book Seats")
                    self.book_seats()

                    st.subheader("5. Generate Bill")
                    if st.button("Generate Bill"):
                        self.generate_bill()
        else:
            st.warning("Please login to continue.")

if __name__ == "__main__":
    bus_booking = BusTicketBooking()
    bus_booking.login()
    bus_booking.run_booking_system()
