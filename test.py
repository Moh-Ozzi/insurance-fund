import pandas as pd

all_diagnosis = pd.read_csv('data/all_diagnosis.csv')
all_interventions = pd.read_csv('data/all_interventions.csv')
all_diagnosis_limits = pd.read_csv('data/all_diagnosis_limits.csv')
all_intervention_limits = pd.read_csv('data/all_intervention_limits.csv')


# print(all_diagnosis_limits.head(20))
# print(all_intervention_limits[all_intervention_limits['age_l'].isna()])


# print(all_diagnosis_limits.info())
# print(all_intervention_limits.info())
# print(all_intervention_limits[all_intervention_limits['code'] == '92211-00'])

x = all_diagnosis[all_diagnosis['mdc'] == '00']
print(x['adrg'].unique())