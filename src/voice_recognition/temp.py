import numpy as np
import matplotlib.pyplot as plt

def main():
    # Generate x values from 0 to 4*pi
    x = np.linspace(0, 4 * np.pi, 1000)
    
    # Calculate the sine of each x value
    y = np.sin(x)

    # Create a new figure
    plt.figure()

    # Plot the sine curve
    plt.plot(x, y, label="y = sin(x)")
    plt.title("Sine Curve")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    
    # Display the plot
    plt.show()

if __name__ == "__main__":
    main()

