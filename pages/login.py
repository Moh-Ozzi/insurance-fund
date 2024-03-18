from flask import Flask, flash, redirect, request, url_for, get_flashed_messages
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)

# Login screen
# layout = html.Div([
# html.Form(
#     [
#         html.H2("Please log in to continue:", id="h1"),
#         dcc.Input(placeholder="Enter your username", type="text", id="uname-box", name='username'),
#         dcc.Input(placeholder="Enter your password", type="password", id="pwd-box", name='password'),
#         html.Button(children="Login", n_clicks=0, type="submit", id="login-button"),
#         html.Div(children="", id="output-state")
#     ], method='POST'
# ),
# dcc.Link("register", href="/register")
# ])



username_input = html.Div(
    [
        dbc.Label("Username"),
        dbc.Input(type="text", id="uname-box", placeholder="Enter username", name="username"),
        # dbc.FormText(
        #     "Please enter your username",
        #     color="secondary",
        # ),
    ],
    className="mb-3 form-group",
)

password_input = html.Div(
    [
        dbc.Label("Password"),
        dbc.Input(
            type="password",
            id="pwd-box",
            placeholder="Enter password", name="password"
        ),
    ],
    className="mb-3 form-group",
)

button_input = html.Div(
dbc.Button('Login', id='login_button', type='submit', n_clicks=0),
    className= "mb-3 form-group rounded-0"
)


layout = html.Div([
    # html.Div([
    #     # Check if there are flashed messages and display them
    #
    #     *[html.P(message) for message in get_flashed_messages()]
    # ], className='alert alert-danger'),
    html.Div(id="the_alert", children=[]),
    html.Div(children="", id="output-state"),
    html.H2("Login", className="my-4 text-center"),
    html.Form([username_input, password_input, button_input], method='POST'),
html.Br(),
    dcc.Link("Don't have an account?", href="/register"),
    html.Br(),
html.Br(),
    dcc.Link("Forgot your Password?", href="/register")
     ],
    className="mx-auto col-10 col-md-8 col-lg-6"
)

