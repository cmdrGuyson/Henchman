import os
import requests
from services.mongodb import CurrencyRate, CurrencyRateSnapshot
from utils.logger import Logger
from datetime import datetime


CURRENCY_RATE_ENDPOINT = os.getenv("CURRENCY_RATE_ENDPOINT")
DATE_FORMAT = "%A, %B %d %Y, %I:%M:%S %p"


class CurrenyModule:
    def __init__(self):
        self.logger = Logger(CurrenyModule.__name__)
        pass

    def get_previous_currency_rates(self):
        """Get most recent previous currency rates stored in database"""
        self.logger.log(f"Retrieving most recent previous currency rates")
        rates = (
            CurrencyRateSnapshot.find(
                CurrencyRateSnapshot.origin == CURRENCY_RATE_ENDPOINT
            )
            .sort(-CurrencyRateSnapshot.created_at)
            .limit(7)
            .to_list()
        )

        return rates

    def get_currency_rates(self):
        """Scrape and return bank currency rates endpoint"""

        self.logger.log(
            f"Scraping {CURRENCY_RATE_ENDPOINT} for currency rate information"
        )

        response = requests.get(CURRENCY_RATE_ENDPOINT)

        if response.status_code != 200:
            self.logger.error(
                f"Failed to retrieve currency rates from: {CURRENCY_RATE_ENDPOINT}"
            )
            return None

        output = response.json()

        if not output and not output.get("data"):
            self.logger.warn("Currency rates not available")
            return None

        rates = []

        for raw_rate in output["data"]:
            rate = CurrencyRate(
                code=raw_rate.get("CurrCode"),
                label=raw_rate.get("CurrName"),
                od_buy_rate=raw_rate.get("ODBUY"),
                tt_buy_rate=raw_rate.get("TTBUY"),
                tt_sell_rate=raw_rate.get("TTSEL"),
                updated_at=datetime.strptime(raw_rate.get("RateWEF"), DATE_FORMAT),
            )
            rates.append(rate)

        self.logger.log("Saving currency rates")
        snapshot = CurrencyRateSnapshot(
            created_at=datetime.utcnow(), origin=CURRENCY_RATE_ENDPOINT, rates=rates
        )
        # snapshot.save()
        self.logger.log("Currency rates saved")
        return snapshot
