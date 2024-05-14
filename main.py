from models.data import consume

"""

Note: Need to create a file named .env with configuration variables.
Check models/settings.py for more information.

"""

if __name__ == "__main__":
    try:
        while True:
            consume()
    except KeyboardInterrupt:
        print('Exiting...')
        exit(3)
