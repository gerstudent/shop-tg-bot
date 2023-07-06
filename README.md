# Introduction

Repository contains the source code of the telegram bot for the store. The project was created in the educational
goals.

- Available functions: choice items from catalog, view contact information, add item to cart, admin panel with the ability to add, remove products and make a mailing list.

# Prerequisites

Be sure you have the following installed on your development machine:

1. Python >= 3.9
2. Git
3. pip
4. Virtualenv

# Setup

To run this project in your development machine, follow these steps:

1. (optional) Create and activate a [virtualenv](https://virtualenv.pypa.io/) or [venv](https://docs.python.org/3/library/venv.html)

2. Clone this repo

`git clone https://github.com/gerstudent/shop_tg_bot`

3. Install dependencies:

`pip install -r requirements.txt`

4. Create file `.env` and add there following variables:

- TOKEN - secret token from @botfather
- GROUP_ID - (Optional) ID of the group to which bot will redirect messages from user
- ADMIN_ID - admin user ID

5. Run bot.py file by running a command:

`python bot.py`