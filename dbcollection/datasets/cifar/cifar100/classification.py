"""
Cifar100 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py

from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


class Classification:
    """ Cifar100 Classification preprocessing functions """

    # extracted file names
    data_files = [
        "meta",
        "train",
        "test",
    ]

    # classes
    coarse_classes = [
        'aquatic mammals',
        'fish',
        'flowers',
        'food containers',
        'fruit and vegetables',
        'household electrical devices',
        'household furniture',
        'insects',
        'large carnivores',
        'large man-made outdoor things',
        'large natural outdoor scenes',
        'large omnivores and herbivores',
        'medium-sized mammals',
        'non-insect invertebrates',
        'people',
        'reptiles',
        'small mammals',
        'trees',
        'vehicles 1',
        'vehicles 2',
    ]

    finer_classes = [
        'beaver', 'dolphin', 'otter', 'seal', 'whale', \
        'aquarium fish', 'flatfish', 'ray', 'shark', 'trout', \
        'orchids', 'poppies', 'roses', 'sunflowers', 'tulips', \
        'bottles', 'bowls', 'cans', 'cups', 'plates', \
        'apples', 'mushrooms', 'oranges', 'pears', 'sweet peppers', \
        'clock', 'computer keyboard', 'lamp', 'telephone', 'television', \
        'bed', 'chair', 'couch', 'table', 'wardrobe', \
        'bee', 'beetle', 'butterfly', 'caterpillar', 'cockroach', \
        'bear', 'leopard', 'lion', 'tiger', 'wolf', \
        'bridge', 'castle', 'house', 'road', 'skyscraper', \
        'cloud', 'forest', 'mountain', 'plain', 'sea', \
        'camel', 'cattle', 'chimpanzee', 'elephant', 'kangaroo', \
        'fox', 'porcupine', 'possum', 'raccoon', 'skunk', \
        'crab', 'lobster', 'snail', 'spider', 'worm', \
        'baby', 'boy', 'girl', 'man', 'woman', \
        'crocodile', 'dinosaur', 'lizard', 'snake', 'turtle', \
        'hamster', 'mouse', 'rabbit', 'shrew', 'squirrel', \
        'maple', 'oak', 'palm', 'pine', 'willow', \
        'bicycle', 'bus', 'motorcycle', 'pickup truck', 'train', \
        'lawn-mower', 'rocket', 'streetcar', 'tank', 'tractor' \
    ]


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def get_object_list(self, data, fine_labels, coarse_labels):
        """
        Groups the data + labels info in a 'list' of indexes.
        """
        object_id = np.ndarray((data.shape[0], 3), dtype=int)
        for i in range(data.shape[0]):
            object_id[i][0] = i
            object_id[i][1] = fine_labels[i]
            object_id[i][2] = coarse_labels[i]
        return object_id


    def load_data(self):
        """
        Load the data from the files.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-100-python')

        # load classes name file
        class_names = load_pickle(os.path.join(data_path_, self.data_files[0]))

        # load train data files
        train_batch = load_pickle(os.path.join(data_path_, self.data_files[1]))

        train_data = train_batch['data'].reshape((50000, 3, 32, 32))
        train_data = np.transpose(train_data, (0, 2, 3, 1)) # NxHxWxC
        train_labels = np.array(train_batch['fine_labels'], dtype=np.uint8)
        train_coarse_labels = np.array(train_batch['coarse_labels'], dtype=np.uint8)
        train_object_list = self.get_object_list(train_data, train_labels, train_coarse_labels)

        # load test data file
        test_batch = load_pickle(os.path.join(data_path_, self.data_files[2]))

        test_data = test_batch['data'].reshape(10000, 3, 32, 32)
        test_data = np.transpose(test_data, (0, 2, 3, 1)) # NxHxWxC
        test_labels = np.array(test_batch['fine_labels'], dtype=np.uint8)
        test_coarse_labels = np.array(test_batch['coarse_labels'], dtype=np.uint8)
        test_object_list = self.get_object_list(test_data, test_labels, test_coarse_labels)

        #return a dictionary
        return {
            "train" : {
                "object_fields": ['images', 'classes', 'superclasses'],
                "data": train_data,
                "class_name": self.finer_classes,
                "coarse_class_name": self.coarse_classes,
                "labels": train_labels,
                "coarse_labels": train_coarse_labels,
                "object_id_list": train_object_list,
            },
            "test" : {
                "object_fields": str2ascii(['images', 'classes', 'superclasses']),
                "data": test_data,
                "class_name": str2ascii(self.finer_classes),
                "coarse_class_name": str2ascii(self.coarse_classes),
                "labels": test_labels,
                "coarse_labels": test_coarse_labels,
                "object_id_list": test_object_list,
            }
        }


    def process_metadata(self):
        """
        Process metadata and store it in a hdf5 file.
        """

        # load data to memory
        data = self.load_data()

        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'classification.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        # add data to the **source** group
        for set_name in ['train', 'test']:
            sourceg = fileh5.create_group('source/' + set_name)
            sourceg.create_dataset('classes', data=data[set_name]["class_name"], dtype=np.uint8)
            sourceg.create_dataset('superclasses', data=data[set_name]["coarse_class_name"], dtype=np.uint8)
            sourceg.create_dataset('images', data=data[set_name]["data"], dtype=np.uint8)
            sourceg.create_dataset('labels', data=data[set_name]["labels"], dtype=np.uint8)
            sourceg.create_dataset('coarse_labels', data=data[set_name]["coarse_labels"], dtype=np.uint8)

        # add data to the **default** group
        for set_name in ['train', 'test']:
            defaultg = fileh5.create_group('default/' + set_name)
            defaultg.create_dataset('classes', data=data[set_name]["class_name"], dtype=np.uint8)
            defaultg.create_dataset('superclasses', data=data[set_name]["coarse_class_name"], dtype=np.uint8)
            defaultg.create_dataset('images', data=data[set_name]["data"], dtype=np.uint8)
            defaultg.create_dataset('object_ids', data=data[set_name]["object_id_list"], dtype=np.int32)
            defaultg.create_dataset('object_fields', data=data[set_name]["object_fields"], dtype=np.uint8)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.process_metadata()