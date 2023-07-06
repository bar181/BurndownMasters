Feature: Login Email Validation

  As a user I want to ensure that my email is a valid approved email

  Rule: Emails should be validated to allow log-in

  Scenario: Emails entered must be on the database
    Given John is on the login page
    When John enters an invalid email to log in
    Then John should not be able to log in and should be redirected to the 'bad-request' page
