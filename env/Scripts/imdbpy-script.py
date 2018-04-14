#!c:\users\zuyich~1\cs411f~1\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'IMDbPY==6.5.dev20180414','console_scripts','imdbpy'
__requires__ = 'IMDbPY==6.5.dev20180414'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('IMDbPY==6.5.dev20180414', 'console_scripts', 'imdbpy')()
    )
