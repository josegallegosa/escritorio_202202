from datetime import datetime, date
from dateutil.relativedelta import relativedelta

date_start = date(2021,1,1)
date_end = date(2021,5,31)
condition = 'M'

quincenas = ['QUINCENA I','QUINCENA II']

meses = [['ENERO'],['FEBRERO'],['MARZO'],['ABRIL'],['MAYO'],['JUNIO'],['JULIO'],['AGOSTO'],['SEPTIEMBRE'],['OCTUBRE'],['NOVIEMBRE'],['DICIEMBRE'],]

#PARA MESES
if date_start.day > 1:
	date_start += relativedelta(months=+1)
date_end += relativedelta(days=+1)

date_traveled = date(date_start.year,date_start.month,1)
for i in range(date_start.month,date_end.month):
	
	print('MES '+str(meses[i-1])+' '+str(date_start.year), str(date(date_traveled.year,date_traveled.month,1)), str(date(date_traveled.year,date_traveled.month+1,1)+relativedelta(days=-1)))
	date_traveled = date(date_traveled.year,date_traveled.month+1,1)
#PARA QUINCENA


