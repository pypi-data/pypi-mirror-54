#   Copyright 2018 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import pandas as pd
import numpy as np
from .exceptions import ReindexMapError

def unionize_indices(dataset):
    """Return a union of all indices in a dataset, without duplicates.

    Parameters:
    dataset (dict of str: pandas DataFrame): The data dictionary containing the dataset.

    Returns:
    pandas Index: Union of all indices in the dataset, without duplicates.
    """
    indices = [df.index for df in dataset.values()]
    master_index = pd.Index([])
    for index in indices:
        master_index = master_index.union(index)
        master_index = master_index.drop_duplicates()
    return master_index

def generate_sample_status_col(df, normal_test):
    """Create a sample status column, called Sample_Tumor_Normal, for a dataframe.

    Parameters:
    df (pandas DataFrame): The dataframe to create a Sample_Status column for, indexed with Patient_IDs.
    normal_test (function): A function that takes a given Patient_ID and returns a bool indicating whether it corresponds to a normal sample.

    Returns:
    pandas Series: A sample status column for the dataframe.
    """
    sample_status_array = np.where(df.index.map(normal_test), "Normal", "Tumor")
    sample_status_col = pd.Series(data=sample_status_array, index=df.index.copy())
    return sample_status_col

def get_reindex_map(series):
    """Generate a reindexing map from a series where the index is the new indices, and the values are the old indices.

    Parameters:
    series (pandas Series): The series to generate the reindex map from.

    Returns:
    pandas Series: The reindexing map, with the old inidicies as the index, and the new indices as the values.
    """
    old_index_name = series.name
    new_index_name = series.index.name
    if new_index_name is None:
        new_index_name = "index" # This is the default name pandas gives unnamed indices when they're made columns

    # Check that the mapping is one to one
    series = series.dropna()
    if len(series) != len(series.drop_duplicates()):
        raise ReindexMapError("Reindex map is not one to one.")

    # Make the index the values, and the values the index
    df = series.reset_index()
    df = df.set_index(old_index_name)
    reindex_map = df[new_index_name]
    return reindex_map

def generate_sample_id_map(master_index):
    """Generate sample ids for all samples in a dataset, and map them to the existing index.

    Parameters:
    master_index (pandas Index): Union of all the indices in the dataset, without duplicates.

    Returns:
    dict: A dictionary with the old index values as the keys, and their corresponding sample ids as the values.
    """
    sample_id_dict = {}
    for i in range(len(master_index)):
        patient_id = master_index[i]
        sample_id_dict[patient_id] = "S{:0>3}".format(i + 1) # Use string formatter to give each sample id the format S*** filled with zeroes, e.g. S001, S023, or S112
    return sample_id_dict

def reindex_dataframe(df, reindex_map, new_index_name, keep_old):
    """Reindex a dataframe based on a mapping of the old index values to new ones.

    Parameters:
    df (pandas DataFrame): The dataframe to reindex.
    reindex_map (dict or pandas Series): A dictionary or pandas Series with the old index values as the keys or index, and the new ones as the values.
    new_index_name (str): The desired name for the new index.
    keep_old (bool): Whether to retain the old index in the dataframe as a column.

    Returns:
    pandas DataFrame: A copy of the given dataframe, with the new index.
    """
    if not df.index.isin(reindex_map.keys()).all(): # This works for a dict or a pandas Series, because Series have a .keys() attribute that's an alias for the index
        not_in = df.index[~(df.index.isin(reindex_map.keys()))]
        raise ReindexMapError(not_in)

    new_index = df.index.map(reindex_map.get)

    if keep_old:
        df = df.reset_index() # This gives the dataframe a numerical index and makes the old index a column, so it's not dropped when we set the new index.
    df.index = new_index
    df.index.name = new_index_name
    df = df.sort_index()
    return df
