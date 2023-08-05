# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for validation and conversion."""
from typing import Any, cast, Dict, List, Optional, Tuple, Union

import json
import re
import traceback
import warnings
import numpy as np
import pandas as pd
import pandas.api as api
import scipy
from math import sqrt

from automl.client.core.common.exceptions import DataException
from automl.client.core.common.utilities import get_value_from_dict
from automl.client.core.runtime.types import DataInputType
from sklearn import model_selection


# For backward compatibility

SOURCE_WRAPPER_MODULE = 'automl.client.core.runtime.model_wrappers'
MAPPED_WRAPPER_MODULE = 'azureml.train.automl.model_wrappers'


def extract_user_data(user_script: Any) -> Dict[str, Optional[Union[np.array, List[str], float, List[int]]]]:
    """
    Extract data from user's module containing get_data().

    This method automatically runs during an automated machine learning experiment.
    Arguments:
        user_script {module} -- Python module containing get_data() function.

    Raises:
        DataException -- Get data script was not defined and X, y inputs were not provided.
        DataException -- Could not execute get_data() from user script.
        DataException -- Could not extract data from user script.

    Returns:
        dict -- Dictionary containing
        X_train, y_train, sample_weight, X_valid, y_valid,
        sample_weight_valid, cv_splits_indices.

    """
    if user_script is None:
        raise DataException(
            "Get data script was not defined and X,"
            " y inputs were not provided.")
    try:
        output = user_script.get_data()         # type: Union[Dict[str, Any], Tuple[Any, Any, Any, Any]]
    except Exception as ex:
        raise DataException("Could not execute get_data() from user script. Exception: {}".format(ex)) from None
    if isinstance(output, dict):
        return _extract_data_from_dict(output)
    elif isinstance(output, tuple):
        return _extract_data_from_tuple(output)
    else:
        raise DataException("The output of get_data() from user script is not a dict or a tuple.")


def _get_indices_missing_labels_output_column(y: DataInputType) -> np.ndarray:
    """
    Return the indices of missing values in y.

    :param y: Array of training labels
    :return: Array of indices in y where the value is missing
    """
    if np.issubdtype(y.dtype, np.number):
        return np.argwhere(np.isnan(y)).flatten()
    else:
        # Cast needed as numpy-stubs thinks None is not an allowed input to np.where
        return np.argwhere((y == "nan") | np.equal(y, cast(np.ndarray, None))).flatten()


def _y_nan_check(output: Dict[str, Union[pd.DataFrame, np.array]]) -> \
        Dict[str, Optional[Union[np.array, List[str], float, List[int]]]]:
    """
    Check for nans in y.

    Keyword Arguments:
        output {dict} -- dictionary containing the output to check. (default: {None})

    Raises:
        DataException -- All label data is NaN.

    Returns:
        dict -- dictionary containing checked output.

    """
    y = output['y']
    X = output['X']
    sample_weight = output['sample_weight']
    if y is not None and pd.isnull(y).any():
        warnings.warn(
            "Labels contain NaN values. Removing for AutoML Experiment.")
        y_indices_pruned = ~pd.isnull(y)
        X_reduced = X[y_indices_pruned]
        y_reduced = y[y_indices_pruned]
        sample_weight_reduced = None
        if sample_weight is not None:
            sample_weight_reduced = sample_weight[y_indices_pruned]
        if y_reduced.shape[0] == 0:
            raise DataException('All label data is NaN.')
        output['X'] = X_reduced
        output['y'] = y_reduced
        output['sample_weight'] = sample_weight_reduced
    y_valid = output['y_valid']
    X_valid = output['X_valid']
    sample_weight_valid = output['sample_weight_valid']
    if y_valid is not None and pd.isnull(y_valid).any():
        warnings.warn(
            "Validation Labels contain NaN values. "
            "Removing for AutoML Experiment.")
        y_valid_indices_pruned = ~pd.isnull(y_valid)
        X_valid_reduced = X_valid[y_valid_indices_pruned]
        y_valid_reduced = y_valid[y_valid_indices_pruned]
        sample_weight_valid_reduced = None
        if sample_weight_valid is not None:
            sample_weight_valid_reduced = \
                sample_weight_valid[y_valid_indices_pruned]
        output['X_valid'] = X_valid_reduced
        output['y_valid'] = y_valid_reduced
        output['sample_weight_valid'] = sample_weight_valid_reduced
    return output


def _extract_data_from_tuple(
        output: Tuple[Union[pd.DataFrame, np.array], Union[pd.DataFrame, np.array],
                      Union[pd.DataFrame, np.array], Union[pd.DataFrame, np.array]]) \
        -> Dict[str, Optional[Union[np.array, List[str], float, List[int]]]]:
    """
    Extract user data if it is passed as a tuple.

    Arguments:
        output {tuple} -- tuple containing user data.

    Raises:
        DataException -- Could not extract X, y from get_data() in user script. get_data only output {0} values.

    Returns:
        tuple -- tuple containing X_train, y_train, X_test, y_test

    """
    X_valid, y_valid = None, None
    if len(output) < 2:
        raise DataException("Could not extract X, y from get_data() in user "
                            "script. get_data only output {0} values."
                            .format(len(output))) from None
    x_raw_column_names = None
    X = output[0]
    y = output[1]
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
        X = X.values
    if isinstance(y, pd.DataFrame):
        y = y.values

    if len(output) >= 4:
        X_valid = output[2]
        y_valid = output[3]
        if isinstance(y_valid, pd.DataFrame):
            y_valid = y_valid.values
        if isinstance(X_valid, pd.DataFrame):
            X_valid = X_valid.values

    return {
        "X": X,
        "y": y,
        "sample_weight": None,
        "x_raw_column_names": x_raw_column_names,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": None,
        "X_test": None,
        "y_test": None,
        "cv_splits_indices": None,
    }


def _extract_data_from_dict(output: Dict[str, Any]) -> \
        Dict[str, Optional[Union[np.array, List[str], float, List[int]]]]:
    """
    Extract user data if it is passed as a dictionary.

    Arguments:
        output {dict} -- dictionary containing user data and metadata.

    Raises:
        DataException -- Invalid data or encountered processing issues.

    Returns:
        dict -- Dictionary containing AutoML relevant data.

    """
    X = get_value_from_dict(output, ['X'], None)
    y = get_value_from_dict(output, ['y'], None)
    sample_weight = get_value_from_dict(output, ['sample_weight'], None)
    X_valid = get_value_from_dict(output, ['X_valid'], None)
    y_valid = get_value_from_dict(output, ['y_valid'], None)
    sample_weight_valid = get_value_from_dict(
        output, ['sample_weight_valid'], None)
    X_test = get_value_from_dict(output, ['X_test'], None)
    y_test = get_value_from_dict(output, ['y_test'], None)
    data = get_value_from_dict(output, ['data_train'], None)
    columns = get_value_from_dict(output, ['columns'], None)
    label = get_value_from_dict(output, ['label'], None)
    cv_splits_indices = get_value_from_dict(
        dictionary=output,
        names=["cv_splits_indices"], default_value=None)
    x_raw_column_names = None

    if data is not None:
        if label is None and X is None and y is None:
            raise DataException('Pandas data array received without a label. '
                                'Please add a ''label'' element to the '
                                'get_data() output.')
        if not isinstance(label, list):
            assert(isinstance(label, str) or isinstance(label, int))
            label = [label]
        y_extracted = data[label].values
        X_extracted = data[data.columns.difference(label)]
        if columns is not None:
            X_extracted = X_extracted[X_extracted.columns.intersection(
                columns)]

        if X is None and y is None:
            X = X_extracted
            y = y_extracted
        else:
            if np.array_equiv(X, X_extracted.values):
                raise DataException(
                    "Different values for X and data were provided. "
                    "Please return either X and y or data and label.")
            if np.array_equiv(y, y_extracted.values):
                raise DataException(
                    "Different values for y and label were provided. "
                    "Please return either X and y or data and label.")
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
        X = X.values
    if isinstance(X_valid, pd.DataFrame):
        X_valid = X_valid.values
    if isinstance(X_test, pd.DataFrame):
        X_test = X_test.values
    if isinstance(y, pd.DataFrame):
        y = y.values
    if isinstance(y_valid, pd.DataFrame):
        y_valid = y_valid.values
    if isinstance(y_test, pd.DataFrame):
        y_test = y_test.values

    if X is None:
        raise DataException(
            "Could not retrieve X train data from get_data() call. "
            "Please ensure you are either returning either "
            "{X_train: <numpy array>, y_train: <numpy array>"
            "or {data: <pandas dataframe>, label: <string>")
    if y is None:
        raise DataException(
            "Could not retrieve y train data from get_data() call. "
            "Please ensure you are either returning either "
            "{X_train: <numpy array>, y_train: <numpy array>"
            "or {data: <pandas dataframe>, label: <string>")

    if (X_valid is None) is not (y_valid is None):
        raise DataException(
            'Received only one of X_valid or y_valid.'
            'Either both or neither value should be provided.')

    return {
        "X": X,
        "y": y,
        "x_raw_column_names": x_raw_column_names,
        "sample_weight": sample_weight,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": sample_weight_valid,
        "X_test": X_test,
        "y_test": y_test,
        "cv_splits_indices": cv_splits_indices,
    }


def _get_column_data_type_as_str(array):
    """
    Get the type of ndarray by looking into the ndarray contents.

    :param array: ndarray
    :raise ValueError if array is not ndarray or not valid
    :return: type of column as a string (integer, floating, string etc.)
    """
    # If the array is not valid, then throw exception
    if array is None:
        raise DataException("The input array is None")

    # If the array is not an instance of ndarray, then throw exception
    if not isinstance(array, np.ndarray):
        raise DataException("Not an instance of ndarray. Found: {actual_type}".format(actual_type=type(array)))

    # Ignore the Nans and then return the data type of the column
    return api.types.infer_dtype(array[~pd.isnull(array)])


def _check_dimensions(
        X, y, X_valid, y_valid, sample_weight, sample_weight_valid):
    """
    Check dimensions of data inputs.

    Arguments:
        X {numpy.ndarray} -- X.
        y {numpy.ndarray} -- y.
        X_valid {numpy.ndarray} -- X for validation.
        y_valid {numpy.ndarray} -- y for validation.
        sample_weight {numpy.ndarray} -- sample weight for training.
        sample_weight_valid {numpy.ndarray} -- sample weight for validation.

    """
    dimension_error_message = "Dimension mismatch for {0} data. " \
                              "Expecting {1} dimensional array, " \
                              "but received {2} dimensional data."
    feature_dimensions = 2
    label_dimensions = 1

    # if the data is not in these 4 type, we will bypass the test
    x_dim = None
    y_dim = None
    x_valid_dim = None
    y_valid_dim = None
    sample_weight_dim = None
    sample_weight_valid_dim = None
    x_shape = None
    y_shape = None
    x_valid_shape = None
    y_valid_shape = None
    sample_weight_shape = None
    sample_weight_valid_shape = None

    if X is not None and (isinstance(X, pd.DataFrame) or isinstance(X, np.ndarray) or scipy.sparse.issparse(X)):
        x_shape = X.shape
        x_dim = X.ndim

    if X_valid is not None and \
            (isinstance(X_valid, pd.DataFrame) or isinstance(X_valid, np.ndarray) or scipy.sparse.issparse(X_valid)):
        x_valid_shape = X_valid.shape
        x_valid_dim = X_valid.ndim

    if isinstance(y, pd.DataFrame) or scipy.sparse.issparse(y):
        y_shape = y.shape
        y_dim = y.shape[1]
    elif isinstance(y, np.ndarray):
        y_shape = y.shape
        y_dim = y.ndim

    if isinstance(y_valid, pd.DataFrame) or scipy.sparse.issparse(y_valid):
        y_valid_shape = y_valid.shape
        y_valid_dim = y_valid.shape[1]
    elif isinstance(y_valid, np.ndarray):
        y_valid_shape = y_valid.shape
        y_valid_dim = y_valid.ndim

    if isinstance(sample_weight, pd.DataFrame) or scipy.sparse.issparse(sample_weight):
        sample_weight_shape = sample_weight.shape
        sample_weight_dim = sample_weight.shape[1]
    elif isinstance(sample_weight, np.ndarray):
        sample_weight_shape = sample_weight.shape
        sample_weight_dim = sample_weight.ndim

    if isinstance(sample_weight_valid, pd.DataFrame) or scipy.sparse.issparse(sample_weight_valid):
        sample_weight_valid_shape = sample_weight_valid.shape
        sample_weight_valid_dim = sample_weight_valid.shape[1]
    elif isinstance(sample_weight_valid, np.ndarray):
        sample_weight_valid_shape = sample_weight_valid.shape
        sample_weight_valid_dim = sample_weight_valid.ndim

    if x_dim is not None and x_dim > feature_dimensions:
        raise DataException(
            dimension_error_message
            .format("X", feature_dimensions, x_dim))
    if y_dim is not None and y_dim != label_dimensions:
        raise DataException(
            dimension_error_message
            .format("y", label_dimensions, y_dim))
    if x_valid_dim is not None and x_valid_dim > feature_dimensions:
        raise DataException(
            dimension_error_message
            .format("X_valid", feature_dimensions, x_valid_dim))
    if y_valid_dim is not None and y_valid_dim != label_dimensions:
        raise DataException(
            dimension_error_message
            .format("y_valid", label_dimensions, y_valid_dim))
    if sample_weight_dim is not None and sample_weight_dim != label_dimensions:
        raise DataException(
            dimension_error_message
            .format("sample_weight", label_dimensions, sample_weight_dim))
    if sample_weight_valid_dim is not None and sample_weight_valid_dim != label_dimensions:
        raise DataException(
            dimension_error_message.format(
                "sample_weight_valid", label_dimensions, sample_weight_valid_dim))

    if x_shape is not None and y_shape is not None and x_shape[0] != y_shape[0]:
        raise DataException(
            "X and y data do not have the same number of samples. "
            "X has {0} samples and y has {1} samples."
            .format(x_shape[0], y_shape[0]))
    if x_valid_shape is not None and y_valid_shape is not None and \
            x_valid_shape[0] != y_valid_shape[0]:
        raise DataException(
            "X_valid and y_valid data do not have the same number "
            "of samples. X_valid has {0} samples and "
            "y_valid has {1} samples."
            .format(x_valid_shape[0], y_valid_shape[0]))
    if sample_weight_shape is not None and y_shape is not None and \
            sample_weight_shape[0] != y_shape[0]:
        raise DataException(
            "sample_weight and y data do not have the same number "
            "of samples. sample_weight has {0} samples and "
            "y has {1} samples."
            .format(sample_weight_shape[0], y_shape[0]))
    if sample_weight_valid_shape is not None and y_valid_shape is not None and\
            sample_weight_valid_shape[0] != y_valid_shape[0]:
        raise DataException(
            "sample_weight_valid and y_valid data do not have the same number "
            "of samples. sample_weight_valid has {0} samples and y_valid "
            "has {1} samples.".format(sample_weight_valid_shape[0], y_valid_shape[0]))
    if x_shape is not None and y_shape is not None and x_shape[0] == 0:
        raise DataException("X and y data do not have any samples.")
    if x_valid_shape is not None and y_valid_shape is not None and x_valid_shape[0] == 0:
        raise DataException("X_valid and y_valid data do not have any samples.")


def sparse_std(x):
    """
    Compute the std for a sparse matrix.

    Std is computed by dividing by N and not N-1 to match numpy's computation.

    :param x: sparse matrix
    :return: std dev
    """
    if not scipy.sparse.issparse(x):
        raise ValueError("x is not a sparse matrix")

    mean_val = x.mean()
    num_els = x.shape[0] * x.shape[1]
    nzeros = x.nonzero()
    sum = mean_val**2 * (num_els - nzeros[0].shape[0])
    for i, j in zip(*nzeros):
        sum += (x[i, j] - mean_val)**2

    return sqrt(sum / num_els)


def sparse_isnan(x):
    """
    Return whether any element in matrix is nan.

    :param x: sparse matrix
    :return: True/False
    """
    if not scipy.sparse.issparse(x):
        raise ValueError("x is not sparse matrix")

    for i, j in zip(*x.nonzero()):
        if np.isnan(x[i, j]):
            return True

    return False


def stratified_shuffle(indices, y, random_state):
    """
    Shuffle an index in a way such that the first 1%, 2%, 4% etc. are all stratified samples.

    The way we achieve this is, first get 1:99 split
    then for the 99 part, we do a split of 1:98
    and then in the 98 part, we do a split of 2:96
    and then in the 96 part, we split 4:92
    then 8:86
    then 16:70
    then 32:38

    Arguments:
        indices {numpy.ndarray} -- indices to shuffle.
        y {numpy.ndarray} -- field to stratify by.
        random_state {RandomState, int, NoneType} -- random_state for random operations.

    Returns:
        numpy.ndarray -- shuffled indices.

    """
    if y is None:
        # no stratification required
        indices_copy = np.array(indices)
        old_state = np.random.get_state()
        np.random.seed(random_state or 0)
        np.random.shuffle(indices_copy)
        np.random.set_state(old_state)
        return indices_copy

    splits = [
        [1, 99],
        [1, 98],
        [2, 96],
        [4, 92],
        [8, 86],
        [16, 70],
        [32, 38]]

    ret = np.array([])
    y_left = y

    for split in splits:
        kept_frac = float(split[0]) / (split[0] + split[1])
        kept, left = model_selection.train_test_split(
            indices,
            train_size=kept_frac,
            stratify=y_left,
            random_state=random_state)
        ret = np.concatenate([ret, kept])
        indices = left
        y_left = y[left]

    ret = np.concatenate([ret, left]).astype('int')
    return ret


def check_input(df: pd.DataFrame) -> None:
    """
    Check inputs for transformations.

    :param df: Input dataframe.
    :return:
    """
    # Raise an exception if the input is not a data frame or array
    if not isinstance(df, pd.DataFrame) and not isinstance(df, np.ndarray):
        raise ValueError("df should be a pandas dataframe or numpy array")


# Regular expressions for date time detection
date_regex1 = re.compile(r'(\d+/\d+/\d+)')
date_regex2 = re.compile(r'(\d+-\d+-\d+)')


def is_known_date_time_format(datetime_str: str) -> bool:
    """
    Check if a given string matches the known date time regular expressions.

    :param datetime_str: Input string to check if it's a date or not
    :return: Whether the given string is in a known date time format or not
    """
    if date_regex1.search(datetime_str) is None and date_regex2.search(datetime_str) is None:
        return False

    return True
