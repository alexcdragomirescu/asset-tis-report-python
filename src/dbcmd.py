import logging
import subprocess
import psutil
import time
import re
from end_session import end_session
from names import breakdown
from glob import glob
from copy_file import copy_file
import os
from remove import remove_file

logger = logging.getLogger(__name__)

class DbCmd(object):
    def __init__(self, host, port, sid, db_user, db_pass, log_dir):
        self.host = host
        self.port = port
        self.sid = sid
        self.db_user = db_user
        self.db_pass = db_pass
        self.log_dir = log_dir
    
    def run(self, dbc, dsn, pnum, dbc_user, dbc_pass, script):
        self.dbc = dbc
        self.dsn = dsn
        self.pnum = pnum
        self.dbc_user = dbc_user
        self.dbc_pass = dbc_pass
        self.script = script
        
        self.caller = subprocess.Popen([
            self.dbc,
            self.dsn,
            self.pnum,
            self.dbc_user,
            self.dbc_pass,
            self.script
        ])
        
        self.script_path_prefix, self.script_basename, self.script_filename, self.script_extension = breakdown(self.script)
        logger.info("Removing old dbcmd log files...")
        self.remove_log()
        
        logger.info("Executing dbcmd...")
        #end_session(self.host, self.port, self.sid, self.db_user, self.db_pass, self.dbc_user)
        self.ps = psutil.Process(self.caller.pid)
        self.counter = [0]
        try:
            while self.caller.poll() == None:
                self.counter[0] = 0
                logger.debug("Counter reset to \"0\".")
                mem = self.ps.memory_info().rss
                while mem == self.ps.memory_info().rss:
                    self.counter[0] += 1
                    logger.debug("Incremented counter by 1. Current value: \"" 
                        + str(self.counter[0]) + "\".")
                    if self.counter[0] == 3600:
                        logger.info("No change detected in memory usage. " 
                            + "Terminating process \"" + self.dbc 
                            + "\" with pid \"" + str(self.caller.pid) 
                            + "\"...")
                        self.ps.kill()
                        logger.info("Process terminated.")
                        logger.info("Removing user session \"" 
                            + dbc_user + "\"...")
                        #end_session(self.host, self.port, self.sid, self.db_user, self.db_pass, self.dbc_user)
                        
                        logger.info("Removing old logs tied to \"" 
                            + self.dbc + "\"script...")
                        self.remove_log()
                        return
                    mem = self.ps.memory_info().rss
                    time.sleep(1)
        except Exception:
            pass
        
        self.log_file = self.get_log()
        self.log_path_prefix, self.log_basename, self.log_filename, self.log_extension = breakdown(self.log_file)
        logger.info("Checking log file \"" + self.log_file + "\"...")
        
        lst = ['Your connection to Oracle Server has been lost. Please logout, and try to login again.',
                'Login Error:',
                'command due to read-only access to the project.']
                
        with open(self.log_file, "r") as f:
            for row in f:
                self.regex = re.findall(r"(?=(" + '.*|.*'.join(lst) + r"))", row)
                if self.regex:
                    logger.info("The log file \"" + 
                        self.log_file + "\" was found with \"" + self.regex 
                        + "\".")
                    #end_session(self.host, self.port, self.sid, self.db_user, self.db_pass, self.dbc_user)
                    self.run()
                    break
                    
        self.copy_log()
        
    def remove_log(self):
        for i in glob(self.script_path_prefix + '\\' + self.script_filename + '*.log'):
            remove_file(i)
            
    def copy_log(self):
        copy_file(self.log_file, os.path.join(self.log_dir, self.log_basename))
            
    def get_log(self):
        self.pathnames = glob(self.script_path_prefix + '\\' + self.script_filename + '*.log')
        self.log_file = max(self.pathnames, key=os.path.getctime)
        return self.log_file
            
        
        
        
        