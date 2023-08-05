import os
import pandas as pd

from ztlearn.utils import maybe_download
from ztlearn.utils import train_test_split
from ztlearn.datasets.data_set import DataSet

URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

def fetch_iris(data_target = True, custom_path = os.getcwd()):
    file_path = maybe_download(custom_path + '/../../ztlearn/datasets/iris/', URL)
    describe  = [
        'sepal-length (cm)',
        'sepal-width (cm)',
        'petal-length (cm)',
        'petal-width (cm)',
        'petal_type'
    ]

    dataframe = pd.read_csv(file_path, names = describe)

    # convert petal type column to categorical data i.e {0:'Iris-setosa', 1:'Iris-versicolor', 2:'Iris-virginica'}
    dataframe.petal_type    = pd.Categorical(dataframe.petal_type)
    dataframe['petal_type'] = dataframe.petal_type.cat.codes

    data, target = dataframe.values[:,0:4], dataframe.values[:,4].astype('int')

    if data_target:
        return DataSet(data, target, describe)
    else:
        return train_test_split(data, target, test_size = 0.2, random_seed = 2)
