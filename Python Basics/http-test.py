import requests
import random

numbers_api_base_url = "http://numbersapi.com/"
binance_api = "https://api.binance.com/api/v3/ticker/price"


def print_request_headers(res):
    print("\nRequest headers:")
    for k, v in res.request.headers.items():
        print(f"{k}: {v}")


def print_response_headers(res):
    print("\nResponse headers:")
    for k, v in res.headers.items():
        print(f"{k}: {v}")


def main():
    numbers = ['15', '15/math', '15/year', '2/15',
               str(random.randint(0, 10**3)), f'{random.randint(-10**3, 10**3)}/math']
    for number in numbers:
        target_url = numbers_api_base_url + number
        response = requests.get(target_url)
        print(f"For '{number}' response: {response.text}")

    tickers = ['BTCUSDT', 'XRPUSDT']
    for ticker in tickers:
        response = requests.get(binance_api, params={'symbol': ticker})
        price_str = response.json()['price']
        price_float = float(price_str)
        print(f"Current {ticker} price: {price_float}")


if __name__ == '__main__':
    main()
