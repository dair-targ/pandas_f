"""
>>> import pandas, pandas_f
>>> def fn(df: pd.DataFrame) -> pd.DataFrame:
...     c = df['a'] + 1
...     d = df['a'] + df['b']
...     return pd.DataFrame({'c': c, 'd': d})
>>> input_df = pd.DataFrame([
...     {'a': 1, 'b': 2},
...     {'a': 2, 'b': 3},
...     {'a': 3, 'b': 4},
... ])
>>> input_df.f.map(fn)
   c  d
0  2  3
1  3  5
2  4  7


Resulting dataframes are concatenated:
>>> def fn2(df: pd.DataFrame) -> pd.DataFrame:
...     c = df['a'] + df['b']
...     r_df = pd.DataFrame({'c': c})
...     return pd.concat([r_df, r_df + 1])
>>> input_df.f.map(fn2)
   c
0  3
0  4
1  5
1  6
2  7
2  8
"""
import pandas as pd
import typing


PandasCategory = typing.NewType(
    'PandasCategory',
    typing.Union[pd.Series, pd.DataFrame],
)

PandasEndofunctor = typing.NewType(
    'PandasEndofunctor',
    typing.Callable[[PandasCategory], PandasCategory],
)


@pd.api.extensions.register_series_accessor('f')
class FSeriesAccessor:
    def __init__(self, series: pd.Series):
        self._series: pd.Series = series

    def __iter__(self):
        for row in self._series:
            yield pd.DataFrame([row])

    def map(self, func: PandasEndofunctor) -> pd.DataFrame:
        """
        :param func: A function to be applied to every value from
        the series, converted into pandas.DataFrame.
        :return: A concatenated pandas.DataFrame
        """
        return pd.concat(map(func, self)).reset_index(drop=True)


@pd.api.extensions.register_dataframe_accessor('f')
class FDataFrameAccessor:
    def __init__(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe

    def __iter__(self):
        for index, row in self._dataframe.iterrows():
            yield pd.DataFrame([row])

    def map(self, func: PandasEndofunctor) -> pd.DataFrame:
        """
        :param func: A function to be applied to every row from
        the dataframe, converted into pandas.DataFrame.
        :return: A concatenated pandas.DataFrame
        """
        return pd.concat(map(func, self))


__all__ = [
    'PandasCategory',
    'PandasEndofunctor',
    'FSeriesAccessor',
    'FDataFrameAccessor',
]
