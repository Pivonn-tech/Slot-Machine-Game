# Slot Machine Game

## Description
This is a simple slot machine game built with Flask, SQLAlchemy, and Flask-Bcrypt. Users can register, log in, deposit money, and spin the slot machine to try their luck.

## Features
- User registration and login
- Secure password storage with Flask-Bcrypt
- Deposit money into the user's account
- Spin the slot machine and win or lose money based on the outcome
- Track transactions (deposits, bets, wins, losses)

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/slot-machine-game.git
    cd slot-machine-game
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Set up the database:**
    ```sh
    flask shell
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

6. **Run the application:**
    ```sh
    flask run
    ```

## Usage

1. **Register an account:**
    - Navigate to `http://127.0.0.1:5000/register` and fill out the registration form.

2. **Log in:**
    - Navigate to `http://127.0.0.1:5000/login` and enter your credentials.

3. **Deposit money:**
    - After logging in, go to the deposit page and add money to your account.

4. **Spin the slot machine:**
    - Once you have money in your account, you can spin the slot machine and try your luck.

## Directory Structure
slot-machine-game/ │ 
├── app.py                # Main application file 
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates │  
├── home.html │   
├── login.html │   
├── register.html │   
├── spin.html │   
├── deposit.html │   
└── welcome.html
└── static/               # Static files (CSS, JS, images) 
├── css/ 
└── js/
## Contributing
If you would like to contribute to this project, please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
