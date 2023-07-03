from flask import Flask, render_template, request, redirect
import flask_login
import psycopg2

# code sources: chatgpt was used to help with specific syntax and functions including setup
# code sources: any more advanced prompts are provided in comments
# external css: tailwindcss.com, daisyui.com


# setup stuff - public can view this
app = Flask(__name__, static_folder='static')


@app.route('/')
def index2():
    # Establish a connection to the PostgreSQL database using a connection string
    connection_string = 'postgresql://db:AVNS_w47yHPWFzhZXkeJMpv0@app-a06f5c95-e1c8-4b82-bafc-cd999e4b2920-do-user-14305200-0.b.db.ondigitalocean.com:25060/db?sslmode=require'
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()

    # Execute a SELECT query on the table
    cursor.execute('SELECT * FROM approved_users')
    records = cursor.fetchall()

    cursor.execute('SELECT * FROM posts')
    tips = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template('index.html', records=records, tips=tips)
app.secret_key = 'iamPublic_NotASecret1!thatsOkayForNow'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database for users
# users = {'me@ivyguide.edu': {'password': 'notSoSecret1!'}}
# users = {
#     'me@ivyguide.edu': {
#         'id': 0,
#         'name': 'IvyGuide',
#         'email': 'me@ivyguide.edu',
#         'role': 1,
#         'password': 'notSoSecret1!'
#     },
#     'mg@ivyguide.edu': {
#         'id': 1,
#         'name': 'Malaika Goswamy',
#         'email': 'mg@ivyguide.edu',
#         'role': 1,
#         'password': 'notSoSecret1!'
#     }
# }

# verified new user invitation code
admin_code = "Agile"

# Password vailidations - MAKE CHANGES IN TDD tests/unit_tests.py
MIN_PASSWORD = 6
MAX_PASSWORD = 12
UPPERCASE = True
LOWERCASE = True

class User(flask_login.UserMixin):
    pass

def get_verified_users():
    connection_string = 'postgresql://db:AVNS_w47yHPWFzhZXkeJMpv0@app-a06f5c95-e1c8-4b82-bafc-cd999e4b2920-do-user-14305200-0.b.db.ondigitalocean.com:25060/db?sslmode=require'
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()

    # Execute a SELECT query on the table
    cursor.execute('SELECT * FROM approved_users')
    users = cursor.fetchall()
    # return users
    verified_users = {}
    for user in users:
        user_data = {
            'id': user[0],
            'name': user[1],
            'password': user[2],
            'email': user[4],
            'role': user[5]
        }
        verified_users[user_data['email']] = user_data
    return verified_users


@login_manager.user_loader
def user_loader(email):
    users = get_verified_users()
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    users = get_verified_users()
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route("/register")
def register():
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("def login - line 131")
    users = get_verified_users()
    print(users)
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']

    if email in users and password == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect('/new-posts')

    return redirect('/bad-request')


# this is the verified user post
@app.route('/new-posts')
# @flask_login.login_required
def protected():
    return render_template("new_posts.html", user=flask_login.current_user)
    # return 'Logged in as: ' + flask_login.current_user.id


@app.route("/bad-request")
def bad_request():
    return render_template("bad_request.html")


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


if __name__ == '__main__':
    app.run()
