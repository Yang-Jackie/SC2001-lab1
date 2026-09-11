import numpy as np
import time

def insertion_sort(arr: list) -> tuple[list, int]:
    comparisons = 0
    for i in range(1, len(arr)):
        j = i
        while j > 0:
            comparisons += 1
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break
            j -= 1
    return arr, comparisons

def _merge(arr: list, l: int, mid: int, r: int) -> tuple[list, int]:
    merged_arr = []
    i = l
    j = mid

    comparisons = 0
    while i < mid and j < r:
        comparisons += 1
        if arr[i] < arr[j]:
            merged_arr.append(arr[i])
            i += 1
        else:
            merged_arr.append(arr[j])
            j += 1

    merged_arr.extend(arr[i:mid])
    merged_arr.extend(arr[j:r])

    return merged_arr, comparisons

def _hybrid_sort(arr: list, l: int, r: int, s: int) -> tuple[list, int]:
    if r-l <= s:
        return insertion_sort(arr[l:r])

    mid = (r+l) // 2
    left_arr, left_comparisons = _hybrid_sort(arr, l, mid, s)
    right_arr, right_comparisons = _hybrid_sort(arr, mid, r, s)

    merged_arr, merge_comparisons = _merge(arr, l, mid, r)
    return merged_arr, left_comparisons + right_comparisons + merge_comparisons

def hybrid_sort(arr: list | np.ndarray, s: int) -> tuple[list, int, float]:
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    time_start = time.perf_counter()
    return *_hybrid_sort(arr, 0, len(arr), s), time.perf_counter() - time_start

def merge_sort(arr: list | np.ndarray) -> tuple[list, int, float]:
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    time_start = time.perf_counter()
    return *_hybrid_sort(arr, 0, len(arr), 1), time.perf_counter() - time_start