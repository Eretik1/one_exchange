import requests
import pprint
import time
import threading
import keyboard

def request_for_bitget():
    urlETCBTC = 'https://api.bitget.com/api/v2/spot/market/orderbook?symbol=ETCBTC&type=step0&limit=100'
    urlBTCUSDT = 'https://api.bitget.com/api/v2/spot/market/orderbook?symbol=BTCUSDT&type=step0&limit=100'
    urlETCUSDT = 'https://api.bitget.com/api/v2/spot/market/orderbook?symbol=ETCUSDT&type=step0&limit=100'
    responseETCBTC = requests.get(urlETCBTC)
    responseBTCUSDT = requests.get(urlBTCUSDT)
    responseETCUSDT = requests.get(urlETCUSDT)
    dataETCBTC = responseETCBTC.json()
    dataBTCUSDT = responseBTCUSDT.json()
    dataETCUSDT = responseETCUSDT.json()
    data = { 
        "BTCUSDT" :
        [dataBTCUSDT["data"]['asks'][0], dataBTCUSDT["data"]['bids'][0]],
        "ETHUSDT" :
        [dataETCUSDT["data"]['asks'][0], dataETCUSDT["data"]['bids'][0]],
        "ETHBTC" :
        [dataETCBTC["data"]['asks'][0], dataETCBTC["data"]['bids'][0]]
    }
    return data 

stop = True 
data_from_bitget = 0
def continuous_function():
    global stop
    global data_from_bitget
    while stop:
        data_from_bitget = request_for_bitget()
        USDT = 5
        navar1 = ( USDT / float(data_from_bitget["BTCUSDT"][0][0])) / float(data_from_bitget["ETHBTC"][0][0]) * float(data_from_bitget["ETHUSDT"][1][0]) - USDT 
        navar2 = ( USDT / float(data_from_bitget["ETHUSDT"][0][0])) * float(data_from_bitget["ETHBTC"][1][0]) * float(data_from_bitget["BTCUSDT"][1][0]) - USDT
        com1 = USDT / 100 * 0.01 * 3
        pprint.pprint(data_from_bitget)
        print(USDT, " USDT")
        print("USDT --> BTS --> ETH --> USDT", navar1, "   ", com1, "   ", navar1 - com1)
        print("USDT --> ETH --> BTS --> USDT", navar2, "   ", com1, "   ", navar2 - com1)
        time.sleep(5)

def stop_function():
    global stop
    while stop:
        if keyboard.is_pressed('q'):
            stop = False
    print("Оба потока остановлены.")

def action():
    thread1 = threading.Thread(target=continuous_function)
    thread2 = threading.Thread(target=stop_function)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()