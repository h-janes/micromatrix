import os
import pathlib
from .main import Matrix

__title__ = "micromatrix"
__version__ = "1.0.1"
__author__ = "illicitbread"
__license__ = "MIT"
__url__ = "https://github.com/illicitbread/matrix"

__cache = os.path.join(pathlib.Path(__file__).parent.absolute(), ".cache")

if not os.path.isfile(__cache):
    cy, cb, cr = "\u001b[33m", "\u001b[1m", "\u001b[0m"
    print(f"{cb+cy+__title__} {__version__+cr+cb} by {cy+__author__+cr+cb} is imported succesfully!{cr}")
    print(f"Source code, help, and bug tracker at: {__url__}")
    print("Don't worry ~ This message will only appear once.")
    print()
    with open(__cache, "w") as wf:
        wf.write("1")
