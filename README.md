# Power_Network_Model

Python program to generate power network model for calculating [geomagnetically induced currents](https://en.wikipedia.org/wiki/Geomagnetically_induced_current).

The program handles different types of transformers (Auto and two-winding), and multiple transformers per substation. It connects correctly between voltage systems. In addition, parallel connections between substations are handled.

Uses the approach outlined [here](http://onlinelibrary.wiley.com/doi/10.1002/2016SW001499/full).

## Installation
```python
pip install power_network_model
```

## Quick Code Example
If you have two .csv files with network information- one for connections, one for transformers:
```python
import pkg_resources
import power_network_model as PNM
import power_network_model.plotter as PNMplot

# read in transformer file, generate substation data:
trafo_filename = pkg_resources.resource_filename("power_network_model", 'Data/Horton_Input_Trafos.csv')
ss_trafos, ss_connections, ss_meta = PNM.make_substations(trafo_filename)

# Generate connections between substations:
connections_filename = pkg_resources.resource_filename("power_network_model", 'Data/Horton_Input_Connections.csv')
connections_twixt_stations = PNM.connections_adder(connections_filename, ss_meta)

# Write out the output files
filename = "Horton_Output"
nodes_output, connections_output = PNM.write_out(filename, ss_trafos, ss_connections, connections_twixt_stations)

################################################################################
# If you want to plot the output:
PNMplot.network_plotter(nodes_output, connections_output, ["red", "blue"], "Horton Model")
```
## **Inputs Required**
The two .csv file inputs need to be in the following format:

Transformer information in a csv file with columns:
 - SS_NAME = Subsation name (important to keep spelling uniform)
 - SS_SYM = Substation symbol
 - TF_SYM = Transformer symbol (or code: e.g, T1432)
 - VOLTAGE = Highest operating voltage of the substation
 - LAT = Latitude
 - LON = Longitude
 - TYPE = Type of transformer: 'A' = autotransformer, "YY" = Wye-Wye, "G" = grounded, "T" = Tee connection station.
 - RES1 = High voltage resistance winding
 - RES2 = Low voltage resistance winding
 - GROUND = Ground resistance at substation
 - SWITCH = Transformer ground switch: 0 = None, 1 = Open, 2 = Closed
  
Connections information in a csv file with columns:
 - FROM = Substation name from
 - TO = Substation name to
 - VOLTAGE = Voltage of connection
 - CIRCUIT = To denote multiple lines per connection
 - RES = Resistance of line.

Verified with the [Horton 2012](http://ieeexplore.ieee.org/abstract/document/6298994/) model (included in Data/).
After calculating GICs for a uniform electric field, compared to Horton:
![Comparison](https://cloud.githubusercontent.com/assets/20742138/23833590/0e27c958-0740-11e7-9ae6-beaf2dda4ed4.png)

Horton_Plotter.py gives the following:
![Horton_Network](https://cloud.githubusercontent.com/assets/20742138/23833656/8c753db8-0740-11e7-9b63-981efeee10f4.png)

Finally, when applied to a larger network such as Ireland:
![irish_power_network](https://cloud.githubusercontent.com/assets/20742138/23032365/ffc3b020-f46b-11e6-85d7-3b0ad793ca57.png)


## **Author**
Written by Sean Blake in Trinity College Dublin, 2017

Email: blakese@tcd.ie

GITHUB: https://github.com/TerminusEst

Uses the MIT license.
