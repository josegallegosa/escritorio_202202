import pandas as pd

df = pd.read_excel('/home/gallegos/Documentos/python_ejm/tabla01.xlsx',sheet_name='Hoja1') 

action = {'Sales':'income_type_1','Ebitda':'income_type_2','Net Income':'income_type_3'}

for row in df.index:
    print(' ')
    print('<record forcecreate="True" id="'+'income_'+str(row)+'" model="income">')
    print('    <field name="income_type" ref="'+action[df['income_type'][row]]+'"/>')
    print('    <field name="year">'+str(df['year'][row])+'</field>')
    print('    <field name="exchange_rate">'+str(df['exchange_rate'][row])+'</field>')
    print('    <field name="amount_sol">'+str(df['amount_sol'][row])+'</field>')
    print('    <field name="amount_thousands_usd">'+str(df['amount_thousands_usd'][row])+'</field>')
    print('</record>')
