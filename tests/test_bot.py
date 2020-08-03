
import bot
import csv
import io

def test_fetch_api():
    stock = bot.fetch_stock('aapl.us')

    f = io.StringIO(stock)
    reader = csv.DictReader(f)

    for row in reader:

        assert row['Symbol'] == 'AAPL.US'
        assert 'Close' in row

