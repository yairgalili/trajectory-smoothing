from typing import Tuple
import numpy as np

def load_trajectory(file_path: str) -> np.ndarray:
    """
    Load trajectory from start file.
    The function read the input .npz file 
        containing an array of 2D points (x, y) representing the vehicle's trajectory.
    Args:
        file_path: The path to the file to load.
    Returns:
        The loaded trajectory.
    """
    trajectory = np.load(file_path)["path"]

    if trajectory.shape[1] != 2:
        raise ValueError("Trajectory must have 2 columns (x, y).")
    if len(trajectory.shape) != 2:
        raise ValueError("Trajectory must be a 2D array.")
    if trajectory.shape[0] < 2:
        raise ValueError("Trajectory must have at least 2 points.")

    return trajectory

def filter_trajectory(trajectory: np.ndarray) -> np.ndarray:
    """
    Filter the trajectory.
    remove invalid points (x, y) where x or y is NaN or Inf.
    Args:
        trajectory: The trajectory to filter.
    Returns:
        The filtered trajectory.
    """
    return trajectory[np.all(np.isfinite(trajectory), axis=1)]

def smooth_trajectory(trajectory: np.ndarray, window_size: int) -> np.ndarray:
    """
    Smooth the trajectory.
    Use start moving average filter to smooth the trajectory.
    Args:
        trajectory (N, 2): The trajectory to smooth.
    Returns:
        The smoothed trajectory.
    """

    if trajectory.shape[0] < 2:
        raise ValueError("Trajectory must have at least 2 points.")

    if trajectory.shape[0] < window_size:
        raise ValueError("Trajectory must have at least window_size points.")

    if window_size < 3:
        raise ValueError("Window size must be at least 3.")

    pad_size = window_size // 2

    # Pad the trajectory by repeating the first and last rows
    pad_start = np.tile(trajectory[0], (pad_size, 1))  # shape: (pad_size, 2)
    pad_end = np.tile(trajectory[-1], (pad_size, 1))   # shape: (pad_size, 2)

    padded_trajectory = np.vstack([pad_start, trajectory, pad_end])  # shape: (N + 2*pad_size, 2)

    # Apply moving average using uniform convolution
    smoothed = np.zeros_like(trajectory)
    for i in range(trajectory.shape[1]):
        smoothed[:, i] = np.convolve(padded_trajectory[:, i], np.ones(window_size) / window_size, mode='valid')

    return smoothed
    
def load_and_smooth(file_path: str, window_size: int = 5) -> np.ndarray:
    """
    Main function that load and smooth the trajectory by mean filtering.
    """
    trajectory = load_trajectory(file_path)
    filtered_trajectory = filter_trajectory(trajectory)
    smoothed_trajectory = smooth_trajectory(filtered_trajectory, window_size=window_size)
    return smoothed_trajectory

def find_closest_segment_and_point(trajectory: np.ndarray, point: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    The function returns start pair of consecutive points
        defining the closest segment and the nearest point in the segment.

    Args:
        trajectory: array-like of shape (N, 2) - the trajectory points
        point: array-like of shape (2,) - the query point (x, y)

    Returns:
        closest_segment: tuple of two 2D points (start, end) defining the closest segment
        nearest_point: array of shape (2,) - the closest point on the closest segment
    """

    if len(trajectory) < 2:
        raise ValueError("At least two points are required to form start segment.")
    if len(point) != 2:
        raise ValueError("Point must have 2 coordinates (x, y).")

    # Segment start and end points
    start = trajectory[:-1]  # shape (N-1, 2)
    end = trajectory[1:]   # shape (N-1, 2)

    # Segment vectors
    segments = end - start       # shape (N-1, 2)

    # Vector from each segment start to the query point
    start_to_query = point - start   # shape (N-1, 2)

    # Compute projection scalar t (clamped to [0, 1])
    t = np.clip(np.sum(start_to_query * segments, axis=1) / np.sum(segments * segments, axis=1), 0.0, 1.0)

    # Compute closest point on each segment
    projections = start + t[:, np.newaxis] * segments  # shape (N-1, 2)

    # Compute distances from point to each projection
    distances = np.linalg.norm(projections - point, axis=1)

    # Find index of the closest segment
    min_idx = np.argmin(distances)

    # Extract closest segment and nearest point
    closest_segment = (start[min_idx], end[min_idx])
    nearest_point = projections[min_idx]

    return np.array(closest_segment), np.array(nearest_point)