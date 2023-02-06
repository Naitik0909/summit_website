from datetime import datetime

def getFormatedDate(date):
    if(date == ""):
        return None
    format = '%d/%m/%Y %H:%M:%S'
    try:
        formated_date = datetime.strptime(date, format)
        return formated_date
    except Exception as e:
        formated_date = None
        return formated_date