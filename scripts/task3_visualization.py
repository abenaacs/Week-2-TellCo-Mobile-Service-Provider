import os


def save_plot(plot, filename):
    directory = "visualizations"
    if not os.path.exists(directory):
        os.makedirs(directory)
    plot.savefig(f"{directory}/{filename}", bbox_inches="tight")
    print(f"Saved {filename} to {directory}")
