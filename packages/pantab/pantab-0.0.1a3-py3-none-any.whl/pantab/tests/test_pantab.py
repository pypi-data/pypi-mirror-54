import os
import pathlib
import re
import tempfile

import numpy as np
import pandas as pd
import pandas.util.testing as tm
import pytest
from tableauhyperapi import Name, TableName, TypeTag

import pantab


@pytest.fixture
def df():
    """Fixture to use which should contain all data types."""
    df = pd.DataFrame(
        [
            [1, 2, 3, 4.0, 5.0, True, pd.to_datetime("1/1/18"), "foo"],
            [6, 7, 8, 9.0, 10.0, True, pd.to_datetime("1/1/19"), "foo"],
        ],
        columns=[
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
            "bool",
            "datetime64",
            "object",
        ],
    )

    df = df.astype(
        {
            "int16": np.int16,
            "int32": np.int32,
            "int64": np.int64,
            "float32": np.float32,
            "float64": np.float64,
            "bool": np.bool,
            "datetime64": "datetime64[ns]",
            # 'grault': 'timedelta64[ns]',
            "object": "object",
        }
    )

    return df


@pytest.fixture
def tmp_hyper(tmp_path):
    """A temporary file name to write / read a Hyper extract from."""
    return tmp_path / "test.hyper"


@pytest.fixture(
    params=[
        "table",
        Name("table"),
        TableName("table"),
        TableName("public", "table"),
        TableName("nonpublic", "table"),
    ]
)
def table_name(request):
    """Various ways to represent a table in Tableau."""
    return request.param


def test_roundtrip(df, tmp_hyper, table_name):
    pantab.frame_to_hyper(df, tmp_hyper, table=table_name)
    result = pantab.frame_from_hyper(tmp_hyper, table=table_name)
    expected = df.copy()
    expected["float32"] = expected["float32"].astype(np.float64)

    tm.assert_frame_equal(result, expected)


def test_roundtrip_missing_data(tmp_hyper, table_name):
    df = pd.DataFrame([[np.nan], [1]], columns=list("a"))
    df["b"] = pd.Series([None, np.nan], dtype=object)  # no inference
    df["c"] = pd.Series([np.nan, "c"])

    pantab.frame_to_hyper(df, tmp_hyper, table=table_name)

    result = pantab.frame_from_hyper(tmp_hyper, table=table_name)
    expected = pd.DataFrame(
        [[np.nan, np.nan, np.nan], [1, np.nan, "c"]], columns=list("abc")
    )
    tm.assert_frame_equal(result, expected)


def test_roundtrip_multiple_tables(df, tmp_hyper, table_name):
    pantab.frames_to_hyper({table_name: df, "table2": df}, tmp_hyper)

    result = pantab.frames_from_hyper(tmp_hyper)
    expected = df.copy()
    expected["float32"] = expected["float32"].astype(np.float64)

    # some test trickery here
    if not isinstance(table_name, TableName) or table_name.schema_name is None:
        table_name = TableName("public", table_name)

    assert set(result.keys()) == set((table_name, TableName("public", "table2")))
    for val in result.values():
        tm.assert_frame_equal(val, expected)
