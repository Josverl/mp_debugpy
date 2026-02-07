import sys
import time

import pystone


def main(runs=3, loops=20):
    all_stones = 0
    for i in range(runs):
        print(f"Running iteration {i + 1} of Pystone benchmark...")
        time.sleep(0.1)
        start_time = time.time()

        # Run the old Pystone benchmark
        stones = pystone.main(loops=loops)  # Adjust loops as needed
        all_stones += stones

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Iteration {i + 1} completed in {elapsed_time:.2f} seconds")

    print(f"Average Pystones: {all_stones / runs:.2f} stones/second over {runs} runs with {loops} loops each.")
    pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(runs=int(sys.argv[1]))
    elif len(sys.argv) == 3:
        main(runs=int(sys.argv[1]), loops=int(sys.argv[2]))
    else:
        main()
