import pandas as pd
import os

def export_to_excel(vacancy_list, user_search, qual):
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(vacancy_list)
    if not os.path.exists('data'):
        os.makedirs('data')
    file_path = f'data/vacancy-habr-{user_search}-{qual}.xlsx'
    df.to_excel(file_path, sheet_name='Vacancy List', index=False)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Vacancy List', index=False)

        worksheet = writer.sheets['Vacancy List']

        for col in worksheet.columns:
            max_len_col = max(len(str(cell.value or '')) for cell in col)
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max(max_len_col + 3, 10)
    print('Data successfully exported to Excel.')