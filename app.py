from flask import Flask, render_template, request, redirect
import flask_login
import psycopg2

# code sources: chatgpt was used to help with specific syntax and functions including setup
# code sources: any more advanced prompts are provided in comments
# flask_login documentation
# external css: tailwindcss.com, daisyui.com


# setup stuff - public can view this
app = Flask(__name__, static_folder='static')



app.secret_key = 'iamPublic_NotASecret1!thatsOkayForNow'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database for users
# users = {'me@ivyguide.edu': {'password': 'notSoSecret1!'}}
# users = {
#     'agile@ivyguide.edu': {
#         'id': 0,
#         'name': 'Agile Student',
#         'email': 'agile@ivyguide.edu',
#         'role': 1,
#         'password': 'notSoSecret1!'
#     },
# 'me@ivyguide.edu': {
#     'id': 0,
#     'name': 'IvyGuide',
#     'email': 'me@ivyguide.edu',
#     'role': 1,
#     'password': 'notSoSecret1!'
# },
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

    authenticated = flask_login.current_user.is_authenticated

    return render_template('index.html', records=records, tips=tips, authenticated=authenticated)

# source: chatGPT prompt: how do i have a dynamic route using flask.  For example:route /category/{moving} where moving can be anything
@app.route('/category/<category>')
def category_name(category):
    # Establish a connection to the PostgreSQL database using a connection string
    connection_string = 'postgresql://db:AVNS_w47yHPWFzhZXkeJMpv0@app-a06f5c95-e1c8-4b82-bafc-cd999e4b2920-do-user-14305200-0.b.db.ondigitalocean.com:25060/db?sslmode=require'
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()

    category = category.replace("-", " ")

    # Execute a SELECT query on the 'approved_users' table
    cursor.execute('SELECT * FROM approved_users')
    records = cursor.fetchall()

    # Execute a SELECT query on the table
    query = "SELECT * FROM posts WHERE category = %s"
    cursor.execute(query, (category,))
    tips = cursor.fetchall()

    if not tips:
        category = category.capitalize()
        query = "SELECT * FROM posts WHERE category = %s"
        cursor.execute(query, (category,))
        tips = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # edge case - wrong category name -> return home page (all)
    if not tips:
        return redirect('/')

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template('category.html', records=records, tips=tips)

# source: chatGPT prompt: how do i convert a database query into a dict in python using these params ....
def get_verified_users():
    connection_string = 'postgresql://db:AVNS_w47yHPWFzhZXkeJMpv0@app-a06f5c95-e1c8-4b82-bafc-cd999e4b2920-do-user-14305200-0.b.db.ondigitalocean.com:25060/db?sslmode=require'
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()

    # Execute a SELECT query on the table
    cursor.execute('SELECT * FROM approved_users')
    users = cursor.fetchall()
    # return users as assoc array (dict) with field names
    verified_users = {}
    for user in users:
        user_data = {
            'name': user[0],
            'password': user[1],
            'email': user[3],
            'role': user[4],
            'id': user[5],
        }
        verified_users[user_data['email']] = user_data
    return verified_users

# source: Flask-login docs
@login_manager.user_loader
def user_loader(email):
    users = get_verified_users()
    if email not in users:
        return

    user = User()
    user.id = email
    return user

# source: Flask-login docs
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


# if already logged in -> redirect to new post
# login for verified user
# source: Flask-login docs
@app.route('/login', methods=['GET', 'POST'])
def login():
    print('168 GET STart')

    if request.method == 'GET' and flask_login.current_user.is_authenticated:
        return redirect('/new-posts')

    if request.method == 'GET':
        print('173 GET')
        return render_template("login.html")
    print('175 POST')
    users = get_verified_users()
    email = request.form['email']
    password = request.form['password']

    if email in users and password == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect('/new-posts')

    return redirect('/bad-request')


# get the user details by running query
# known technical debt
# can refactor later to include in model if we have multiple verified users
# source: Flask-login docs
# source: gpt prompt: how do i filter a query by a specific field in python to get user row data ...
def get_user_details(id):
    connection_string = 'postgresql://db:AVNS_w47yHPWFzhZXkeJMpv0@app-a06f5c95-e1c8-4b82-bafc-cd999e4b2920-do-user-14305200-0.b.db.ondigitalocean.com:25060/db?sslmode=require'
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()

    email = str(flask_login.current_user.id)
    query = "SELECT * FROM approved_users WHERE email = %s"
    cursor.execute(query, (email,))
    record = cursor.fetchone()
    return record


# this is the verified user post
# source: gpt prompt: how do i database insert using python for the following field data
@app.route('/new-posts', methods=['GET', 'POST'])
@flask_login.login_required
def new_posts():

    authenticated = flask_login.current_user.is_authenticated
    if request.method == 'GET':
        return render_template("new_posts.html", user=flask_login.current_user, authenticated = authenticated)

    user = get_user_details(flask_login.current_user.id)

    title = request.form['title']
    author = user[0]
    text = request.form['text']
    category = request.form['category']

    print('new_posts record user')
    print(user)

    # Execute a SELECT query on the table
    connection_string = 'postgresql://db:AVNS_w47yHPWFzhZXkeJMpv0@app-a06f5c95-e1c8-4b82-bafc-cd999e4b2920-do-user-14305200-0.b.db.ondigitalocean.com:25060/db?sslmode=require'
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    insert_query = 'INSERT INTO posts (title, author, text, category) VALUES (%s, %s, %s, %s)'
    cursor.execute(insert_query, (title, author, text, category))
    connection.commit()

    return redirect('/new-posts')


@app.route("/bad-request")
def bad_request():
    return render_template("bad_request.html")

# source: Flask-login docs
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')

# source: Flask-login docs
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


if __name__ == '__main__':
    app.run()
