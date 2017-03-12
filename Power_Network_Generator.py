"""Program to make power network model from transformer information and connections.

    Required for this program is 2 inputs:

    1) csv file containing transformer info. The columns should be:

        SS_NAME = Subsation name (important to keep spelling uniform)
        SS_SYM = Substation symbol
        TF_SYM = Transformer symbol (or code: e.g, T1432)
        VOLTAGE = Highest operating voltage of the substation
        LAT = Latitude
        LON = Longitude
        TYPE = Type of transformer: 'A' = autotransformer, "YY" = Wye-Wye, "G" = grounded, "T" = Tee connection station.
        RES1 = High voltage resistance winding
        RES2 = Low voltage resistance winding
        GROUND = Ground resistance at substation
        SWITCH = Transformer ground switch: 0 = None, 1 = Open, 2 = Closed

    2) csv file containing substation connection info. The columns should be:
        FROM = Substation name from
        TO = Substation name to
        VOLTAGE = Voltage of connection
        CIRCUIT = To denote multiple lines per connection
        RES = Resistance of line.

    An example of the code running for the Horton et al 2012 test case paper is outlined below:

"""

import PNG_Functions as PNG
################################################################################

# read in transformer file, generate substation data:
filename = "Data/Horton_Trafo_Info.csv"
ss_trafos, ss_connections, ss_meta = PNG.make_substations2(filename)

# Generate connections between substations:
filename = "Data/Horton_Connection_Info.csv"
connections_twixt_stations = PNG.connections_adder(filename, ss_meta)

################################################################################
# Write out the output file
filename = "Data/Horton_Model_Output.txt"
PNG.write_out(filename, ss_trafos, ss_connections, connections_twixt_stations)













