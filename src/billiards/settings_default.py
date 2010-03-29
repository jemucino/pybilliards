# The default system settings

import os

__datadir = os.path.join(os.path.dirname(__file__),'data')
if not os.path.exists(__datadir):
    import sys
    try:
        if sys.frozen == 1:
            # for executables built using pyinstaller
            try:
                __datadir = os.path.join(os.environ['_MEIPASS2'], 'data')
            except KeyError:
                __datadir = os.path.join(os.path.dirname(sys.executable), 'data')
    except AttributeError:
        pass

settings = {'defaultdatadir': __datadir,
            'systemdatadir' : os.path.join('/etc','pybilliards','data'),
            'userdatadir'   : os.path.join(os.path.expanduser('~'),'.config','pybilliards','data'),
            'userdir'       : os.path.join(os.path.expanduser('~'),'.config','pybilliards'),
            'loglevel'      : 'debug',
            'theme'         : 'default',
            }