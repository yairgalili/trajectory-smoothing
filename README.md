# Vehicle Trajectory - RESTful API

## Overview

This document outlines the design of a RESTful API that provides access
to trajectory processing features including:

-   Filtering

-   Path Smoothing

-   Finding closest segments and nearest point on a trajectory

This API is intended to be integrated into geospatial applications and
autonomous systems.

## Key Features
| Feature | Description |
| -------- | ------- |
| Filtering | Filter nonfinite points on the trajectory|
| Smoothing | Apply mean filter on the trajectory |
| Closest segment and point | Find the closest segment and nearest point on a trajectory for a given point|
  -----------------------------------------------------------------------

## API ENDPoints
| Endpoint | Method | Description |
| -------- | ------- | ------- |
| /login | Get | Authenticate|
| /filter | Post | Filter nonfinite points on the trajectory |
| /smooth | Post | Apply mean filter on the trajectory |
| /closest-segment | Post | Find the closest segment and nearest point on a trajectory for a given point|

  -----------------------------------------------------------------------

## Data structures

### General formats

-  Trajectory data: List\[List\[float\]\]

    - The trajectory is a list of two points that defines the path, for e.g. \[\[0, 0\], \[1, 0\], \[2, 1\], \[3, 3\]\]

### API

- Login

   - Input:  

      - User_name: str

      - Password: str

   - Output: 

      - token: str

- Filter

  - Input:  

    - trajectory: List\[List\[float\]\]

  -  Output: 

      - trajectory: List\[List\[float\]\]

- Smooth

  - Input:  

    - trajectory: List\[List\[float\]\]

    - window_size: int - This parameter defines the window size of the mean filter.

  - Output:  

    - trajectory: List\[List\[float\]\]

- Closest segment and nearest point

  - Input:  

    - trajectory: List\[List\[float\]\]

    - point: List\[float\] - This parameter defines the query point coordinates.

  - Output:  

    - Closest_segment: Tuple\[List\[float\]\] - Tuple of the points, which are the edges of the closest section.

    - Nearest_point: List\[float\] - The coordinates of the nearest point in the closest section to the query point.

## Error management

  -----------------------------------------------------------------------
| HTTP status | Description |
| -------- | ------- |
| 200 - OK | Success|
| 400 - Bad Request | Malformed Input (Invalid data structure) |
| 401 - Unauthorized | Missing or invalid authentication token |
| 422 - Unprocessable Entity |Input is valid but cannot be processed (e.g. empty trajectory)|

  -----------------------------------------------------------------------

##  Authentication

-   Authentication Strategy: API token (header based)

## Technology stack
   - Python 3.12
      - Programming Language
  - Pydantic
      - Data validation
   - FastAPI
      - Rest API framework
  - Docker
    - Containerization
  - Gunicorn
      - ASGI server
  - Kubernetes
      - Orchestration
  - PyJWT
      - Authentication
  - Pytest
      - Testing
  ---------------------------------------------------------------------------
