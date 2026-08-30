from os import walk, path, remove
from zipfile import ZipFile, ZIP_DEFLATED

def zipfile_dir(zip_path):
    if path.exists(f'{zip_path}.apworld'):
        remove(f'{zip_path}.apworld')
    with ZipFile(f'{zip_path}.apworld', 'x', ZIP_DEFLATED) as myzip:
        for (root,dirs,files) in walk(zip_path):
            for file in files:
                current_path = f'{root}\\{file}'
                myzip.write(current_path)
    print('manual_sekiro.apworld Written')