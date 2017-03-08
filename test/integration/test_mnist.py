#!/usr/bin/env python3


"""
Test downloading the mnist dataset.
"""


from __future__ import print_function
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(lib_path)
import dbcollection.manager as dbclt


# delete all cache data + dir
print('==> dbcollection.remove:\n')
dbclt.manage_cache(delete_cache=True, is_test=True)

# download/setup dataset
print('==> dbcollection.download:\n')
dbclt.setup(name='mnist', data_dir='/home/mf/tmp/download_data', verbose=True, is_test=True)

# download dataset
print('==> dbcollection.download:\n')
loader = dbclt.load(name='mnist', task='classification', verbose=True, is_test=True)

# print data from the loader
dbclt.info(is_test=True)

# print data from the loader
print('######### info #########\n')
print('Dataset: ' + loader.name)
print('Task: ' + loader.task)
print('Data path: ' + loader.data_dir)
print('Metadata cache path: ' + loader.cache_path)

# delete all cache data + dir
print('==> dbcollection.remove:\n')
dbclt.manage_cache(delete_cache=True, is_test=True)