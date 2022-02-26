remaining_months = quinta_obj.get_month(payslip.date_from)-1
if employee.affiliate_eps:
    factor=1.0675
else:
    factor=1.09
calculo_5ta_mes = contract.wage + ASIF
mes = (quinta_obj.get_month(payslip.date_from)-13)*(-1)
if mes <6:
    gratification_projection = 2*factor*(contract.wage+ASIF)
elif mes>=6 and mes <12:
    gratification_projection = factor*(contract.wage+ASIF)
else:
    gratification_projection = 0
list_incomes = quinta_obj.get_data_month_values(employee,payslip.date_from)[0]
list_projections=quinta_obj.get_data_month_values(employee,payslip.date_from)[1]
mes = (quinta_obj.get_month(payslip.date_from)-13)*(-1)
uit = parameter_obj.get_amount('UIT',payslip.date_from)
retencion_renta=0
if mes==1:
    ingreso_anual = imp_5ta + remaining_months*calculo_5ta_mes+gratification_projection
else:
    ingreso_anual = quinta_obj.get_data_last_month(employee,payslip.date_from).income_to_date+imp_5ta+remaining_months*calculo_5ta_mes+gratification_projection
base_5ta = ingreso_anual-7*uit
if base_5ta > 0:
    renta_1=0
    saldo_base_5ta=base_5ta
    for scale in quinta_obj.get_scales_5ta(payslip.date_from):
        renta_scale=0
        if base_5ta >= scale['lower_limit'] and base_5ta <= scale['upper_limit']:
            renta_scale = saldo_base_5ta*scale['percentage']/100
            saldo_base_5ta = 0
        elif base_5ta > scale['upper_limit']:
            renta_scale = scale['lower_limit']*scale['percentage']/100
            saldo_base_5ta += -scale['lower_limit']
        renta_1 += renta_scale
else:
    renta_1 = 0
if mes==1:
    retencion_mensual = round(renta_1/(remaining_months+1),2)
else:
    retencion_mensual = round((renta_1 - quinta_obj.get_data_last_month(employee,payslip.date_from).accumulated_withholding)/(remaining_months+1),2)
if retencion_mensual<0:
    retencion_renta=0
else:
    if mes==1:
        retencion_renta = renta_1 - retencion_mensual*remaining_months
    else:
        retencion_renta = renta_1 - retencion_mensual*remaining_months - quinta_obj.get_data_last_month(employee,payslip.date_from).accumulated_withholding
for n in range(1,13):
    if n==mes:
        list_incomes[n-1] = imp_5ta
    elif mes<n:
        list_projections[n-1] = calculo_5ta_mes
accumulated_withholding = quinta_obj.get_data_last_month(employee,payslip.date_from).accumulated_withholding+retencion_renta
result = retencion_renta
quinta_obj.generate_data_5ta(contract, payslip.date_from, list_incomes, list_projections,gratification_projection,base_5ta,renta_1,accumulated_withholding,retencion_renta)
		
