import logging
import os
import inspect
from datetime import datetime

# Create a logs directory if it doesn't exist
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Generate the log file name based on the current time
log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
log_file_path = os.path.join(logs_dir, log_file_name)

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_file_path)
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(module)s - %(filename)s - Line: %(lineno)d - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(module)s - %(filename)s - Line: %(lineno)d - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def log_task(task_description):
    """
    Log the time, line of code, task executed, folder, and file name.
    :param task_description: Description of the task being logged
    """
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_code.co_filename)
    lineno = frame.f_lineno
    module = frame.f_globals["__name__"]
    folder = os.path.dirname(os.path.abspath(frame.f_code.co_filename))
    logger.debug(f"Task: {task_description} | Folder: {folder} | File: {filename} | Line: {lineno}")


