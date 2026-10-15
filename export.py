import os
import pandas as pd

def export_to_excel(vacancy_list, user_search):
    df = pd.DataFrame(vacancy_list)

    if not os.path.exists('data'):
        os.makedirs('data')

    df.to_excel(f'data/vacancy-habr-{user_search}.xlsx', sheet_name='Vacancy List', index=False)
    print('Data successfully exported to Excel.')