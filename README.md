### NASA Asteroid Data Science Project

This project analyzes real-world NASA data of asteroids approaching Earth using Python.  
It includes data cleaning, feature extraction, and various visualizations to better understand asteroid characteristics.

### Features

- Filtered asteroid data by close approach year (from 2000 onward)
- Found:
  - Brightest asteroid (max absolute magnitude)
  - Closest asteroid to Earth
  - Average diameters (min and max)
  - Most common orbits
- Visualizations:
  -  Histogram of asteroid diameters
  -  Histogram of orbit intersection values
  -  Pie chart of hazardous vs. non-hazardous asteroids
  -  Linear regression: Absolute Magnitude vs. Speed (mph)

### Technologies Used

- Python
- NumPy
- Matplotlib
- SciPy

### Input

The project expects a CSV file named `nasa.csv` in the same directory, containing asteroid data.

### How to Run

```bash
python nasa_astroid_ds.py
