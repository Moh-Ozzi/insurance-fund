
from flask import Flask, request, redirect, session, url_for, flash, render_template
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import dash
from dash import dcc, html, Input, Output, State, ALL
from utils.login_handler import restricted_page
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datetime import datetime, timedelta
import random
import string
import smtplib
from email.message import EmailMessage
import dash_mantine_components as dmc
import numpy as np


## SERVER CONFIGURATION AND INITIALISATION

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
server.config.update(SECRET_KEY='5791628bb0b13ce0c676dfde280ba245')
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(server)


#
# 'postgresql://superstore_jibm_user:6a4sKfN1RmZwRMr06jCxKABco67BmHhq@dpg-cmajt30l5elc73el1qi0-a.frankfurt-postgres.render.com/superstore_jibm'



global_username = ''

## Creating the USER Model and the Database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    trial = db.Column(db.Boolean(20))
    OTP = db.Column(db.String(80))
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.password}', '{self.trial}', '{self.OTP}', '{self.registration_date}')"




with server.app_context():
    db.create_all()

## Routing For Login and Registartion and Logout
alert = False
count_message = 0

@server.route('/register', methods=['POST', 'GET'])
def register_route():
    global alert
    global count_message
    if request.form:
        data = request.form
        with server.app_context():
            # if User.query.all() == []:
            user = User(username=data['username'], password=data['password'], trial=True)
            db.session.add(user)
            db.session.commit()
            alert=True
            count_message = 0
        return redirect('/login')


@server.route('/login', methods=['POST'])
def login():
    global global_username
    if request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return """invalid username and/or password <a href='/login'>login here</a>"""
        if (datetime.utcnow() > user.registration_date + timedelta(minutes=1)) and (user.trial == True) and (user.OTP == None):
            global_username = username
            return redirect('/trial')
        login_user(user)
        if 'url' in session:
            if session['url']:
                url = session['url']
                session['url'] = None
                return redirect(url) ## redirect to target url
        return redirect('/check') ## redirect to home


@server.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('/'))


@server.route("/test")
def test():
    return render_template('test.html')


# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(username):
    u = User.query.get(username)
    return u

load_figure_template("united")

# The DASH APP
app = dash.Dash(
    __name__, server=server, use_pages=True, suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP]
)
app.config["suppress_callback_exceptions"] = True

server = app.server

home_page = dbc.NavLink(html.Div("Home", className="fw-bolder fs-5 text"), href="/", active="exact")
check_page = dbc.NavLink(html.Div("Check", className="fw-bolder fs-5 text"), href="/check", active="exact")
register_page = dbc.NavLink(html.Div("Register", className="fw-bolder fs-5 text"), href="/register", active="exact")
login_page = dbc.NavLink(html.Div("Login", className="fw-bolder fs-5 text"), href="/login", active="exact")
logout_page = dbc.NavLink(html.Div("Logout"), href="/logout", active="exact")
menue = dbc.NavLink(dbc.DropdownMenu(children=
            [dbc.DropdownMenuItem("Settings", id='placeholder', className="fw-bolder"), dbc.DropdownMenuItem("Logout", href='/logout', className="fw-bold")],
            label="Profile",
            nav=True,
            className="fw-bolder fs-5 text"
                    ),
             active="exact"
            )

toggle_button = dbc.Button(
    id="navbar-toggle", style={"height": "1px",}
)



sidebar = dbc.Nav(
            [
                toggle_button,
                html.Br(),
                html.Br(),
                html.Div(home_page),
                html.Div(id="check-page"),
                html.Div(id="table-page"),
                html.Div(id="register-page"),
                html.Div(id="login-page"),
                html.Div(id="time-page"),
                html.Div(id="menu", className="text-danger"),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Hr(),
            ],
            navbar=True,
            vertical=True,
            pills=True,
            className="border border-2 shadow",
style={'height': '100vh'},
    )

collapse = dbc.Collapse(sidebar, id="navbar-collapse", is_open=True)


app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    # toggle_button,
                    sidebar,
                    dcc.Location(id="url") ## THE PATH ELEMENT
                ], width=2, style={'height': '100%'}, className='mt-1'),
            dbc.Col(
                dash.page_container, width=10
            )
        ],
            className='my-2', style={'height': '100%'}
    )
], fluid=True, style={'background-color': '#F8F9F9'})


@app.callback(
     Output("register-page", "children"),
     Output("login-page", "children"),
     Output("check-page", "children"),
     Output("menu", "children"),
     Output('url', 'pathname'),
     Input("url", "pathname"),
     Input({'index': ALL, 'type':'redirect'}, 'n_intervals'),
    prevent_initial_call=True
)
def update_authentication_status(path, n):
    global popovers
    ### logout redirect
    if n:
        if not n[0]:
            return '', '', '', '', dash.no_update
        else:
            return '', '', '', '', '/'

    ### test if user is logged in
    if current_user.is_authenticated:
        if path == '/login':
            return '', '',  check_page, menue, '/'

        if path == '/summary':
            return '', '', check_page, menue, dash.no_update

        return '', '', check_page, menue,  dash.no_update
    else:
        ### if page is restricted, redirect to login and save path
        if path in restricted_page:
            session['url'] = path
            return register_page, login_page, '', '', '/login'
    ### if path not login and logout display login link
    if current_user and path not in ['/register', '/login', '/logout']:
        return register_page, login_page, '', '', dash.no_update
    elif path == '/register':
        return register_page, login_page, '', '', dash.no_update

    ### if path login and logout hide links
    if path in ['/login', '/logout', '/register']:
        return register_page, login_page, '', '', '', dash.no_update, ''

@app.callback(
    Output("username", "children"),
    Input('url', 'pathname'))
def current_username(url):
    if url == '/summary' and current_user.is_authenticated:
        current_username = "Welcome, " + current_user.username + '!'
        return current_username


@app.callback(
    Output("the_alert", "children"),
    Input("url", "pathname"))
def toggle_modal(path):
    alert_message = dbc.Alert("User registered successfully", color="#f5813d",
                              dismissable=True, className="text-center fw-bold")
    global count_message
    if path == '/login' and alert == True and count_message == 0:
        count_message = 1
        return alert_message
    return dash.no_update

@app.callback(
    Output("buying_message", "children"),
    Input("buy_button", "n_clicks"),
    Input('otp-input', 'value')
    )
def update_user(n, value):
    global alert
    with server.app_context():
        user = User.query.filter_by(username=global_username).first()
        if n == 1 and user.OTP == None:
            otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
            user.OTP = otp
            user.trial = False
            db.session.commit()
            sendemail(otp)
            return 'شكرا. سيتم التواصل معك وتزوريدك بكلمة مرور يرجى إدخالها بالأسفل.'
        if user.OTP is not None:
            if value == user.OTP:
                alert=False
                return "تم تفعيل الحساب. يمكنك تسجيل الدخول الان."

def sendemail(OTP):
    EMAIL_ADDRESS = 'mohamedelauzei@gmail.com'
    EMAIL_PASSWORD = 'rrfm ugmh reca gljy'
    msg = EmailMessage()
    msg['Subject'] = 'New user'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'mohamedelauzei@gmail.com'
    msg.set_content('The OTP for new user {} IS {}'.format(global_username, OTP))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == "__main__":
    app.run_server(debug=True)