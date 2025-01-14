import requests
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count

from debounce import debouncer

# https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014
BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates'
THREAD_POOL_SIZE = 2


def get_dates(total_days=7) -> list[str]:
    result_ = []
    today = datetime.now()
    for d in range(total_days):
        date_ = today - timedelta(days=d)
        str_date = datetime.strftime(date_, '%d.%m.%Y')
        result_.append(str_date)
    result_.append('err_date')
    return result_


def get_rate(date: str) -> dict:
    url = f'{BASE_URL}?json&date={date}'
    response = requests.get(url)
    exchange_rate = response.json()['exchangeRate']
    rates = list(filter(lambda el: el.get('currency', None) in ['EUR', 'USD'], exchange_rate))
    rates = list(map(lambda el: {
        el.get('currency', None): {'sale':  el.get('saleRate', None), 'purchase':  el.get('purchaseRate', None)}
    }, rates))
    result = {}
    for el in rates:
        result.update(el)
    return result


def worker(date_):
    # sleep
    func = debouncer(lambda: True, 100)
    while not func() is True:
        pass

    try:
        r = get_rate(date_)
    except Exception as err:
        return {date_: err}
    else:
        return {date_: r}


if __name__ == '__main__':
    dates = get_dates()
    with Pool(cpu_count()) as pool:
        pool.map_async(worker, dates, callback=print)
        pool.close()
        pool.join()
