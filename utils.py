import datetime


def convert_date(date:str)-> str:
    """Converts date from dd/mm/yyyy to yyyy-mm-dd"""
    format_str = '%d/%m/%Y - %H:%M:%S' # The format
    return datetime.datetime.strptime(date, format_str).strftime('%Y-%m-%d %H:%M:%S')

