import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_month_count(installment_type):
    installment_type_lower = installment_type.lower()
    if installment_type_lower == 'annual':
        month_count = 12
    elif installment_type_lower == 'quarter':
        month_count = 3
    elif installment_type_lower == 'monthly':
        month_count = 1
    elif installment_type_lower == 'half_annual':
        month_count = 6

    return month_count


def calculate_max_grace_date(installment_date, max_grace):
    max_grace_date = installment_date
    for i in range(max_grace):
        if max_grace_date.date().weekday() == 3:  # Thursday
            max_grace_date = max_grace_date + relativedelta(days=3)
        elif max_grace_date.date().weekday() == 4:  # Friday
            max_grace_date = max_grace_date + relativedelta(days=2)
        else:
            max_grace_date = max_grace_date + relativedelta(days=1)
    max_grace_date_str = max_grace_date.strftime('%d-%m-%y')
    return max_grace_date_str


installment_data = []
with open('C:\\project1\\project_installment\\Contracts.csv','r') as f1:
    reader_list = csv.reader(f1)
    headers = next(reader_list)
    for row in reader_list:
        installment_data.append(row)
        contract_startdate_str = datetime.strptime(row[1], '%d-%m-%Y') # convert stardate from string to date
        contract_enddate_str = datetime.strptime(row[2], '%d-%m-%Y') # convert end date from string to date
        # get the different between start_date , end_date
        start_end_dates_difference = relativedelta(contract_enddate_str,contract_startdate_str)
        installment_type = row[6]  # contract_payment_type
        month_count = calculate_month_count(installment_type)
        print('month_count',month_count)
        # calculate total months and convert years to months
        total_months = start_end_dates_difference.years * 12 + start_end_dates_difference.months
        # calculate installment count
        installment_count = total_months / month_count
        # calculate installment amount
        # Check if deposit exists and calculate installment amount  after deducting deposit
        # contract total fees - contract deposit / installment count
        if row[4] and int(row[4]) is not None:  # row[4] = contract_deposit_fees
            installment_amount = (int(row[3]) - int(row[4])) / installment_count
        else:
            installment_amount = int(row[3]) / installment_count  # row[3]== contract_total_fees
        # read max_grace
        max_grace = int(row[7])  # row[7] = max_grace (working_days)
############################################################
        print(installment_data)
        print(installment_type)
        print(start_end_dates_difference)
        print(start_end_dates_difference.years,'years')
        print('count of installment : ',installment_count)
        print('installment amount : ', installment_amount)
        print('max_grace', max_grace)

        headers = ['installment serial', 'installment date', 'installment amount', 'max grace date']
        file_name = f'C:\\project1\\project_installment\\{int(row[0])}-{row[5]}-installments.csv'
        with open(file_name, 'w', newline='') as f2:
            write_pen = csv.writer(f2)
            write_pen.writerow(headers)
            for i in range(int(installment_count)):
                installment_serial = i + 1
                installment_date = contract_startdate_str + relativedelta(months=month_count * i)
                installment_date_str = installment_date.strftime('%d-%m-%Y')
                max_grace_date_str = calculate_max_grace_date(installment_date, max_grace)
                write_pen.writerow([installment_serial, installment_date_str, installment_amount,max_grace_date_str])


