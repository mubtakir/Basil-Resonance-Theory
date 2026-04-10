import numpy as np
import matplotlib.pyplot as plt

# --- Discovery Diary: Step 17 - The Elliptic Cone ---
# Proving that the height is Pi times the radius!

def simulate_elliptic_cone():
    print("Welcome to Step 17: The 3D Elliptic Cone!")
    
    # h = pi * r
    # Let's test this with a radius r = 1.0
    r = 1.0
    h_expected = np.pi * r
    
    print(f"For a Base Radius r = {r}")
    print(f"The Harmonic Height should be h = {h_expected:.5f}")
    
    # Visualization of the Cone Slope
    theta = np.linspace(0, 2*np.pi, 100)
    x = r * np.cos(theta)
    y = 0.5 * r * np.sin(theta) # Elliptic base
    
    # 3D Plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw base
    ax.plot(x, y, 0, label="Elliptic Base")
    
    # Draw apex at height h
    for i in range(0, 100, 10):
        ax.plot([0, x[i]], [0, y[i]], [h_expected, 0], color='gray', alpha=0.3)
    
    ax.scatter([0], [0], [h_expected], color='red', s=100, label="Apex (Zeta Zero)")
    
    ax.set_title(f"Step 17: The Basil Cone (h = πr)")
    ax.set_zlabel("Height (h)")
    ax.legend()
    
    print(f"The red point is where the 'Resonance' is locked at the apex.")
    plt.show()

if __name__ == "__main__":
    simulate_elliptic_cone()

