import math
import time
import data_generator
import sorting_interface
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

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

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Comparisons
    line1 = ax1.plot(
        input_sizes,
        comparisons,
        marker='o',
        markersize=4,
        label='Comparisons',
        color='tab:blue'
    )

    ax1.set_xlabel('Input Size')
    ax1.set_ylabel('Number of Comparisons', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Duration
    ax2 = ax1.twinx()

    line2 = ax2.plot(
        input_sizes,
        durations,
        marker='x',
        markersize=4,
        label='Duration',
        color='tab:red'
    )

    ax2.set_ylabel('Duration (s)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Formatting
    ax1.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    ax1.grid(axis='both', alpha=0.3)

    ax1.set_title(
        f'Hybrid Merge Sort vs Input Size (S={S})'
    )

    # Combined legend
    lines = line1 + line2
    ax1.legend(lines, [line.get_label() for line in lines])

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
    pass

if __name__ == "__main__":
    sanity_check()
    dataset = data_generator.dataset(100)
    S = 32
    # plot_over_input_size(dataset, S)
    plot_over_s(30, [1000, 100_000, 10_000_000], [4, 8, 16, 24, 32, 48, 64])
