import logging

# Create a logger
logger = logging.getLogger("fantasy_bot")
logger.setLevel(logging.DEBUG)  # Change to INFO or WARNING for production

# Create console handler and set level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

# Add formatter to handler
ch.setFormatter(formatter)

# Add handler to logger
logger.addHandler(ch)
