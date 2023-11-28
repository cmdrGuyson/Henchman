from modules.currency import CurrenyModule
from modules.email import EmailModule
from utils.logger import Logger
from templates.newsletter import main_template
from datetime import datetime, date
import os

OCHESTRATOR_DIR = os.path.dirname(os.path.abspath(__file__))
HENCHMAN_DIR = os.path.dirname(OCHESTRATOR_DIR)
TEMP_DIR = os.path.join(HENCHMAN_DIR, "temp")
ASSETS_DIR = os.path.join(HENCHMAN_DIR, "assets")


class Executor:
    def __init__(self):
        self.currency_module = CurrenyModule()
        self.email_module = EmailModule()
        self.logger = Logger(Executor.__name__)

    def execute_job(self):
        """Execute newsletter job"""

        self.logger.info("Executing newsletter job")

        today = date.today()
        if not today.isoweekday() < 6:
            self.logger.info("Skipping newsletter execution on weekend")
            return

        try:
            self.logger.info("Successfully executed newsletter job")
            self.currency_module.get_currency_rates()
            rates = self.currency_module.plot_currency_graph()

            if not rates:
                raise Exception("No rates found")

            current_rate = rates[-1].get("rate")
            current_day = datetime.now().strftime("%dth %B %Y")

            if not current_rate:
                raise Exception("No current currency rate")

            html_content = main_template.format("Gayanga", current_day, current_rate)

            self.email_module.set_html_content(html_content)
            self.email_module.set_subject(f"Henchman | {current_day}")
            self.email_module.attach_image(
                os.path.join(TEMP_DIR, "figure.png"), "graph"
            )
            self.email_module.attach_image(os.path.join(ASSETS_DIR, "icon.png"), "logo")

            self.email_module.send_email("gayangakuruppu@gmail.com")

        except Exception as e:
            self.logger.error(
                f"Something went wrong while executing newsletter job. error: {e}"
            )
