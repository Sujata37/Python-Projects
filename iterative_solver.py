# image inpainting to solve 2d laplace equation

import numpy as np
import matplotlib.pyplot as plt


def step_jacobi_2D(u: np.ndarray, mask: np.ndarray, omega: float = 1.0) -> np.ndarray:
    """
    Performs one step of the Jacobi iteration for solving the Laplace equation in 2D.

    Parameters
    ----------
    u : array_like
            Current iterate
    mask : array_like
            Mask indicating which points are to be updated
    omega : float, optional
            Relaxation parameter (default is 1.)

    Returns
    -------
    u : array_like
            Updated iterate
    """
    u_new = u.copy()
    avg_neighbors = (
        np.roll(u, +1, axis=0) +  
        np.roll(u, -1, axis=0) +  
        np.roll(u, +1, axis=1) +  # Left
        np.roll(u, -1, axis=1)    # Right
    ) / 4.0

    u_new[mask] = (1 - omega) * u[mask] + omega * avg_neighbors[mask]
    return u_new


def step_sor_2D(u: np.ndarray, mask: np.ndarray, omega: float = 1.0) -> np.ndarray:
    """
    Performs one step of the SOR (Successive Over-Relaxation) iteration for solving the Laplace equation in 2D.

    Parameters
    ----------
    u : array_like
            Current iterate
    mask : array_like
            Mask indicating which points are to be updated
    omega : float, optional
            Relaxation parameter (default is 1.)

    Returns
    -------
    u : array_like
            Updated iterate
    """
    nrows, ncols = u.shape

    # Go through each pixel
    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            if mask[i, j]:
                # Average of 4 neighbors (use the latest values)
                avg = (u[i+1, j] + u[i-1, j] + u[i, j+1] + u[i, j-1]) / 4.0
                # Update in-place using the relaxation formula
                u[i, j] = (1 - omega) * u[i, j] + omega * avg

    return u



def inpaint_jacobi(image: np.ndarray, mask: np.ndarray, tol: float = 1e-10, max_iter: int = 1000, omega: float = 1.0) -> tuple[np.ndarray, int]:
    """
    Solves the Laplace equation in 2D using the Jacobi iteration.

    Parameters
    ----------
    image : array_like
            Input image
    mask : array_like
            Mask indicating which points are to be updated
    tol : float, optional
            Tolerance for convergence
    max_iter : int, optional
            Maximum number of iterations
    omega : float, optional
            Relaxation parameter

    Returns
    -------
    u : array_like
            Inpainted image
    it : int
            Number of iterations
    """
    u = image.copy()

    for it in range(max_iter):
        u_new = step_jacobi_2D(u, mask, omega)
        # Measure how much it changed
        diff = np.linalg.norm(u_new[mask] - u[mask])

        u = u_new

        # Stop for small change
        if diff < tol:
            return u, it + 1  # Return image and number of steps used

    return u, max_iter

def inpaint_sor(image: np.ndarray, mask: np.ndarray, tol: float = 1e-10, max_iter: int = 1000, omega: float = 1.0) -> tuple[np.ndarray, int]:
    """
    Solves the Laplace equation in 2D using the SOR iteration.

    Parameters
    ----------
    image : array_like
            Input image
    mask : array_like
            Mask indicating which points are to be updated
    tol : float, optional
            Tolerance for convergence
    max_iter : int, optional
            Maximum number of iterations
    omega : float, optional
            Relaxation parameter

    Returns
    -------
    u : array_like
            Inpainted image
    it : int
            Number of iterations
    """
    u = image.copy()

    for it in range(max_iter):
        u_old = u.copy()
        u = step_sor_2D(u, mask, omega)

        diff = np.linalg.norm(u[mask] - u_old[mask])

        # Stop for small change
        if diff < tol:
            return u, it + 1

    return u, max_iter


def find_optimal_omega_sor(image: np.ndarray, mask: np.ndarray, omega_values: np.ndarray = None, nIter: int = 1000, abstol: float = 1e-10) -> tuple[np.ndarray, int]:
    """
    Test a range of omega values for SOR and return the optimal omega (fastest convergence).

    Parameters
    ----------
    image : array_like
            Input image
    mask : array_like
            Mask indicating which points are to be updated
    omega_values : iterable, optional
            Range of omega values to test.
    nIter : int
            Maximum number of SOR iterations
    abstol : float
            Residual tolerance

    Returns
    -------
    omega_opt : float
            Omega with fastest convergence
    min_iters : int
            Number of iterations for optimal omega
    """
    if omega_values is None:
        omega_values = np.arange(1.0, 2.0, 0.05)

    best_omega = None
    fewest_iters = nIter

    for omega in omega_values:
        _, iters = inpaint_sor(image, mask, tol=abstol, max_iter=nIter, omega=omega)

        if iters < fewest_iters:
            best_omega = omega
            fewest_iters = iters

    return best_omega, fewest_iters


if __name__ == '__main__':
    # Load image
    image = np.loadtxt('image.txt')

    # Create mask
    mask = np.zeros_like(image, dtype=bool)
    mask[60:70, 30:70] = True
    
    # Create damaged image
    damaged = image.copy()
    damaged[mask] = 0.0

    # Refine with Jacobi
    refined_jacobi, it_jacobi = inpaint_jacobi(damaged, mask)

    # Refine with SOR
    refined_sor, it_sor = inpaint_sor(damaged, mask)

    # Plot
    fig, axs = plt.subplots(1, 4, figsize=(14, 4))
    axs[0].imshow(image, cmap='gray')
    axs[0].set_title("Original")
    axs[1].imshow(damaged, cmap='gray')
    axs[1].set_title("Damaged")
    axs[2].imshow(refined_jacobi, cmap='gray')
    axs[2].set_title("Jacobi")
    axs[3].imshow(refined_sor, cmap='gray')
    axs[3].set_title("SOR")
    for ax in axs:
        ax.axis('off')
    plt.tight_layout()
    plt.show()
