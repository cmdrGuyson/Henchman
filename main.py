from flask import Flask
from flask_apscheduler import APScheduler
import os
from dotenv import load_dotenv
import matplotlib

from ochestrators.executor import Executor

load_dotenv()
matplotlib.use("agg")

PORT = os.getenv("PORT", 8000)

app = Flask(__name__)


# Initialize scheduler
scheduler = APScheduler()


def job():
    executor = Executor()
    executor.execute_job()


@scheduler.task(
    "cron",
    id="newsletter_job",
    hour=10,
    timezone="Asia/Colombo",
)
def newsletter_job():
    job()


@app.route("/health")
def health():
    return {"status": True}, 200


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(
        host="0.0.0.0",
        port=PORT,
    )
