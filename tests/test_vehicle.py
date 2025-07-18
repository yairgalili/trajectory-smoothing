from hydra.core.global_hydra import GlobalHydra
from hydra import initialize, compose
import matplotlib.pyplot as plt
import numpy as np
import pytest

from src.vehicle import find_closest_segment_and_point, load_and_smooth

"""
load cfg yaml for tests
"""
@pytest.fixture
def hydra_config():
    # Initialize Hydra
    GlobalHydra.instance().clear()
    with initialize(config_path="configs", version_base=None):
        cfg = compose(config_name="test_vehicle")
    return cfg

def test_load_and_smooth(hydra_config, plot=False):
    """
    Test the load_and_smooth function.
    The function load the trajectory from the input file and smooth it by mean filtering.
    The function should raise an error if the trajectory is not a 2D array.
    The function should raise an error if the trajectory has less than window_size points.
    The function should raise an error if the trajectory has less than 2 points.
    The function should raise an error if the window size is less than 3.
    """
    cfg = hydra_config 
    filtered_trajectory = load_and_smooth(cfg["load_and_smooth"]["file_path"])

    assert np.all(np.isfinite(filtered_trajectory))
    assert len(filtered_trajectory.shape) == 2
    assert filtered_trajectory.shape[1] == 2
    
    if plot:
        plt.plot(filtered_trajectory[:, 0], filtered_trajectory[:, 1], 'r*')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Filtered Trajectory")
        plt.savefig("tests/data/filtered_trajectory.jpg")



def test_find_closest_segment_and_point(hydra_config):
    """
    Test the find_closest_segment_and_point function.
    The function should return the closest segment and the nearest point on the segment.
    The function should raise an error if the trajectory has less than 2 points.
    The function should raise an error if the point has less than 2 coordinates.
    """
    cfg = hydra_config
    trajectory = np.array(cfg["find_closest_segment_and_point"]["trajectory"])
    point = np.array(cfg["find_closest_segment_and_point"]["query_point"])
    closest_segment, closest_point = find_closest_segment_and_point(trajectory, point)
    assert np.isclose(closest_point, cfg["find_closest_segment_and_point"]["closest_point"]).all()
    assert np.isclose(closest_segment, cfg["find_closest_segment_and_point"]["closest_segment"]).all()