default_app_config = 'cq.apps.CqConfig'

VERSION = (0, 3, 3)

__version__ = '.'.join(str(x) for x in VERSION[:(2 if VERSION[2] == 0 else 3)])  # noqa
