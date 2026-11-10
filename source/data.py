import os
import numpy as np
from time import localtime, strftime
import pathlib


# Project root
root_folder = pathlib.Path(__file__).parent.parent

data = np.reshape(np.arange(100)**2, (10, 10))
#
# metadata = {
#     "time": strftime("%H:%M:%S", localtime()),
#     "ppsm": [1, 2, 16]
# }
#
# np.savez(root_folder / "Resource" / "arr1.npz", data=data, meta=metadata)

loaded_npz = np.load(root_folder / "Resource" / "arr1.npz")
print(f"{loaded_npz.files=}")
print(f"{loaded_npz.allow_pickle=}")

loaded_npz.allow_pickle=True

data = loaded_npz.get("data")
meta = loaded_npz.get("meta")

print(meta)