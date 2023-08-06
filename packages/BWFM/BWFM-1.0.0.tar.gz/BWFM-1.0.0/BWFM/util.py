from pathlib import Path

conf_dir = Path.home().joinpath(".bwfm")
conf_path = conf_dir.joinpath("conf.json")

conf_dir.mkdir(exist_ok=True)
