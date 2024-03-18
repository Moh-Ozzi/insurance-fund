import dash
from dash import html, dcc, callback, Input, Output, ctx, State
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from utils.login_handler import require_login
from pages.funcs import calculate_age, check_diagnosis_age_and_sex, check_intervention_age_and_sex, \
    check_giagnosis_mdc, check_intervention_mdc
import numpy as np


dash.register_page(__name__, title='check', path='/check')
require_login(__name__)



all_diagnosis = pd.read_csv('data/all_diagnosis.csv')
all_interventions = pd.read_csv('data/all_interventions.csv')
all_diagnosis_limits = pd.read_csv('data/all_diagnosis_limits.csv')
all_intervention_limits = pd.read_csv('data/all_intervention_limits.csv')



diagnosis = all_diagnosis['description'].unique()
interventions = all_interventions['description'].unique()

layout = html.Div([
    html.P('Enter age: '),
    dcc.DatePickerSingle(id='dob', max_date_allowed=datetime.now().date()),
    html.P('Enter sex: '),
    dcc.Dropdown(
                    id="sex-dropdown",
                        options= [{'label': 'Male', 'value': 'MALE'},
                              {'label': 'Female', 'value': 'FEML'}]
                ),
    html.P('Enter diagnos: '),
    dcc.Dropdown(
                id="diagnosis-dropdown",
                options=[{'label':diagnos, 'value':diagnos} for diagnos in diagnosis],
            ),
    html.P('Enter intervention: '),
    dcc.Dropdown(
                id="interventions-dropdown",
                options=[{'label':intervention, 'value':intervention} for intervention in interventions],
            ),
    html.Br(),
    dbc.Button('Submit', id='button'),
    html.H1(id='text')
    ]
)



@callback(Output('text', 'children'),
          Input('button', 'n_clicks'),
          State('dob', 'date'), State('sex-dropdown', 'value'),
          State('diagnosis-dropdown', 'value'), State('interventions-dropdown', 'value'))
def execute(button, dob, sex, diagnosis, treatement):
    if  ctx.triggered_id == "button":
        age = int(calculate_age(dob))
        diagnosis_age_sex_check = check_diagnosis_age_and_sex(all_diagnosis_limits, diagnosis, age, sex)
        intervention_age_sex_check = check_intervention_age_and_sex(all_intervention_limits, treatement, age, sex)
        if diagnosis_age_sex_check != '':
            return diagnosis_age_sex_check
        elif intervention_age_sex_check != '':
            return intervention_age_sex_check
        # Check MDC (by Diagnosis in Appendix A) if equal 00
        diagnosis_mdc_chechk = check_giagnosis_mdc(all_diagnosis, diagnosis)
        if diagnosis_mdc_chechk != '':
            return diagnosis_mdc_chechk
        # Check MDC (by Treatment in Appendix B) if equal 00
        intervention_md_check = check_intervention_mdc(all_interventions, treatement)
        if intervention_md_check != '':
            return intervention_md_check
        # Check for common ADRG between diagnosis & treatement
        diagnosis_df = all_diagnosis[all_diagnosis['description'] == diagnosis]
        intervention_df = all_interventions[all_interventions['description'] == treatement]
        merged = pd.merge(diagnosis_df, intervention_df, on='adrg')
        if merged.shape[0] > 0:
            adrg = merged['adrg'].iloc[0]
            return f'ADRG is {adrg}'

    return ''


            # CHECK THAT AGE LIMIT IS NOT NULL



        # CHECK THAT INTERVENTION HAS AGE LIMIT

        # CHECK THAT DIAGNOSIS HAS SEX SPECIFICATION

        # CHECK THAT INTERVENTION HAS SEX SPECIFICATION

