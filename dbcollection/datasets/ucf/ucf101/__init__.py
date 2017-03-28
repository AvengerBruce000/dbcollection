"""
UCF101-Action recognition download/process functions.
"""


from __future__ import print_function, division
from dbcollection.utils.url import download_extract_all

from .recognition import Recognition


class UCF101:
    """ UCF101-Action recognitio preprocessing/downloading functions """

    # download url
    url = [
        'http://crcv.ucf.edu/data/UCF101/UCF101.rar',
        'http://crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-RecognitionTask.zip',
        'http://crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-DetectionTask.zip'
    ]
    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'recognition',
                'activity', 'human', 'single person']


    def __init__(self, data_path, cache_path, extract_data, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.extract_data = extract_data
        self.verbose = verbose


    def download(self):
        """
        Download and extract files to disk.
        """
        # download + extract data and remove temporary files
        download_extract_all(self.url, self.md5_checksum, self.data_path,
                             self.extract_data, self.verbose)

        return self.keywords


    def process(self):
        """
        Process metadata for all tasks
        """
        # init tasks
        tasks = {
            "recognition": Recognition(self.data_path, self.cache_path, self.verbose)
        }

        # process all tasks
        info_output = {}
        for task in tasks:
            if self.verbose:
                print('Processing ::{}:: task:\n'.format(task))
            info_output[task] = tasks[task].run()

        # define a default task
        info_output['default'] = info_output['recognition']

        return info_output, self.keywords