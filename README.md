# Bus Ticket Booking System

## Overview

The **Bus Ticket Booking System** is a web-based application built using **Streamlit** that allows users to register, log in, select bus types, book seats, and generate bills. It includes an email confirmation system for registration and billing.

## Features

- **User Authentication**: Registration and login system with password hashing.
- **Bus Selection**: Choose between Government and Private buses.
- **AC/Non-AC Option**: Allows users to choose an AC or non-AC bus.
- **Seating Management**: Displays seating chart and allows seat booking.
- **Automated Billing**: Generates a bill with ticket price, GST, and total cost.
- **Email Notification**: Sends confirmation emails and bills to users.

## Technologies Used

- **Python**
- **Streamlit** (for web interface)
- **SQLite** (for user authentication database)
- **smtplib** & **EmailMessage** (for email notifications)
- **Hashlib** (for secure password hashing)

## Installation

### Prerequisites

Ensure you have Python installed on your system. You can install dependencies using:

```bash
pip install streamlit
```

### Running the Application

1. Clone the repository or download the script.
2. Run the following command:

```bash
streamlit run bus_booking_app.py
```

3. The application will open in your default web browser.

## Usage

1. **Login/Register**: New users must register before logging in.
2. **Select Destination**: Enter the destination city.
3. **Choose Bus Type**: Select Government or Private bus.
4. **Choose AC Option**: Select AC or Non-AC bus.
5. **Book Seats**: Choose and confirm seat selections.
6. **Generate Bill**: Get total cost breakdown and receive the bill via email.

## Database

The application uses SQLite to store user credentials in `user_credentials.db`.

## Security Considerations

- Passwords are hashed using SHA-256 before storing in the database.
- Email credentials should be stored securely using environment variables.

## Future Enhancements

- Online payment integration.
- Dynamic route and pricing management.
- Enhanced UI and seat selection.

## Contributors

Developed by **Kunjesh Shrimankar**

## License

This project is open-source and available for modification and enhancement.

