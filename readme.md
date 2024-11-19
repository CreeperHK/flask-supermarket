# Disclaimer: 
This program is not for commercial use. Please be responsible for any legal issues during use. In addition, some of the pictures in the program come from the Internet. If there are any copyright issues, please contact me immediately from the copyright owner. I will remove the relevant content immediately after receiving the message.

# Flask Supermarket Application

This is a Flask-based web application for managing a supermarket system. The application allows users to register, log in, view items, place orders, and for admins to manage items and orders.

## Features

- User registration and login
- Admin login for managing items and orders
- Item management (add, edit, delete)
- Order placement and management
- Filtering orders by state (Processing, Confirmed, Shipping, Completed)
- Session management for users and admins

## Technologies Used

- Python
- Flask
- Flask-PyMongo
- MongoDB
- HTML/CSS for front-end

## Requirements

- Python 3.x (The development version is 3.12.7)
- MongoDB (Atlas, Azure, or local installation)
- Flask
- Flask-PyMongo
- Werkzeug

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CreeperHK/flask-supermarket.git
   cd yourrepository
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MongoDB connection in the `app.py` file. Update the `connectType` variable to match your MongoDB setup (Atlas, Azure, or localhost) and provide the connection string.

5. Run the application:

   ```bash
   python app.py
   ```

6. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

- **Register**: Create a new user account.
- **Login**: Log in with your credentials.
- **Admin Panel**: Access the admin panel by logging in with a username ending in `-a`.
- **Manage Items**: Admins can add, edit, or delete items.
- **Place Orders**: Users can browse items and place orders.
- **View Orders**: Users can view their orders, and admins can view all orders.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!