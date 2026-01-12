# auction-project



[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-3.0+-green.svg)](https://www.djangoproject.com/)

A feature-rich eBay-like e-commerce auction site where users can post listings, place bids, comment on listings, and manage a watchlist.

##  Features
- **Listings:** Create, view, and close auction listings.
- **Bidding:** Real-time validation for bid amounts.
- **Watchlist:** Add/remove items to a personal watchlist.
- **Categories:** Filter listings by category.
- **Admin Interface:** Full control over users, listings, and comments.

##  Security Measures
To follow industry best practices, this project uses **environment variables** to manage sensitive data. The `SECRET_KEY` and `DEBUG` mode are handled via a `.env` file, which is excluded from version control for security.



##  Installation & Local Setup

### 1. Clone the repository
 ```bash
git clone [https://github.com/thoughts-cell/auction-project](https://github.com/thoughts-cell/auction-project)
cd commerce
 ```

### 2. Install Dependencies
 ```bash
pip install -r requirements.txt
 
```
(Note: Ensure python-dotenv is installed as it is required to read the configuration.)

### 3. Automatic Environment Configuration
I have included a helper script to make setup easier. Run the following command to automatically generate a secure SECRET_KEY and create your local .env file:
 
```bash
python setup_env.py
```
###  4. Database Setup
Apply the migrations to initialize the SQLite database:

 

python manage.py migrate
### 5. Start the Server

```Bash

python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.
```