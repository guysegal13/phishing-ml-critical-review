"""Loading helpers for the UCI Phishing Websites dataset."""
import pandas as pd


def load_phishing_arff(path):
    """Parse the UCI .arff file into a plain int DataFrame.

    The file format is simple enough (one @attribute line per column, then
    a flat @data block) that pulling in a whole arff library felt like
    overkill for 31 columns.
    """
    columns, rows, in_data_block = [], [], False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("%"):
                continue
            if line.lower().startswith("@attribute"):
                columns.append(line.split()[1])
            elif line.lower().startswith("@data"):
                in_data_block = True
            elif in_data_block:
                rows.append(line.split(","))
    return pd.DataFrame(rows, columns=columns).astype(int)
