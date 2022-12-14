import logging
import shutil
import distutils.dir_util

logger = logging.getLogger(__name__)

def copy_files(source, destination):
    try:
        distutils.dir_util.copy_tree(source, destination)
    except (OSError, PermissionError) as e:
        logger.exception("Failed to copy tree \"" + source 
            + "\" to destination\"" + destination + "\".")
    else:
        logger.info("Successfully copied tree \"" + source 
            + "\" to destination\"" + destination + "\".")
        
def copy_file(source, destination):
    try:
        shutil.copy2(source, destination)
    except (OSError, PermissionError) as e:
        logger.exception("Failed to copy pathname \"" + source 
            + "\" to destination\"" + destination + "\".")
    else:
        logger.info("Successfully copied pathname \"" + source 
            + "\" to destination\"" + destination + "\".")