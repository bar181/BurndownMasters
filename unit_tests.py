import unittest
import re

# code source for email vailidation function from chatgpt prompt: in python check if email is formatted okay

# password validation rules
MIN_PASSWORD = 6
MAX_PASSWORD = 12
UPPERCASE = True
LOWERCASE = True


def return_known_user():
    good = {}  # Create an empty dictionary
    good['email'] = 'me@ivyguide.edu'
    good['password'] = 'notSoSecret1!'
    good['admin_code'] = 1234
    return good


# returns False if any validation rules fail
def check_login(email, password):
    known_user = return_known_user()
    if email != known_user['email']:
        return False
    if password != known_user['password']:
        return False
    return True


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def password_size(password):
    if len(password) < MIN_PASSWORD:
        return False
    if len(password) > MAX_PASSWORD:
        return False
    return True


def has_uppercase(password):
    for char in password:
        if char.isupper():
            return True
    return False


def has_lowercase(password):
    for char in password:
        if char.islower():
            return True
    return False


class MyTestCase(unittest.TestCase):

    def test_test_framework(self):
        test_var = True
        self.assertEqual(True, test_var)  # add assertion here

    def test_bad_email(self):
        user_input = 'IamABadEmail'
        known_user = return_known_user()
        self.assertNotEqual(known_user['email'], user_input)

    def test_good_email(self):
        user_input = 'me@ivyguide.edu'
        known_user = return_known_user()
        self.assertEqual(known_user['email'], user_input)

    def test_bad_password(self):
        user_input = 'IamBad'
        known_user = return_known_user()
        self.assertNotEqual(known_user['password'], user_input)

    def test_good_password(self):
        user_input = 'notSoSecret1!'
        known_user = return_known_user()
        self.assertEqual(known_user['password'], user_input)

    def test_bad_admin_code(self):
        user_input = 'IamBad'
        known_user = return_known_user()
        self.assertNotEqual(known_user['admin_code'], user_input)

    def test_good_admin_code(self):
        user_input = 1234
        known_user = return_known_user()
        self.assertEqual(known_user['admin_code'], user_input)

    def test_password_size(self):
        user_input = 'small'
        self.assertEqual(False, password_size(user_input))

    def test_password_too_big(self):
        user_input = 'iambigiambigiambigiambigiambig'
        self.assertEqual(False, password_size(user_input))

    def test_password_uppercase(self):
        user_input = 'Password'
        self.assertEqual(True, has_uppercase(user_input))
        user_input = 'password'
        self.assertEqual(False, has_uppercase(user_input))

    def test_password_lowercase(self):
        user_input = 'Password'
        self.assertEqual(True, has_lowercase(user_input))
        user_input = 'PASSWORD'
        self.assertEqual(False, has_lowercase(user_input))

    def test_login_good(self):
        known_user = return_known_user()
        user_email = known_user['email']
        user_password = known_user['password']
        self.assertEqual(True, check_login(user_email, user_password))

    def test_login_bad_email(self):
        known_user = return_known_user()
        user_email = 'IamBad'
        user_password = known_user['password']
        self.assertEqual(False, check_login(user_email, user_password))

    def test_login_bad_password(self):
        known_user = return_known_user()
        user_email = known_user['email']
        user_password = 'IamBad'
        self.assertEqual(False, check_login(user_email, user_password))

    def test_email_format_good(self):
        known_user = return_known_user()
        user_email = known_user['email']
        self.assertEqual(True, is_valid_email(user_email))

    def test_email_format_bad(self):
        user_email = 'aaa.aaa.com'
        self.assertEqual(False, is_valid_email(user_email))
        user_email = 'aaa@aaa@com'
        self.assertEqual(False, is_valid_email(user_email))
        user_email = '.aaa@com'
        self.assertEqual(False, is_valid_email(user_email))
        user_email = '.aaa@$$$'
        self.assertEqual(False, is_valid_email(user_email))


if __name__ == '__main__':
    unittest.main()
