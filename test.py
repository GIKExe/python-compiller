

import local
from local.utils import String

x = String('sas1 sas2 sas3 ')
print(x.wrap(4)[0].__class__)