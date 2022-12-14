import logging
import os
import zipfile

logger = logging.getLogger(__name__)

def zip_dir(source, destination):
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zip:
        length = len(source)
        for root, dirs, files in os.walk(source):
            folder = root[length:]
            for file in files:
                zip.write(os.path.join(root, file), os.path.join(folder, file))
            
def zip_file(source, destination):
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write(source)
    