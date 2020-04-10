import pandas as pd
import pandas_f
import unittest


class FSeriesAccessorTestCase(unittest.TestCase):
    def test_map(self):
        # Given
        def fn(df: pd.DataFrame) -> pd.DataFrame:
            c = df['a'] + 1
            d = df['a'] + 2
            df2 = pd.DataFrame({'c': c, 'd': d})
            return pd.concat([df2] * 2)

        s = pd.Series([
            {'a': 1},
            {'a': 2},
            {'a': 3},
        ])

        # When
        actual_df = s.f.map(fn)

        # Then
        expected_df = pd.DataFrame(
            [{'c': 2, 'd': 3}, {'c': 2, 'd': 3}, {'c': 3, 'd': 4},
             {'c': 3, 'd': 4}, {'c': 4, 'd': 5}, {'c': 4, 'd': 5}, ])

        pd.testing.assert_frame_equal(
            expected_df,
            actual_df
        )


class FDataFrameAccessorTestCase(unittest.TestCase):
    def test_map(self):
        # Given
        def fn(df: pd.DataFrame) -> pd.DataFrame:
            self.assertEquals(1, len(df))
            c = df['a'] + 1
            d = df['a'] + df['b']
            df2 = pd.DataFrame({'c': c, 'd': d})
            return pd.concat([df2])

        input_df = pd.DataFrame([
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3},
            {'a': 3, 'b': 4},
        ])

        # When
        actual_df = input_df.f.map(fn)

        # Then
        expected_df = pd.DataFrame([
            {'c': 2, 'd': 3},
            {'c': 3, 'd': 5},
            {'c': 4, 'd': 7},
        ])

        pd.testing.assert_frame_equal(
            expected_df,
            actual_df
        )
