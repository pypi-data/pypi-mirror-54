
# Json Decoder
This is Json Decoder utility project which decode JSON response into dictionary/list.

## Installation
Run Following Command to install:
``` Python
pip install JsonDecoderUtility
```

## Example Json Strcuture
    {
        "status": {
            "timestamp": "2019-10-29T09:53:32.713Z",
            "error_code": 0,
            "error_message": null,
            "elapsed": 11,
            "credit_count": 1,
            "notice": null
        },  
        data: [
                {
                    "id": 1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "slug": "bitcoin",
                    "num_market_pairs": 7839,
                    "date_added": "2013-04-28T00:00:00.000Z",
                    "tags": [
                        "mineable"
                    ],
                    "max_supply": 21000000,
                    "circulating_supply": 18018712,
                    "total_supply": 18018712,
                    "platform": null,
                    "cmc_rank": 1,
                    "last_updated": "2019-10-29T09:52:38.000Z",
                    "quote": {
                        "INR": {
                            "price": 667560.1128484675,
                            "volume_24h": 1970166977183.0684,
                            "percent_change_1h": -0.2029636,
                            "percent_change_24h": 0.36647437,
                            "percent_change_7d": 14.05843774,
                            "market_cap": 12028573416104.035,
                            "last_updated": "2019-10-29T09:53:01.000Z"
                        }
                    }
                }
            ]
    }
