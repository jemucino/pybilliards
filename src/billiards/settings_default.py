# The default system settings

import os

settings = {'defaultdatadir': 'data',
            'systemdatadir' : os.path.join('/etc','pybilliards','data'),
            'userdatadir'   : os.path.join(os.path.expanduser('~'),'.config','pybilliards','data'),
            'userdir'       : os.path.join(os.path.expanduser('~'),'.config','pybilliards'),
            'loglevel'      : 'debug',
            'theme'         : 'default',
            }