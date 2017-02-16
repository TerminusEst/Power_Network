from collections import Counter

"""

1) Make "master" list of substations.
2) Loop through transformers. Add each transformer to respective substation.
3) For each substation, calculate internal configuration
4) write transformers to output format, keeping correct trafo numbers.
5) worry about connections
6) Write-out output, 

The file inputs are 

1) Transformer data
    - Name, Code, Voltage, Lat, Lon, Type, Res1, Res2, Ground, Switchable

2) Connections
    - Station_from, Station_to, Voltage, Circuit ID, Transmission Res

"""

execfile("/home/blake/Drive/Network_Analysis/master_Eirgrid/PNG_Functions.py")
################################################################################
# 1
# Make "master" list of substations.
# Substations should be in the form:
# NAME, SYMBOL, VOLTAGE, LAT, LON, TYPE (1,2,3,4 - Auto, YY, Reg, T), WIND RES1, WIND RES2, GROUND RES, Switch
filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Input/Substation_Names.txt"
f = open(filename, 'r')
data = f.readlines()
f.close()

# Read in data, skip first row (headings), skip last row (empty)
master = [x.split("\t") for x in data[1:-1]]
voltages = [x[2] for x in master]

substation_names = []
substation_volt = []
substation_sym = []

for j in master:
    if j[0] not in substation_names:
        substation_names.append(j[0])
        substation_volt.append(j[2])
        substation_sym.append(j[1])

master_substations = substation_sym

################################################################################
# 2
# Loop through trafos, add each to respective substation.

master_raw = []
for i in master_substations:
    temp_list = []

    for index, value in enumerate(master):
        if i == value[1]:
            temp_list.append(value)

    master_raw.append(temp_list)

################################################################################
# 3
# For each substation, calculate internal configuration

refined_trafos = []
refined_connection = []

refined_trafos, refined_connections, substation_meta = [], [], []

count = 1
test_list = []

for index, i in enumerate(master_raw):

    a, b, c = substation_internals(i)
    aa, bb, cc, count = number_adder(a, b, c, count)

    refined_trafos.append(aa)
    refined_connections.append(bb)
    substation_meta.append(cc)

    for k in aa:
        test_list.append(k[0])

################################################################################
# 5
# Generate connections between substations

folder = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Input/"
connection_files = ["connect_400.txt", "connect_275.txt", "connect_220.txt", "connect_110.txt", "connect_NI110.txt"]
voltages = ["400", "275", "220", "110", "110"]

refined_connections_twixt_stations = []
ss_meta = [x[0] for x in substation_meta]

for filename, volt in zip(connection_files, voltages):
    filename = folder + filename
    refined_connections_twixt_stations = connections_adder(filename, volt, refined_connections_twixt_stations)

################################################################################
# 6
# Write out the output file
filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/output.txt"
write_out(filename, refined_trafos, refined_connections, refined_connections_twixt_stations)

# Write out substation meta data
filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/Substation_meta.txt"
write_substation_data(filename, substation_meta)

#-------------------------------------------------------------------------------
# connections_meta

filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/Connections_meta.txt"
write_connections_data(filename, refined_connections_twixt_stations)

