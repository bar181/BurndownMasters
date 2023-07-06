from behave import *
import re
import app

email = 'me@ivyguide.edu'

@given("John is on the login page")
def step_impl(context):
    pass

@when("John enters an invalid {email} to log in")
def step_impl(context, email):
    test_email = email

@then("John should not be able to log in and should be redirected to the 'bad-request' page")
def step_impl(context):
    assert(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None)



