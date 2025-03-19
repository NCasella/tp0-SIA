import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.arange(10)  # X-axis values (e.g., time points, categories)
y = np.sin(x)      # Mean values
std_dev = 0.1 * np.abs(np.sin(x))  # Standard deviation values

# Create the plot
plt.figure(figsize=(8, 6))

# Plot the mean values
plt.plot(x, y, label='Mean Value', marker='o', linestyle='-', color='b')

# Add error bars representing the standard deviation
plt.fill_between(x, y - std_dev, y + std_dev, color='b', alpha=0.2, label='Standard Deviation')

# Add labels, title, and legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Mean and Standard Deviation')
plt.legend()

# Show the plot
plt.grid(True)
plt.savefig("graph.png")
plt.show()
