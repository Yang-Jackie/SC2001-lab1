import time
import numpy as np

import cppimport.import_hook
algorithms_cpp = cppimport.imp("algorithms_cpp")

def hybrid_sort(arr: list | np.ndarray, s) -> tuple[list, int, float]:
    return algorithms_cpp.hybrid_sort(arr, s)

def merge_sort(arr: list | np.ndarray) -> tuple[list, int, float]:
    return algorithms_cpp.merge_sort(arr)
