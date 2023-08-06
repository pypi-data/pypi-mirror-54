from fake_useragent import UserAgent
from shadow_useragent import ShadowUserAgent
import shadow_useragent
import logging
import os
import tempfile
import sys
from os.path import pardir, sep
import shutil

sys.path.append(pardir + sep + ".")


DB = os.path.join(
    tempfile.gettempdir(),
    'fake_useragent_0.1.11.json'
    )


this_dir, this_filename = os.path.split(__file__)

DATA_PATH = os.path.join(this_dir, "useragents.json")

if not os.path.isfile(DB):
    shutil.copy(DATA_PATH, DB)
else:
    if os.stat(DB).st_size==0:
        shutil.copy(DATA_PATH,DB)



class AgentManager():

    manager_dft = 'shadow'
    manager_d = {
        'fake'   : UserAgent(cache=True),
        'shadow' : ShadowUserAgent()
    }
    manager_name = None


    def __init__(self, **kwargs):
        for k in kwargs.keys():
            self.__dict__[k] = kwargs[k]
        if not self.manager_name:
            self.manager_name = self.manager_dft       


    def random(self):
        if self.manager_name == 'shadow':
            return self.manager_d[self.manager_name].random_nomobile
        if self.manager_name == 'fake':
            return self.manager_d[self.manager_name].random
            




