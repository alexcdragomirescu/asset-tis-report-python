import logging
import os
from glob import glob
from stat import S_ISREG, ST_CTIME, ST_MODE
import shutil
import re
import time

logger = logging.getLogger(__name__)

def remove_files(path_prefix):
    for pathname in glob(path_prefix + '\\*.*'):
        try:
            os.remove(pathname)
        except (OSError, PermissionError) as e:
            logger.exception("Failed to remove pathname \"" + pathname + "\".")
        else:
            logger.info("Successfully removed pathname \"" + pathname + "\".")
                
def remove_file(pathname):
    try:
        os.remove(pathname)
    except (OSError, PermissionError) as e:
        logger.exception("Failed to remove pathname \"" + pathname + "\".")
    else:
        logger.info("Successfully removed pathname \"" + pathname + "\".")
        
def remove_tree(path_prefix):
    try:
        shutil.rmtree(path_prefix)
    except (OSError, PermissionError) as e:
        logger.exception("Failed to remove path-prefix \"" + path_prefix + "\".")
    else:
        logger.info("Successfully removed path-prefix \"" + path_prefix + "\".")
    
        
def remove_old_nth_files(pp, file_number):
    pathnames = [os.path.join(pp, filename) for filename in os.listdir(pp)]
    file_stats = [(os.stat(pp), pp) for pp in pathnames]
    sorted_pathnames = sorted([(stat[ST_CTIME], pp) for stat, pp in file_stats if S_ISREG(stat[ST_MODE])])
    result = [pp for stat, pp in sorted_pathnames[:-file_number]]

    for pp in result:
        try:
            os.remove(pp)
        except (OSError, PermissionError) as e:
            logger.exception("Failed to remove pathname \"" + pp + "\".")
        else:
            logger.info("Successfully removed pathname \"" + pp + "\".")
            
def remove_old_files(path_prefix, days):
    now = time.time()
    
    for pathname in os.listdir(path_prefix):
        if os.path.getmtime(os.path.join(path_prefix, pathname)) < now - days * 86400:
            if os.path.isfile(os.path.join(path_prefix, pathname)):
                os.remove(os.path.join(path_prefix, pathname))
                