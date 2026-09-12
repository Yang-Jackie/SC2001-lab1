import argparse
import math
import time
import data_generator
import sorting_interface
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

def plot_comparisons_and_durations(
    x_values,
    comparisons,
    durations,
    *,
    axes=None,
    title=None,
    x_label="Input size",
    comparison_label="Comparisons",
    duration_label="Duration",
    comparison_style=None,
    duration_style=None,
):
    x_values = list(x_values)
    comparisons = list(comparisons)
    durations = list(durations)

    if not (
        len(x_values)
        == len(comparisons)
        == len(durations)
    ):
        raise ValueError(
            "x_values, comparisons, and durations "
            "must have equal lengths"
        )

    if axes is None:
        fig, ax_comparisons = plt.subplots(figsize=(10, 6))
        ax_duration = ax_comparisons.twinx()
    else:
        ax_comparisons, ax_duration = axes
        fig = ax_comparisons.figure

    comp_style = {
        "color": "tab:blue",
        "marker": "o",
    }
    time_style = {
        "color": "tab:red",
        "marker": "x",
    }

    if comparison_style:
        comp_style.update(comparison_style)

    if duration_style:
        time_style.update(duration_style)

    comparison_line, = ax_comparisons.plot(
        x_values,
        comparisons,
        label=comparison_label,
        **comp_style,
    )

    duration_line, = ax_duration.plot(
        x_values,
        durations,
        label=duration_label,
        **time_style,
    )

    ax_comparisons.set_xlabel(x_label)
    ax_comparisons.set_ylabel("Number of comparisons")
    ax_duration.set_ylabel("Duration (seconds)")
    ax_comparisons.grid(alpha=0.3)

    if title:
        ax_comparisons.set_title(title)

    return (
        fig,
        (ax_comparisons, ax_duration),
        (comparison_line, duration_line),
    )

def sanity_check():
    arr = [5, 2, 9, 1, 5, 6]
    print(f"Original array: {arr}")
    arr, comparisons, _ = sorting_interface.hybrid_sort(arr, 16)
    print(f"Sorted array: {arr}\nComparisons made: {comparisons}")

    arr = data_generator.generate(20, 100)
    print(f"Original array: {arr}")
    arr, comparisons, _ = sorting_interface.hybrid_sort(arr, 16)
    print(f"Sorted array: {arr}\nComparisons made: {comparisons}")

def benchmark(dataset, S):
    input_sizes = []
    comparisons = []
    durations = []

    start = time.perf_counter()

    for i, arr in enumerate(dataset):
        input_sizes.append(len(arr))

        if (i + 1) % 10 == 0:
            print(f"Processing the {i+1}-th array")

        _, comp, duration = sorting_interface.hybrid_sort(arr, S)
        comparisons.append(comp)
        durations.append(duration)

    end = time.perf_counter()
    print(f"Time taken to process {len(input_sizes)} arrays: {end - start:.2f} seconds")

    return input_sizes, comparisons, durations

def plot_over_input_size(dataset, S):
    input_sizes, comparisons, durations = benchmark(dataset, S)

    fig, (ax_comparisons, ax_duration), lines = plot_comparisons_and_durations(
        input_sizes,
        comparisons,
        durations,
        title=f"Hybrid Merge Sort vs Input Size (S={S})",
        x_label="Input size"
    )

    ax_comparisons.xaxis.set_major_formatter(
        StrMethodFormatter("{x:,.0f}")
    )
    ax_comparisons.yaxis.set_major_formatter(
        StrMethodFormatter("{x:,.0f}")
    )

    ax_comparisons.legend(
        lines,
        [line.get_label() for line in lines],
    )

    fig.tight_layout()
    plt.show()

def plot_over_s(n_samples: int, sizes: list, thresholds: list):
    n_cols = 2
    n_rows = math.ceil(len(sizes) / n_cols)

    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(12, 5 * n_rows)
    )

    axes = axes.flatten()

    time_start = time.perf_counter()

    for ax, size in zip(axes, sizes):
        dataset = list(data_generator.dataset(n_samples, size))

        average_comparisons = []
        average_durations = []
        sample_durations = [[] for _ in range(n_samples)]

        for s in thresholds:
            total_comparisons = 0
            total_duration = 0

            print(f"Processing size={size}, threshold={s}...")

            for sample_index, arr in enumerate(dataset):
                _, comp, duration = sorting_interface.hybrid_sort(
                    arr, s
                )

                total_comparisons += comp
                total_duration += duration
                sample_durations[sample_index].append(duration)

            average_comparisons.append(
                total_comparisons / n_samples
            )
            average_durations.append(
                total_duration / n_samples
            )

        # Left y-axis: comparisons
        line1 = ax.plot(
            thresholds,
            average_comparisons,
            marker='o',
            label='Comparisons'
        )

        ax.set_title(f'n = {size:,}')
        ax.set_xlabel('Threshold S')
        ax.set_ylabel('Key Comparisons')
        ax.grid()

        # Right y-axis: duration
        ax_time = ax.twinx()

        sample_lines = []
        for sample_index, durations in enumerate(sample_durations):
            line = ax_time.plot(
                thresholds,
                durations,
                color='tab:orange',
                alpha=0.2,
                linewidth=0.8,
                label='Sample durations' if sample_index == 0 else None
            )
            if sample_index == 0:
                sample_lines = line

        line2 = ax_time.plot(
            thresholds,
            average_durations,
            color='tab:red',
            marker='x',
            linestyle='--',
            linewidth=2,
            label='Average duration'
        )

        ax_time.set_ylabel('Duration (s)')

        # Combined legend
        lines = line1 + sample_lines + line2
        ax.legend(
            lines,
            [line.get_label() for line in lines]
        )

    print(
        f"Time taken: "
        f"{time.perf_counter() - time_start:.2f} seconds"
    )

    for ax in axes[len(sizes):]:
        ax.remove()

    plt.tight_layout()
    plt.savefig("outputs/plot_over_s.png", dpi=300)
    plt.show()

def compare_hybrid_merge(dataset, S):
    dataset = list(dataset)

    input_sizes, hybrid_comparisons, hybrid_durations = benchmark(dataset, S)
    _, merge_comparisons, merge_durations = benchmark(dataset, 1)

    # Asymptotic reference, not an exact upper bound.
    n_log_n = [
        n * math.log2(n) if n > 1 else 0
        for n in input_sizes
    ]

    fig, ax_comparisons = plt.subplots(figsize=(11, 7))
    ax_duration = ax_comparisons.twinx()

    # Left axis: comparison counts
    hybrid_comp_line, = ax_comparisons.plot(
        input_sizes,
        hybrid_comparisons,
        color="tab:blue",
        marker="o",
        markersize=4,
        label=f"Hybrid comparisons (S={S})",
    )

    merge_comp_line, = ax_comparisons.plot(
        input_sizes,
        merge_comparisons,
        color="tab:cyan",
        marker="s",
        markersize=4,
        linestyle="--",
        label="Merge-sort comparisons",
    )

    theoretical_line, = ax_comparisons.plot(
        input_sizes,
        n_log_n,
        color="black",
        linestyle=":",
        linewidth=2,
        label=r"$n\log_2(n)$ reference",
    )

    # Right axis: measured durations
    hybrid_time_line, = ax_duration.plot(
        input_sizes,
        hybrid_durations,
        color="tab:red",
        marker="x",
        markersize=4,
        label=f"Hybrid runtime (S={S})",
    )

    merge_time_line, = ax_duration.plot(
        input_sizes,
        merge_durations,
        color="tab:orange",
        marker="^",
        markersize=4,
        linestyle="--",
        label="Merge-sort runtime",
    )

    ax_comparisons.set_title(
        f"Hybrid Sort vs Merge Sort (S={S})"
    )
    ax_comparisons.set_xlabel("Input size, n")
    ax_comparisons.set_ylabel("Number of key comparisons")
    ax_duration.set_ylabel("Runtime (seconds)")

    ax_comparisons.xaxis.set_major_formatter(
        StrMethodFormatter("{x:,.0f}")
    )
    ax_comparisons.yaxis.set_major_formatter(
        StrMethodFormatter("{x:,.0f}")
    )

    ax_comparisons.grid(alpha=0.3)

    lines = [
        hybrid_comp_line,
        merge_comp_line,
        theoretical_line,
        hybrid_time_line,
        merge_time_line,
    ]

    ax_comparisons.legend(
        lines,
        [line.get_label() for line in lines],
        loc="upper left",
    )

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-cpp",
        "--cpp",
        action="store_true",
        help="Use the C++ sorting implementation",
    )
    args = parser.parse_args()

    sorting_interface.select_backend(use_cpp=args.cpp)
    sanity_check()
    dataset = data_generator.dataset(100)
    S = 32
    plot_over_input_size(dataset, S)
    # plot_over_s(30, [1000, 100_000, 10_000_000], [4, 8, 16, 24, 32, 48, 64, 128])
    # compare_hybrid_merge(dataset, S)
