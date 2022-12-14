import os
import sys
import csv
import logging
import socket
import subprocess
import distutils.dir_util
import openpyxl
import jinja2
import paramiko

from ssh import SSH
from names import breakdown
from zip import zip_dir
from lxml import etree
from copy_file import copy_file
from dbcmd import DbCmd
from datetime import datetime, timedelta
from remove import remove_files, remove_old_files, remove_tree
dt = datetime.now()
ts = dt.strftime('%Y%m%d%H%M%S')

wd = os.path.dirname(os.path.abspath(sys.argv[0]))
logs = os.path.join(wd, 'logs')

log = os.path.join(logs, 'python_' + str(ts) + '.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler(log),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Logging enabled.")
hostname = socket.gethostname()
main = os.path.basename(__file__)
logging.info("The script was executed from \"" + main + "\", located in the \
    path-prefix \"" + wd + "\" on the machine \"" + hostname + "\".")
    
logging.info("Removing old program logs...")
remove_old_files(logs, 7)

reports = os.path.join(wd, 'reports')
logging.info("Removing CSV files...")
remove_files(reports)


psexec = os.path.join(wd, 'psexec')
logging.info("Executing SQL queries...")
command = [
    os.path.join(psexec, 'PsExec.exe'), 
    '-accepteula', 
    '\\\\192.168.21.106', 
    r'E:\tis\tis.cmd'
]
p = subprocess.Popen(command)
p.wait()

t = r'\\192.168.21.106\e$\tis\output'
distutils.dir_util.copy_tree(t, reports)

asset = os.path.join(wd, 'asset')
logging.info("Removing ASSET data...")
remove_files(os.path.join(asset, '43'))
remove_files(os.path.join(asset, '44'))
remove_files(os.path.join(asset, '45'))
remove_files(os.path.join(asset, '46'))
remove_files(os.path.join(asset, '47'))
remove_files(os.path.join(asset, '48'))
remove_files(os.path.join(asset, '50'))
remove_files(os.path.join(asset, '51'))
remove_files(os.path.join(asset, '52'))
remove_files(os.path.join(asset, '53'))
remove_files(os.path.join(asset, '54'))
remove_files(os.path.join(asset, '55'))
remove_files(os.path.join(asset, '56'))
remove_files(os.path.join(asset, '57'))
remove_files(os.path.join(asset, '59'))
remove_files(os.path.join(asset, '60'))

log_dir = os.path.join(logs, 'tis_' + str(ts))
os.mkdir(log_dir)
dbcmd91 = DbCmd('EDITED', 'EDITED', 'EDITED', 'EDITED', 'EDITED', log_dir)
logging.info("Exporting ASSET data...")
dbcmd91.run(
    r'C:\Program Files\TEOCO\ENTERPRISE 9.1\DBCMD91.exe',
    '99_NEW_PROD_ASSET_91',
    '21',
    'EDITED',
    'EDITED',
    os.path.join(asset, 'export.txt')
)
logging.info("Done.")

data = []

with open(os.path.join(asset, '43', '43.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '43', 'PROPERTY-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID'), i.find('PROPERTY-CODE').text, j.get('EPSG'), j.find('X').text, j.find('Y').text] 
        for i in root.iterfind('.//PROPERTY') for j in i.iterfind('.//LOCATION')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '43', '43.csv'), os.path.join(reports, '43.csv'))


with open(os.path.join(asset, '44', '44.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '44', 'MU-NODE-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//MU-NODE')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '44', '44.csv'), os.path.join(reports, '44.csv'))


with open(os.path.join(asset, '45', '45.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '45', 'PROPERTY-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID'), i.find('PROPERTY-CODE').text] 
        for i in root.iterfind('.//PROPERTY')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '45', '45.csv'), os.path.join(reports, '45.csv'))


with open(os.path.join(asset, '46', '46.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '46', 'PROPERTY-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//PROPERTY')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '46', '46.csv'), os.path.join(reports, '46.csv'))


with open(os.path.join(asset, '47', '47.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '47', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '47', '47.csv'), os.path.join(reports, '47.csv'))


with open(os.path.join(asset, '48', '48.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '48', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '48', '48.csv'), os.path.join(reports, '48.csv'))


with open(os.path.join(asset, '50', '50.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '50', 'MU-NODE-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//MU-NODE')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '50', '50.csv'), os.path.join(reports, '50.csv'))


with open(os.path.join(asset, '51', '51.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '51', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '51', '51.csv'), os.path.join(reports, '51.csv'))


with open(os.path.join(asset, '52', '52.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '52', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '52', '52.csv'), os.path.join(reports, '52.csv'))


with open(os.path.join(asset, '53', '53.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    with open (os.path.join(wd, 'exclusions', '53.csv')) as exclusion:
        reader = csv.reader(exclusion)
        tree = etree.parse(os.path.join(asset, '53', 'GSM-CELL-LIST001.xml'))
        root = tree.getroot()
        data = [[i.get('ID')[0:8] + i.get('ID')[-1]] 
            for i in root.iterfind('.//GSM-CELL') if i.get('ID')[0:8] + i.get('ID')[-1] not in reader]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '53', '53.csv'), os.path.join(reports, '53.csv'))


with open(os.path.join(asset, '54', '54.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '54', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '54', '54.csv'), os.path.join(reports, '54.csv'))


with open(os.path.join(asset, '55', '55.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '55', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '55', '55.csv'), os.path.join(reports, '55.csv'))


with open(os.path.join(asset, '56', '56.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '56', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '56', '56.csv'), os.path.join(reports, '56.csv'))


with open(os.path.join(asset, '57', '57.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '57', 'GSM-CELL-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//GSM-CELL')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '57', '57.csv'), os.path.join(reports, '57.csv'))


with open(os.path.join(asset, '59', '59.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    with open (os.path.join(wd, 'exclusions', '53.csv')) as exclusion:
        reader = csv.reader(exclusion)
        tree = etree.parse(os.path.join(asset, '59', 'MU-NODE-LIST001.xml'))
        root = tree.getroot()
        data = [[i.get('ID') + '_' + '{:.2f}'.format(float(j.find('HGHT').text))] 
            for i in root.iterfind('.//MU-NODE') for j in i.iterfind('.//ANTENNA-CONFIG-LIST/ANTENNA') if i.get('ID') + '_' + '{:.2f}'.format(float(j.find('HGHT').text)) not in reader]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '59', '59.csv'), os.path.join(reports, '59.csv'))


with open(os.path.join(asset, '60', '60.csv'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    tree = etree.parse(os.path.join(asset, '60', 'MU-NODE-LIST001.xml'))
    root = tree.getroot()
    data = [[i.get('ID')] for i in root.iterfind('.//MU-NODE')]
    for row in data:
        csv_writer.writerows([row])
copy_file(os.path.join(asset, '60', '60.csv'), os.path.join(reports, '60.csv'))


tis_file_date = dt.strftime('%d.%m.%Y')
output = os.path.join(wd, 'output')
remove_files(output)
tis_filename = 'TIS_full report_' + str(tis_file_date) + '.xlsx'
tis_pathname = os.path.join(output, tis_filename)

templates = os.path.join(wd, 'templates')
copy_file(os.path.join(templates, 'tis.xlsx'), tis_pathname)
    

ranxg_files = (
    '1' ,'2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', 
    '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', 
    '28', '31', '32', '33', '34', '61', '64', '65', '66', '67', '68', '69', 
    '70', '71', '72', '73', '74', '75', '62a', '62b', '62c', '63a', '63b'
)

asset_files = (
    '43', '44', '45', '46', '47', '48', '50', '51', '52', '53', '54', '55', 
    '56', '57', '59', '60'
)

wb = openpyxl.load_workbook(tis_pathname)

for file in ranxg_files:
    sheet = wb[file.upper()]
    with open(os.path.join(reports, file + '.csv'), 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            sheet.append(row)
            
for file in asset_files:
    sheet = wb[file.upper()]
    with open(os.path.join(reports, file + '.csv'), 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            sheet.append(row)

logging.info("Saving TIS report...")
wb.save(tis_pathname)

log_basename = breakdown(log)[1]
logging.info("Copying the log at this point...")
copy_file(log, os.path.join(log_dir, log_basename))

archive_filename = 'tis_' + str(ts) + '.zip'
archive_pathname = os.path.join(logs, archive_filename)
logging.info("Archiving and compressing logs...")
zip_dir(log_dir, archive_pathname)
remove_tree(log_dir)

dt_end = datetime.now()
diff = dt_end - dt
days, seconds = diff.days, diff.seconds
hours = days * 24 + seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60

hts = dt.strftime('%A, %B %d %Y, %H:%M:%S %p')
event_end_hts = dt_end.strftime('%A, %B %d %Y, %H:%M:%S %p')

logging.info("Authoring admin email template...")
templateLoader = jinja2.FileSystemLoader(searchpath=templates)
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = 'admin.html'
template = templateEnv.get_template(TEMPLATE_FILE)
context = {
    'main': main,
    'wd': wd,
    'hostname': hostname,
    'ts': str(ts),
    'hts': str(hts),
    'event_end_hts': str(event_end_hts),
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
}

message_filename = 'tis_' + TEMPLATE_FILE
with open(os.path.join(wd, message_filename), 'wb') as f:
    f.write(template.render(**context).encode('utf-8'))

freetown_pk = paramiko.RSAKey.from_private_key(
    open(
        os.path.join(wd, 'freetown', 'id_rsa')
    )
)
freetown_ssh = SSH(hostname = '172.31.240.82', username = 'taskexec', pkey = freetown_pk)
freetown_ssh.sftp()
logging.info("Seding files to freetown...")
freetown_ssh._ftp.put(os.path.join(wd, message_filename), '/export/home/taskexec/send_mail/outbox/' + message_filename)
freetown_ssh._ftp.put(tis_pathname, '/export/home/taskexec/send_mail/outbox/' + tis_filename)
freetown_ssh._ftp.put(archive_pathname, '/export/home/taskexec/send_mail/outbox/' + archive_filename)
freetown_ssh.ssh('''python /export/home/taskexec/send_mail/mail.py \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --to 'EDITED' \
        --subject 'tis_report_{tis_file_date}' \
        --inline_attachment '/export/home/taskexec/send_mail/outbox/{message_filename}' \
        --attachment '/export/home/taskexec/send_mail/outbox/{tis_filename}' \
        --attachment '/export/home/taskexec/send_mail/outbox/{archive_filename}\''''.format(
        tis_file_date = str(tis_file_date), 
        message_filename = message_filename,
        tis_filename = tis_filename, 
        archive_filename = archive_filename,
    )
)
logging.info("Done.")
