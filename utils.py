import datetime
import os


def convert_date(date:str)-> str:
    """Converts date from dd/mm/yyyy to yyyy-mm-dd"""
    format_str = '%d/%m/%Y - %H:%M:%S' # The format
    return datetime.datetime.strptime(date, format_str).strftime('%Y-%m-%d %H:%M:%S')

def return_url(env):
    if env == 'local':
        url = os.environ.get('URL_LOCAL')
    if env == 'prod':
        url = os.environ.get('URL_PROD')

    return url