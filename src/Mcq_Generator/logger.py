import logging
import os
import inspect
from datetime import datetime

def create_logger():
    """
    Create a logger that logs to a unique file named by the current timestamp.
    """
    # Create a logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Generate the log file name based on the current time
    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_file_path = os.path.join(logs_dir, log_file_name)

    # Create a custom logger
    logger = logging.getLogger(log_file_name)  # Use the log file name as the logger name

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create handlers
    f_handler = logging.FileHandler(log_file_path)
    f_handler.setLevel(logging.DEBUG)

    # Create formatter and add it to handler
    f_format = logging.Formatter('%(asctime)s - %(module)s - %(filename)s - Line: %(lineno)d - %(message)s')
    f_handler.setFormatter(f_format)

    # Add handler to the logger
    logger.addHandler(f_handler)

    return logger

def log_task(task_description):
    """
    Log the time, line of code, task executed, folder, and file name.
    :param task_description: Description of the task being logged
    """
    logger = create_logger()  # Create a new logger with a unique log file
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_code.co_filename)
    lineno = frame.f_lineno
    module = frame.f_globals["__name__"]
    folder = os.path.dirname(os.path.abspath(frame.f_code.co_filename))
    logger.debug(f"Task: {task_description} | Folder: {folder} | File: {filename} | Line: {lineno}")
    logger.handlers.clear()  # Clear handlers to avoid duplicate logs in subsequent calls
