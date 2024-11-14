# data_processing/main.py
from .process import Process
from .logger_config import logger

def send_alert_message(error_message):
    logger.critical(f"ALERT: {error_message}")

if __name__ == "__main__":
    data_source = "path/to/data_source"
    process = Process(data_source)

    try:
        process.run_process()
    except (DataCollectionError, DataQualityError, CalculationError, DatapackGenerationError) as e:
        error_message = f"Process failed: {e}"
        logger.critical(error_message)
        send_alert_message(error_message)
