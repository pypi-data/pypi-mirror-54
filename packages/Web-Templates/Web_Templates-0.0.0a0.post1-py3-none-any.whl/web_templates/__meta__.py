"""

Versioning
==========

:pep:`0440` describes the versioning of a Python package.
"""

__project__ = "Web-Templates" # PReviously Django-Templates
__summary__ = "Standardized templates for Python's web frameworks"

__company__ = 'Manaikan'
__website__ = 'https://gitlab.com/manaikan/web-templates/'

__author__  = 'Carel van Dam'
__e_mail__  = 'carelvdam@gmail.com'

__release__ = (0,0,0) # (major.minor.micro)
__version__ = __release__[:-1]
__develop__ = None
__postnum__ = 1
__prostat__ = ("Alpha", 0) # rlscddt/status

__version__ = ".".join([str(item) for item in __version__])
__release__ = ".".join([str(item) for item in __release__]) \
            + {None    : lambda value : "".format(value)     if value is not None else "",
               "Alpha" : lambda value : "a{}".format(value)  if value is not None else "",
               "Beta"  : lambda value : "b{}".format(value)  if value is not None else "",
               "RC"    : lambda value : "rc{}".format(value) if value is not None else "",}[__prostat__[0]](__prostat__[1]) \
            + (".post{}".format(__postnum__) if __postnum__ is not None else "") \
            + (".dev{}".format(__develop__)  if __develop__ is not None else "") # [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
