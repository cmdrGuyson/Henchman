from modules.currency import CurrenyModule
from modules.email import EmailModule
from utils.logger import Logger
from templates.newsletter import main_template
from datetime import datetime


class Executor:
    def __init__(self):
        self.currency_module = CurrenyModule()
        self.email_module = EmailModule()
        self.logger = Logger(Executor.__name__)

    def execute_job(self):
        """Execute newsletter job"""
        self.logger.info("Executing newsletter job")
        try:
            self.logger.info("Successfully executed newsletter job")
            rates = self.currency_module.plot_currency_graph()

            if not rates:
                raise Exception("No rates found")

            current_rate = rates[-1].get("rate")
            today = datetime.now().strftime("%dth %B %Y")

            if not current_rate:
                raise Exception("No current currency rate")

            html_content = main_template.format("Gayanga", today, current_rate)

            self.email_module.set_html_content(html_content)
            self.email_module.set_subject(f"Henchman | {today}")
            self.email_module.attach_image(
                "/Users/guyson/Documents/Work/Henchman/temp/figure.png", "graph"
            )
            self.email_module.attach_image(
                "/Users/guyson/Documents/Work/Henchman/assets/icon.png", "logo"
            )

            self.email_module.send_email("gayangakuruppu@gmail.com")

        except Exception as e:
            self.logger.error(
                f"Something went wrong while executing newsletter job. error: {e}"
            )
