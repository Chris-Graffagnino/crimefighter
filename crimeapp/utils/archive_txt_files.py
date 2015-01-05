import os
import subprocess

files = os.listdir('./')

for file in files:
    if file[-3:] in ['txt']:
        subprocess.call(['mv', file, 'booking_archive'])
