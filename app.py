from flask import Flask, render_template, request, redirect
import flask_login

# setup stuff - public can view this
app = Flask(__name__)
app.secret_key = 'iamPublic_NotASecret1!thatsOkayForNow'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database.
users = {'foo@bar.tld': {'password': 'secret'}}


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

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bad-request")
def bad_request():
    return render_template("bad_request.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("def login")
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect('/protected')

    return redirect('/bad-request')


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


if __name__ == '__main__':
    app.run()
