# Power_Network

Python program to generate power network model for calculating geomagnetically induced currents.

The program handles different types of transformers (Auto and two-winding), and multiple transformers per substation. 

Uses the approach outlined [here](http://onlinelibrary.wiley.com/doi/10.1002/2016SW001499/full).

##**Inputs Required**
Transformer information:
  - Substation name, Substation code, Voltage, Lat, Lon, Type, Res1, Res2, Ground, Switchable
  
Connections information:
  - Station_from, Station_to, Voltage, Circuit ID, Transmission Res

Gives a tasty model which looks like the following:

![irish_power_network](https://cloud.githubusercontent.com/assets/20742138/23032365/ffc3b020-f46b-11e6-85d7-3b0ad793ca57.png)


##**Author**
Written by Sean Blake in Trinity College Dublin, 2017

Email: blakese@tcd.ie

GITHUB: https://github.com/TerminusEst

Uses the MIT license.
