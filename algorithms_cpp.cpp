/*
<%
setup_pybind11(cfg)
%>
*/

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>
#include <utility>
#include <cstdint>

namespace py = pybind11;

using SortResult = std::pair<std::vector<int>, int>;
using RunResult = std::tuple<std::vector<int>, int, double>;

SortResult _insertion_sort(std::vector<int> arr) {
    int comparisons = 0;

    for (int i = 0; i < arr.size(); ++i) {
        int j = i;
        while (j > 0 && arr[j] < arr[j - 1]) {
            std::swap(arr[j], arr[j - 1]);
            --j;
            ++comparisons; // Count the comparison that succeeded
        }
        if (j > 0) {
            ++comparisons; // Count the comparison that failed the while condition
        }
    }

    return {std::move(arr), comparisons};
}

SortResult _merge(const std::vector<int>& left, const std::vector<int>& right) {
    std::vector<int> merged;
    merged.reserve(left.size() + right.size());
    int comparisons = 0;

    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] < right[j]) {
            merged.push_back(left[i++]);
        } else {
            merged.push_back(right[j++]);
        }
        ++comparisons; // Count the comparison made during merging
    }

    // Append remaining elements
    while (i < left.size()) {
        merged.push_back(left[i++]);
    }
    while (j < right.size()) {
        merged.push_back(right[j++]);
    }

    return {std::move(merged), comparisons};
}

SortResult _hybrid_sort(const std::vector<int>& arr, int l, int r, int s) {
    if (r - l <= s) {
        return _insertion_sort(std::vector<int>(arr.begin() + l, arr.begin() + r));
    }

    int mid = (r+l) >> 1;
    SortResult left = _hybrid_sort(arr, l, mid, s);
    SortResult right = _hybrid_sort(arr, mid, r, s);

    SortResult merged_results = _merge(left.first, right.first);

    merged_results.second += left.second + right.second;
    return merged_results;
}


RunResult hybrid_sort(const std::vector<int>& arr, int threshold) {
    auto start = std::chrono::steady_clock::now();

    auto res = _hybrid_sort(arr, 0, arr.size(), threshold);

    auto end = std::chrono::steady_clock::now();

    double seconds = std::chrono::duration<double>(end - start).count();
    
    return {std::move(res.first), res.second, seconds};
}

RunResult merge_sort(const std::vector<int>& arr) {
    auto start = std::chrono::steady_clock::now();

    SortResult res = _hybrid_sort(arr, 0, arr.size(), 1);

    auto end = std::chrono::steady_clock::now();

    double seconds = std::chrono::duration<double>(end - start).count();
    
    return {res.first, res.second, seconds};
}

PYBIND11_MODULE(algorithms_cpp, m) {
    m.def("hybrid_sort", &hybrid_sort, py::arg("arr"), py::arg("threshold"));
    m.def("merge_sort", &merge_sort, py::arg("arr"));
}
