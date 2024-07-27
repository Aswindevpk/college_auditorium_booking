# College Venue Booking System

This project is a web-based application for booking venues, managing bookings, and handling approvals. It features user roles such as users and administrators, with distinct functionalities for each.

## Features

- **User Login**: Multiple user roles with different functionalities.
- **Booking a Venue**: Check availability, book, postpone, or cancel bookings.
- **Booking History**: Access and manage booking history.
- **Admin Approval**: Multi-level booking approval process.

## User Guide

### User Login

1. Go to the [Venue Booking System Login Page](https://appus2023.pythonanywhere.com/login/)
2. Use the following credentials:

   **User1**:
   - Username: `CS`
   - Password: `pass@123`
   
   **User2**:
   - Username: `BCOM`
   - Password: `pass@123`

### Booking a Venue

1. **Select Date**: Choose the desired date and click submit.
2. **View Venues**: Available venues will be listed with color codes:
   - **Green**: Available
   - **Yellow**: Pending Booking
   - **Gray**: Booked
3. **Select Venue**: Choose the appropriate venue and fill out the booking form, selecting the needed slots.
4. **Submit Form**: Submit the form for admin approval.
5. **Check Status**: Monitor the booking status in the "Booking History" tab.

### Postponing a Booking

1. **Access Booking History**: Go to the "Booking History" tab and select the booking you need to postpone.
2. **Postpone Booking**: Click on "Postpone Booking."
3. **Select New Date & Venue**: Choose the new date and venue, then check availability.
4. **Preview**: Review the booking details and click "Preview."
5. **Submit**: Submit for admin approval. The booking will be tagged as "Postponed" in the booking history.

### Canceling a Booking

1. **Find Booking**: Locate the booking in the "Booking History."
2. **Cancel**: Click on "Cancel Booking." The booking will be canceled.

## Admin Guide

### Admin Login

1. Go to the [Admin Page](https://appus2023.pythonanywhere.com/booking-admin/)
2. Use the provided admin credentials.

### Approval Process

1. **Initial Review**: Administrator reviews and approves/rejects bookings.
2. **Final Approval**: Admin-approved bookings are then approved/rejected by the Principal.

### How to Approve/Reject a Booking

1. **Login**: Access the admin page.
2. **Review Bookings**: Recent bookings are displayed on the homepage.
3. **Decision**: Approve or reject the booking.
   - If rejecting, provide a reason for the rejection.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:

    ```sh
    git clone https://github.com/Aswindevpk/college_auditorium_booking.git
    ```

2. **Navigate to the project directory**:

    ```sh
    cd college_auditorium booking
    ```

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

    
4. **Migrations to Database**:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
    
5. **Create the Default Users.**:

    ```sh
    python manage.py create_default_users
    ```
6. **Loading initial data to Database**:

    ```sh
    python manage.py loaddata data.json
    ```

7. **Start the development server**:

    ```sh
    python manage.py runserver
    ```

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Django
- **Database**: PostgreSQL or SQLite (depending on your configuration)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---
