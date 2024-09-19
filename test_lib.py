"""
Test Lib
"""

from mylib.lib import read_csv_file, stats_overview, split_day_night, hist_day_night

import polars as pl

# import pandas as pd
import matplotlib.pyplot as plt

import unittest

# string IO helps create a csv file for testing
from io import StringIO


class test_functions(unittest.TestCase):
    def test_read_csv_file(self):
        csv_data = """col1,col2,col3
                        1,-1,0
                        10,0, """
        csv_file = StringIO(csv_data)

        test_df = read_csv_file(csv_file)

        # Check the dataframe has correct data
        self.assertEqual(test_df.shape, (2, 3))

    def test_stats_overview(self):
        csv_data = """A,B,C
                            1,2,3
                            4,5,6
                            7,8,9"""
        test_df = pl.read_csv(StringIO(csv_data))
        stat_summary = stats_overview(test_df, "C")

        mean_value = (
            stat_summary.filter(pl.col("statistic") == "mean").select("C").to_numpy()[0]
        )
        count_value = (
            stat_summary.filter(pl.col("statistic") == "count")
            .select("C")
            .to_numpy()[0]
        )
        median_value = (
            stat_summary.filter(pl.col("statistic") == "median")
            .select("C")
            .to_numpy()[0]
        )

        # Check if the description contains expected values
        self.assertEqual(mean_value, 6)
        self.assertEqual(count_value, 3)
        self.assertEqual(median_value, 6)

    def test_split_day_night(self):
        csv_data = """traffic_volume,date_time
                  5000,2012-10-02 07:00:00
                  1,2012-10-02 19:00:00
                  7000,2012-10-02 23:00:00
                  200,2012-10-02 14:00:00
                  10000,2012-10-02 00:00:00"""
        test_df = pl.read_csv(StringIO(csv_data))
        test_day, test_night = split_day_night(test_df)
        self.assertEqual(test_day.shape, (2, 2))
        self.assertEqual(test_night.shape, (3, 2))

    def test_hist_day_night(self):
        day_csv_data = """traffic_volume,date_time
                  5000,2012-10-02 07:00:00
                  5000,2012-10-02 08:00:00
                  7000,2012-10-02 12:00:00
                  1000,2012-10-02 13:00:00
                  6000,2012-10-02 15:00:00"""
        day_df = pl.read_csv(StringIO(day_csv_data))

        night_csv_data = """traffic_volume,date_time
                  500,2012-10-02 21:00:00
                  1000,2012-10-02 22:00:00
                  3000,2012-10-02 23:00:00
                  1000,2012-10-02 01:00:00
                  2000,2012-10-02 03:00:00"""
        night_df = pl.read_csv(StringIO(night_csv_data))

        try:
            # Test plot, but not displaying it
            plt.figure()
            hist_day_night(day_df, night_df)
            plot_success = True
        except Exception as e:
            plot_success = False
            print(f"Plot failed: {e}")

        self.assertTrue(plot_success)


if __name__ == "__main__":
    unittest.main()
    # test_read_csv_file()
    # test_stats_overview()
    # test_split_day_night()
    # test_hist_day_night()
