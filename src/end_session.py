import logging
import cx_Oracle

logger = logging.getLogger(__name__)

def end_session(host, port, sid, db_user, db_pass, dbc_user):
    dsn = cx_Oracle.makedsn(host, port, sid)
    conn = cx_Oracle.connect(db_user, db_pass, dsn)
    
    cur = conn.cursor()
    
    select = """
        SELECT * FROM NETWORK_PLANNING.ENT_ACTIVELOGON_DATA 
        WHERE USERID = :username
    """
    
    delete = """
        DELETE FROM NETWORK_PLANNING.ENT_ACTIVELOGON_DATA 
        WHERE USERID = :username
    """
    
    cur.prepare(select)
    cur.execute(None, {'username':dbc_user.upper()})
    res = cur.fetchall()
    if len(res) == 0:
        logger.info("User session for \"" + dbc_user + "\" does not exist.")
        return
    cur.prepare(delete)
    assert cur.execute(None, {'username':dbc_user.upper()}), "Failed to remove user session\"" + dbc_user + "\"."
    logger.info("User session \"" + dbc_user + "\" sucsesfully removed.")
    conn.commit()
    
    cur.close()
    conn.close()
    