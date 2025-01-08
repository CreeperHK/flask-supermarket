# Disclaimer: 
This program is for academic use only. Please be responsible for any legal issues during use. In addition, some of the pictures in this program come from the Internet. 
This program is using Azure, AWS or Google Cloud may not suitable for this program.

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
   OR
   ```bash
   flask run --host=127.0.0.1 --port=8000
   ```

6. Open your web browser and navigate to `http://127.0.0.1:8000`, test with the local deploy in localhost

7. (optional)
   Follow steps 1-6 above to re-execute it in the VM, Configure with Nginx and Gunicorn yourself to run this program in the VM.

## Usage

- **Register**: Create a new user account.
- **Login**: Log in with your credentials.
- **Admin Panel**: Access the admin panel by logging in with a username ending in `-a`.
- **Manage Items**: Admins can add, edit, or delete items.
- **Place Orders**: Users can browse items and place orders.
- **View Orders**: Users can view their orders, and admins can view all orders.

## Need to know while testing
- Please make a Admin user account in MongoDB before do the testing.
- The admin page and normal user login page is the same.
- Login with the '<username>-a', the python will run on admin login. If the user does not in the admin database, the login will fail.
- Please make sure all module has been install properly, if the module missing, it may not showing error until you run on those part.
- Please run the whole program locally before putting it into Cloud platform.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!
