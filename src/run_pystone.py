import pystone
import time

def main():
    for i in range(3):
        print(f"Running iteration {i + 1} of Pystone benchmark...")
        time.sleep(0.1)
        start_time = time.time()

        # Run the old Pystone benchmark
        x = pystone.main(loops=10)  # Adjust loops as needed

        print(x)

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"Iteration {i + 1} completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
