from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def calculate_age(date_of_birth):
    if date_of_birth is not None:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        now = datetime.now()
        age = now.year - dob.year

        # Check if age is less than 7 days
        if (now - dob).days < 7:
            days = (now - dob).days
            age = f"00{days:01d}"

        # Check if age is less than 28 days
        elif (now - dob).days < 28:
            weeks = (now - dob).days // 7
            age = f"01{weeks}"

        # Check if age is less than one year
        elif age < 1:
            months = (now.year - dob.year) * 12 + now.month - dob.month
            age = f"1{months:02d}"

        # Check if age is less than 100 years
        elif age < 100:
            age = f"2{age:02d}"

        # Age is larger than 100 years
        else:
            age = f"3{age:02d}"

        return age

def check_diagnosis_age_and_sex(all_diagnosis_limits, diagnosis, age, sex):
    check_message = ''
    if diagnosis in all_diagnosis_limits['description'].values:
        x = all_diagnosis_limits[all_diagnosis_limits['description'] == diagnosis]
        if pd.notna(x['age_l'].iloc[0]):
            if (age >= x['age_l'].iloc[0]) and (age <= x['age_h'].iloc[0]):
                pass
            else:
                check_message = 'age for diagnosis not correct '
        if pd.notna(x['sex'].iloc[0]):
            if sex == x['sex'].iloc[0]:
                pass
            else:
                check_message = check_message + '\n sex for diagnosis not correct'
    return check_message

def check_intervention_age_and_sex(all_intervention_limits, intervention, age, sex):
    check_message = ''
    if intervention in all_intervention_limits['description'].values:
        x = all_intervention_limits[all_intervention_limits['description'] == intervention]
        if pd.notna(x['age_l'].iloc[0]):
            if (age >= x['age_l'].iloc[0]) and (age <= x['age_h'].iloc[0]):
                pass
            else:
                check_message = 'age for intervention not correct '
        if pd.notna(x['sex'].iloc[0]):
            print(x['sex'].iloc[0])
            if sex == x['sex'].iloc[0]:
                pass
            else:
                check_message = check_message + '\n sex for intervention not correct'
    return check_message

def check_giagnosis_mdc(all_diagnosis, diagnosis):
    message = ''
    x = all_diagnosis[all_diagnosis['description'] == diagnosis]
    if '00' in x['mdc'].values:
        adrg = x['adrg'].iloc[0]
        message = f'The ADRG is {adrg}'
    return message

def check_intervention_mdc(all_interventions, intervention):
    message = ''
    x = all_interventions[all_interventions['description'] == intervention]
    if '00' in x['mdc'].values:
        adrg = x['adrg'].iloc[0]
        message = f'The ADRG is {adrg}'
    return message