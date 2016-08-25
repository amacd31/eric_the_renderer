Eric the Renderer
=================

Renders data files as a plot.

Usage
-----

Run the script with Python passing in the name of the file to render.

Using the included example data file:

::

 python render.py example.txt

Help information can be found with the --help option:

::

 python render.py --help

Render on a 100 x 100 grid with a line 5 thick:

::

 python render.py --linewidth=5 --axis-size=100 example.txt
