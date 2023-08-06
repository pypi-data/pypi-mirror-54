from jsondecoder import JsonDecoder

if __name__ == "__main__":
    curr = input("Enter Currency: ")
    symbol = input("Enter Crypto:")
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=e14b9347-6f38-42ae-8300-58cdc35af2f9&start=1&limit=3&convert='+curr
    # coinmarket = JsonDecoder(
    #    'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=e14b9347-6f38-42ae-8300-58cdc35af2f9&start=1&limit=10&convert=INR')
    coinmarket = JsonDecoder(url)

    coinmarket.get_content_from_url(curr, symbol)
