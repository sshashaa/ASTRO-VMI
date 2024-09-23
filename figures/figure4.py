import numpy as np
import matplotlib.pyplot as plt

# Define the function
def f(x1, x2):
    return (x1**2 + x2-11)**2 + (x1+x2**2-7)**2 + (x1-x2)**2 + abs(x1-3)

# Define the range for x1 and x2
x1 = np.linspace(-7.5, 7.5, 500)
x2 = np.linspace(-7.5, 7.5, 500)

# Create a grid of (x1, x2) values
X1, X2 = np.meshgrid(x1, x2)

# Calculate the function values for each point in the grid
Z = f(X1, X2)

# Create a contour plot
contour = plt.contour(X1, X2, Z, levels=np.logspace(0, 3, 15), cmap='viridis')

# Add labels and a color bar
plt.xlabel('x1')
plt.ylabel('x2')
plt.colorbar(contour, label='Function Value')


# Save the plot as a PDF file
plt.savefig(f'experiments/plots/figure4.pdf', format='pdf')
