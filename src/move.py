import logging
import os

logger = logging.getLogger(__name__)

def move_file(source, destination):
    try:
        os.rename(source, destination)
    except (OSError, PermissionError) as e:
        logger.exception("Failed to move pathname \"" + source 
            + "\" to destination\"" + destination + "\".")
    else:
        logger.info("Successfully moved pathname \"" + source 
            + "\" to destination\"" + destination + "\".")
            