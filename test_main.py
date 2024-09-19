from main import main
from pathlib import Path

test_fig_file_path = Path("Figure/test_figure.png")

if test_fig_file_path.exists():
    test_fig_file_path.unlink()


def test_main_plot():
    main("Metro_Interstate_Traffic_Volume.csv.gz", fig_name="test_figure")
    path = Path("Figure/test_figure.png")
    assert path.exists()


if __name__ == "__main__":
    test_main_plot()
