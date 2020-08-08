# skyglow-heatmaps
Light Pollution Heatmaps of Pittsburgh, for the summer 2020 CMU skyglow class.

By Ela Gulsen

![pittsburgh heatmap](https://github.com/elagulsen/skyglow-heatmaps/blob/master/img/heatmap.png?raw=true)

This project uses datasets provided by Globe at Night and Dark Sky Meter.

Check out the skyglow class website [here!](https://skyglow-cmu.github.io/index.html)

# usage
heatmap.py generates heat maps based on user input.

You can customize the dimension, radius of color around each point, sigma (blurring factor), and alpha (transparency of the heat map layered over the map of Pittsburgh).

To run the map with default settings, you can simply run ```python heatmap.py```.

To customize the settings, you can use command line arguments: DIM=[your dimension], SIGMA=[your sigma], RADIUS=[your radius], and ALPHA=[your alpha] (in any order and any combination). (You can also use the shorthand D=, S=, R=, and A=).

Here are some recommended settings to try!

```python heatmap.py DIM=500 RADIUS=20```

Creates a nicely blurred map with a relatively large radius of color around each point.

```python heatmap.py DIM=500 RADIUS=10 SIGMA=0```

Creates a map of points with no color blurring.

```python heatmap.py DIM=1000 RADIUS=40```

Creates a high definition map with blurring and a relatively large radius of color around each point.

Be careful, high definition maps may take longer to generate.
