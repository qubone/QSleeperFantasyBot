"""This module sets up a logger for the fantasy bot application.
It configures a logger named 'fantasy_bot' with DEBUG level logging by default,
and outputs log messages to the console with a specific format that includes
the timestamp, log level, and message.
Usage:
    logger.info("This is an info message.")
    logger.error("This is an error message.")
"""

import logging

# Create a logger
logger = logging.getLogger("fantasy_bot")
logger.setLevel(logging.INFO)  # Change to INFO or WARNING for production

# Create console handler and set level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

# Add formatter to handler
ch.setFormatter(formatter)

# Add handler to logger
logger.addHandler(ch)
