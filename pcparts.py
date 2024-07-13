import pandas as pd

# Load the CSV files (replace with your actual file paths)
gpu_data = pd.read_csv('gpu_benchmarks.csv')
cpu_data = pd.read_csv('cpu_benchmarks.csv')

# Remove the '$' sign and convert the 'Price' column to numeric
gpu_data['Price'] = gpu_data['Price'].replace('[\$,]', '', regex=True).astype(float)
cpu_data['Price'] = cpu_data['Price'].replace('[\$,]', '', regex=True).astype(float)

# Define the budget

budget = float(input("Enter Budget: "))

# Initial bottleneck range
bottleneck_min = 0.9
bottleneck_max = 1.1

# Flag to check if a valid pair is found
found_valid_pair = False

while not found_valid_pair:
    # Filter GPUs and CPUs within the budget
    affordable_gpus = gpu_data[gpu_data['Price'] <= budget]
    affordable_cpus = cpu_data[cpu_data['Price'] <= budget]

    # Generate all possible pairs of GPUs and CPUs
    pairs = [(gpu, cpu) for gpu in affordable_gpus.itertuples() for cpu in affordable_cpus.itertuples()]

    # Calculate the total price and combined benchmark score for each pair
    pairs_within_budget = []
    for gpu, cpu in pairs:
        total_price = gpu.Price + cpu.Price
        combined_score = gpu.Benchmark + cpu.Benchmark
        gpu_normalized = gpu.Normalized
        cpu_normalized = cpu.Normalized
        bottleneckratio = gpu_normalized / cpu_normalized

        # Check if the pair is within budget and has a good balance (bottleneck)
        if total_price <= budget and bottleneck_min <= bottleneckratio <= bottleneck_max:
            pairs_within_budget.append((gpu.Model, cpu.Model, total_price, combined_score, gpu_normalized, cpu_normalized))

    # Sort pairs by combined benchmark score in descending order
    sorted_pairs = sorted(pairs_within_budget, key=lambda x: x[3], reverse=True)

    # Get the top pair if any valid pairs are found
    if sorted_pairs:
        top_pair = sorted_pairs[0]
        found_valid_pair = True
    else:
        # Increase the bottleneck range if no valid pairs are found
        bottleneck_min -= 0.1
        bottleneck_max += 0.1
        print(f"No matches found within {bottleneck_min:.1f}-{bottleneck_max:.1f} bottleneck range. Increasing range...")

# Display the top pair
print("Top GPU and CPU pair within the budget and bottleneck range:")
print(f"GPU: {top_pair[0]}, CPU: {top_pair[1]}, Total Price: ${top_pair[2]:.2f}, Bottleneck Ratio: {top_pair[4] / top_pair[5]:.2f}")
# , Combined Benchmark: {top_pair[3]}, GPU Normalized: {top_pair[4]:.2f}, CPU Normalized: {top_pair[5]:.2f}