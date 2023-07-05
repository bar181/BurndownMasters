import unittest
import re

# code source for email vailidation function from chatgpt prompt: in python check if email is formatted okay

# note sprint 2 included refactored orginal tests based on new information about format from database
# Sprint 2 removed 3 old tests that were not valid anymore (now there are 13 sprint 1 tests)
# Sprint 2 added 15 net new unit tests (total tests at end of spring 2 is 28)
# Ran 28 tests in 0.006s
# OK

# password validation rules
MIN_PASSWORD = 6
MAX_PASSWORD = 30
UPPERCASE = True
LOWERCASE = True


# sample user (refactored in sprint 2 based on new known format)
users = []
user = {'me@ivyguide.edu': {
    'id': 0,
    'name': 'IvyGuide',
    'email': 'me@ivyguide.edu',
    'role': 1,
    'password': 'notSoSecret1!'}
}
users.append(user)

# for category testing: to use in URL (category/<name>)
approved_categories = ["Moving", "Dining", "Transport", "Residential life", "Things to do", "test"]


# for new posts
POST_MAX_TITLE = 50
POST_MAX_CONTENT = 500
POST_MAX_WORD_LENGTH = 40


def return_known_user():
    return users[0]['me@ivyguide.edu']


# returns False if any validation rules fail
def validate_login(email, password):

    if not is_valid_email(email):
        return False
    if not password_size(password):
        return False

    return True


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


def is_category_approved(category):
    return category in approved_categories


# verified user posts - validations

# functional tests - checks everything for title
def valid_post_title(text):
    text = str(text)
    if not valid_post_title_size(text):
        return False
    if not valid_sentence_size(text):
        return False
    return True


# functional tests - checks everything for new post content (i.e. tip)
def valid_post_content(text):
    text = str(text)
    if not valid_post_content_size(text):
        return False
    if not valid_sentence_size(text):
        return False
    return True


# False if too big or too small
def valid_post_title_size(text):
    text = str(text)
    if len(text) < 1:
        return False
    if len(text) > POST_MAX_TITLE:
        return False
    return True


def valid_post_content_size(text):
    text = str(text)
    if len(text) < 1:
        return False
    if len(text) > POST_MAX_CONTENT:
        return False
    return True


# False if a single word is too big
def valid_word_size(text):
    if len(text) > POST_MAX_WORD_LENGTH:
        return False
    return True

# check all word in input to make sure no word > than max word size
# code help source: chatgpt prompt: can you provide the code for the function def valid_sentence_size where the pseudocode is provided
    # break sentence into words (separate by space)
    #     # loop through words
    #     # call valid_word_size(text) -> if false return False
def valid_sentence_size(sentence):
    # break sentence into words (separated by space)
    words = sentence.split()

    # loop through words - if false return
    for word in words:
        if not valid_word_size(word):
            return False

    return True

# for new posts
# POST_MAX_TITLE = 50
# POST_MAX_CONTENT = 500


class MyTestCase(unittest.TestCase):

    def test_test_framework(self):
        test_var = True
        self.assertEqual(True, test_var)  # add assertion here

    def test_bad_email(self):
        user_input = 'IamABadEmail'
        known_user = return_known_user()
        self.assertNotEqual(known_user['email'], user_input)

    def test_user_format_okay(self):
        known_user = return_known_user()
        self.assertEqual(known_user['name'], "IvyGuide")
#
    def test_user_format_has_all_fields(self):
        known_user = return_known_user()
        self.assertEqual(known_user['id'], 0)
        self.assertEqual(known_user['name'], "IvyGuide")
        self.assertEqual(known_user['email'], "me@ivyguide.edu")
        self.assertEqual(known_user['role'], 1)
        self.assertEqual(known_user['password'], "notSoSecret1!")

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

    def test_bad_role(self):
        user_input = 'IamBad'
        known_user = return_known_user()
        self.assertNotEqual(known_user['role'], user_input)

    def test_good_role(self):
        user_input = 1
        known_user = return_known_user()
        self.assertEqual(known_user['role'], user_input)
#
    def test_password_size(self):
        user_input = 'small'
        self.assertEqual(False, password_size(user_input))

    def test_password_too_big(self):
        user_input = 'iambigiambigiambigiambigiambigLikeReallyeallyeallyLong!'
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

    def test_validate_login(self):
        known_user = return_known_user()
        user_email = known_user['email']
        user_password = known_user['password']
        self.assertEqual(True, validate_login(user_email, user_password))

    def test_validate_login_bad_email(self):
        known_user = return_known_user()
        user_email = "IamBad"
        user_password = known_user['password']
        self.assertEqual(False, validate_login(user_email, user_password))

    def test_validate_login_bad_password_size(self):
        known_user = return_known_user()
        user_email = known_user['email']
        user_password = '123'
        self.assertEqual(False, validate_login(user_email, user_password))
        user_password = '1234567890123456789012345678901234567890'
        self.assertEqual(False, validate_login(user_email, user_password))

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

    def test_bad_category_provided(self):
        category = 'IamBad'
        self.assertEqual(False, is_category_approved(category))

    def test_perfect_category_one_word(self):
        category = 'Moving'
        self.assertEqual(True, is_category_approved(category))
        category = 'Transport'
        self.assertEqual(True, is_category_approved(category))

    def test_fail_category_not_capitalized_one_word(self):
        category = 'moving'
        self.assertEqual(False, is_category_approved(category))

    def test_category_adjusted_not_capitalized_one_word(self):
        category = 'moving'
        category = category.capitalize()
        self.assertEqual(True, is_category_approved(category))

    def test_fail_category_multi_word(self):
        category = 'residential-life'
        self.assertEqual(False, is_category_approved(category))

    def test_fail_category_multi_word_not_remove_hyphen(self):
        category = 'residential-life'
        category = category.capitalize()
        self.assertEqual(False, is_category_approved(category))

    def test_category_adjusted_multi_word(self):
        category = 'residential-life'
        category = category.capitalize()
        category = category.replace("-", " ")
        self.assertEqual(True, is_category_approved(category))

    def test_fail_new_post_title_size(self):
        title = ''
        self.assertEqual(False, valid_post_title_size(title))

    def test_good_new_post_title_size(self):
        title = 'I am good'
        self.assertEqual(True, valid_post_title_size(title))

    def test_new_post_title_too_big_size(self):
        title = '0123456789 01234567890 1234567890 1234567890 1234567890'
        self.assertEqual(False, valid_post_title_size(title))

    def test_word_size_single_word(self):
        title = 'Word'
        self.assertEqual(True, valid_word_size(title))

    def test_sentence_size_single_word_okay(self):
        title = 'Word'
        self.assertEqual(True, valid_sentence_size(title))

    def test_sentence_size_single_word_too_big(self):
        title = 'IamTooBig012345678901234567890123456789012345678901234567890'
        self.assertEqual(False, valid_sentence_size(title))

    def test_sentence_size_multiple_words_okay(self):
        title = 'I am a good Sentence '
        self.assertEqual(True, valid_sentence_size(title))

    def test_sentence_size_multiple_words_too_big(self):
        title = 'I am a bad Sentence with a long word IamTooBig012345678901234567890123456789012345678901234567890'
        self.assertEqual(False, valid_sentence_size(title))

    def test_valid_post_content_size(self):
        text = 'I am good '
        self.assertEqual(True, valid_post_content_size(text))

    def test_valid_post_content_size_too_big(self):
        text = '0123456789 01234567890 1234567890 1234567890 1234567890'
        text = text * 10
        self.assertEqual(False, valid_post_content_size(text))

    def test_entire_valid_post_title(self):
        text = 'I am good '
        self.assertEqual(True, valid_post_title(text))

    def test_entire_valid_post_title_bad(self):
        text = '0123456789 01234567890 1234567890 1234567890 1234567890'
        self.assertEqual(False, valid_post_title(text))


    def test_valid_post_content(self):
        text = 'I am good '
        self.assertEqual(True, valid_post_content(text))

    def test_valid_post_content_multi_words(self):
        text = '0123456789 01234567890 1234567890 1234567890 1234567890'
        self.assertEqual(True, valid_post_content(text))

    def test_valid_post_content_bad_post(self):
        text = '0123456789 01234567890 1234567890 1234567890 1234567890'
        long_word = 'I am a bad Sentence with a long word IamTooBig012345678901234567890123456789012345678901234567890'
        self.assertEqual(False, valid_post_content(text * 10))  # fail too long
        self.assertEqual(False, valid_post_content(text + long_word))  # fail long word
        self.assertEqual(False, valid_post_content(text*10 + long_word)) # too long and fail long word

if __name__ == '__main__':
    unittest.main()
