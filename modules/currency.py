import os
import requests
from services.mongodb import CurrencyRate, CurrencyRateSnapshot
from utils.logger import Logger
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


CURRENCY_RATE_ENDPOINT = os.getenv("CURRENCY_RATE_ENDPOINT")
DATE_FORMAT = "%A, %B %d %Y, %I:%M:%S %p"

FIGURE_NAME = "temp/figure.png"


class CurrenyModule:
    def __init__(self):
        self.logger = Logger(CurrenyModule.__name__)
        pass

    def get_previous_currency_rates(self):
        """Get most recent previous currency rates stored in database"""
        self.logger.log(f"Retrieving most recent previous currency rates")
        rate_snapshots = (
            CurrencyRateSnapshot.find(
                CurrencyRateSnapshot.origin == CURRENCY_RATE_ENDPOINT
            )
            .sort(-CurrencyRateSnapshot.created_at)
            .limit(7)
            .to_list()
        )

        # Get USD rates
        usd_rates = []
        for rate_snapshot in rate_snapshots:
            usd_rate = [rate for rate in rate_snapshot.rates if rate.code == "USD"][0]
            usd_rates.append(
                {
                    "date": rate_snapshot.created_at.strftime("%d/%m"),
                    "rate": usd_rate.tt_buy_rate,
                }
            )
        usd_rates.reverse()
        return usd_rates

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

    def plot_currency_graph(self):
        data = self.get_previous_currency_rates()

        if not data:
            self.logger.log(f"Not enough data to plot currency rates")
            return False

        self.logger.log(f"Plotting currency rates")

        df = pd.DataFrame(data)
        x = df["date"]
        y = df["rate"]

        plt.figure(figsize=(10, 7))

        plt.xticks(rotation=90)
        plt.plot(
            x,
            y,
            marker="H",
        )
        for i, txt in enumerate(y):
            plt.text(
                x[i],
                y[i] + 0.02,
                f"{y[i]:.2f}",
                ha="center",
                va="bottom",
                rotation=0,
                fontsize=20,
            )

        plt.savefig(FIGURE_NAME)
        self.logger.log(f"Figure saved to {FIGURE_NAME}")
        return True
