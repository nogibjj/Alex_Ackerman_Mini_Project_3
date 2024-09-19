"""
Library
"""

import polars as pl

# import pandas as pd
import matplotlib.pyplot as plt


def read_csv_file(file_name):
    return pl.read_csv(file_name)


def stats_overview(df, col):
    stat_table = df.select([col]).describe()  # Median is labeled as 50%
    median = df.select([col]).median()
    median_df = pl.DataFrame({"statistic": ["median"], col: [median.item()]})
    stat_table = pl.concat([stat_table, median_df])  # Add median to stat_table
    return stat_table


def split_day_night(df):
    # Transform 'date_time to datetime'
    df_datetime = df.with_columns(pl.col("date_time").str.to_datetime())

    # Separate data into day and night
    df_day = df_datetime.filter(
        (pl.col("date_time").dt.hour() >= 7) & (pl.col("date_time").dt.hour() < 19)
    )
    df_night = df_datetime.filter(
        (pl.col("date_time").dt.hour() >= 19) | (pl.col("date_time").dt.hour() < 7)
    )

    return df_day, df_night


def hist_day_night(df_day, df_night):
    plt.figure(figsize=(11, 4))

    plt.subplot(1, 2, 1)
    plt.hist(df_day["traffic_volume"])
    plt.xlim(-100, 7500)
    plt.ylim(0, 8000)
    plt.title("Traffic Volume: Day")
    plt.xlabel("Traffic Volume")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.hist(df_night["traffic_volume"])
    plt.xlim(-100, 7500)
    plt.ylim(0, 8000)
    plt.title("Traffic Volume: Night")
    plt.xlabel("Traffic Volume")
    plt.ylabel("Frequency")

    # return fig


if __name__ == "__main__":
    csv_file = "Metro_Interstate_Traffic_Volume.csv.gz"
    df = read_csv_file(csv_file)

    # Get statistics about traffic volume
    traffic_volume_summary = stats_overview(df, "traffic_volume")
    print("Traffic Volume Summary\n", traffic_volume_summary, "\n")

    # Traffic stats: Day vs Night
    day_df, night_df = split_day_night(df)
    day_traffic_volume = stats_overview(day_df, "traffic_volume")
    print("Day Traffic Volume Stats\n", day_traffic_volume, "\n")

    night_traffic_volume = stats_overview(night_df, "traffic_volume")
    print("Night Traffic Volume Stats\n", night_traffic_volume, "\n")

    # Histogram of Traffic Volume: Day vs Night
    fig_name = "lib_test_fig"
    hist_day_night(day_df, night_df)
    plt.savefig(f"Figure/{fig_name}.png")
