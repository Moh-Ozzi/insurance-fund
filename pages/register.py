import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)

# Registration screen
# layout = html.Form([
#         html.Label('Username'),
#         dcc.Input(id='username', type='text', name='username'),
#         html.Label('Password'),
#         dcc.Input(id='password', type='password', name='password'),
#         html.Button('Submit', id='submit_button', type='submit')
#     ], method='POST')

username_input = html.Div(
    [
        dbc.Label("Username"),
        dbc.Input(type="text", id="username", placeholder="Enter username", name="username"),
        # dbc.FormText(
        #     "Please enter your username",
        #     color="dark",
        # ),
    ],
    className="mb-3 form-group",
)

password_input = html.Div(
    [
        dbc.Label("Password"),
        dbc.Input(
            type="password",
            id="password",
            placeholder="Enter password", name="password"
        ),
        # dbc.FormText(
        #     "يجب أن يحتوي 6 حروف و أرقام", color="dark"
        # )
    ],
    className="mb-3 form-group",
)

button_input = html.Div(
dbc.Button('Sign up', id='submit_button', type='submit'),
    className= "mb-3 form-group"
)



layout = html.Div([
    html.H2("Create an Account", className="my-4 text-center"),
    html.Form([username_input, password_input, button_input], method='POST')
     ],
    className="mx-auto col-10 col-md-8 col-lg-6"
)




