import random
import string
import socket


def random_string(lenght=10):
    return "".join([random.choice(string.ascii_letters) for _ in range(lenght)])


def random_phone():
    return "".join([random.choice(string.digits) for _ in range(10)])


def random_email():
    return random_string() + "@" + random_string(5) + "." + random.choice(["com", "ua", "org", "ru"])


def create_random_user(connection):
    """This user will have password test"""
    query = 'INSERT INTO `oc_customer` (`customer_id`, `customer_group_id`, `store_id`, `language_id`, `firstname`, `lastname`, `email`, `telephone`, `password`, `custom_field`, `newsletter`, `ip`, `status`, `safe`, `token`, `code`, `date_added`) VALUES (NULL, 1, 0, 1, %s, %s, %s, %s, %s, "", 0, %s, 1, 1, "", "", NOW());'
    email = random_email()
    password = "$2y$10$Ra9Adr9RCviSWdiwDTRXT.drmQE0A0P7z6aS5dcDXbPnf7tRSlNf." # test
    ip = socket.gethostbyname(socket.gethostname())
    connection.cursor().execute(query, (random_string(), random_string(), email, random_phone(), password, ip,))
    connection.commit()
    return email, "test"