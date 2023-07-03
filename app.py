from flask import Flask, render_template, request, redirect
import flask_login
import sqlite3

# code sources: chatgpt was used to help with specific syntax and functions including setup
# code sources: any more advanced prompts are provided in comments
# external css: tailwindcss.com, daisyui.com


# setup stuff - public can view this
app = Flask(__name__, static_folder='static')
app.secret_key = 'iamPublic_NotASecret1!thatsOkayForNow'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database for users
# users = {'me@ivyguide.edu': {'password': 'notSoSecret1!'}}
users = {
    'me@ivyguide.edu': {
        'id': 0,
        'name': 'IvyGuide',
        'email': 'me@ivyguide.edu',
        'role': 1,
        'password': 'notSoSecret1!'
    },
    'mg@ivyguide.edu': {
        'id': 1,
        'name': 'Malaika Goswamy',
        'email': 'mg@ivyguide.edu',
        'role': 1,
        'password': 'notSoSecret1!'
    }
}

# verified new user invitation code
admin_code = "Agile"

# Password vailidations - MAKE CHANGES IN TDD tests/unit_tests.py
MIN_PASSWORD = 6
MAX_PASSWORD = 12
UPPERCASE = True
LOWERCASE = True

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

tips = []

tip = {
    'title': 'Getting Here from airport',
    'text': "If it's your first time, just take Uber ($25) or taxi ($35).  The subway system rocks for return or cheap students - runs from airport to Harvard Square"
}
tips.append(tip)
tip = {
    'title': 'Laundry',
    'text': "There are laundry machines in each dorm (or as Harvard calls them 'Houses' or 'Halls'.  Some use quarters.  Others you need to add cash to a payment card called Crismon Cash.  If you want to be pampered there is a laundry service you can buy"
}
tips.append(tip)
tip = {
    'title': 'Do I need pillows and bedding?',
    'text': "Students taking a plane here likely won't have room in their suitcase.  There is a Target one subway stop away.  We were provided a blanket.  Also, check out the donoation bins in each dorm."
}
tips.append(tip)
tip = {
    'title': 'Is Harvard really as good as in the movies',
    'text': "Yes. You'll find out!"
}
tips.append(tip)
tip = {
    'title': 'Is the campus busy in the summer',
    'text': "Harvard has 2 main terms (Fall and Winter).  The summer is operated by the Summer School.  So no regular HArvard students unless they are working here or taking a summer class like you.  The campus and area is still busy.  You'll see a lot of high school students around and people taking courses to meet on-campus requirements"
}
tips.append(tip)

tip = {
    'title': 'Can I pick a roommate?',
    'text': "No. I had one roommate and found out when I moved in.  Most dorm rooms are 2 people per room.  Small bedrooms but big common area.  During the regular school year there were 4 people in m dorm room and in the summer only 2"
}
tips.append(tip)

@app.route("/")
def index():
    return render_template("index.html", tips=tips)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("def login - line 131")
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
