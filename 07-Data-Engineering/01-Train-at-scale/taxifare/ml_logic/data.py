from taxifare.ml_logic.params import (COLUMN_NAMES_RAW,
                                            DTYPES_RAW_OPTIMIZED,
                                            DTYPES_RAW_OPTIMIZED_HEADLESS,
                                            DTYPES_PROCESSED_OPTIMIZED
                                            )

import os
import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # remove useless/redundant columns
    # $CODE_BEGIN
    df = df.drop(columns=['key'])
    # $CODE_END

    # remove buggy transactions
    # $CODE_BEGIN
    df = df.drop_duplicates()  # TODO: handle in the data source if the data is consumed by chunks
    df = df.dropna(how='any', axis=0)
    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0) |
            (df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
    df = df[df.passenger_count > 0]
    df = df[df.fare_amount > 0]
    # $CODE_END

    # remove irrelevant/non-representative transactions (rows) for a training set
    # $CODE_BEGIN
    df = df[df.fare_amount < 400]
    df = df[df.passenger_count < 8]
    df = df[df["pickup_latitude"].between(left=40.5, right=40.9)]
    df = df[df["dropoff_latitude"].between(left=40.5, right=40.9)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-73.7)]
    df = df[df["dropoff_longitude"].between(left=-74.3, right=-73.7)]
    # $CODE_END

    print("\n✅ data cleaned")

    return df
