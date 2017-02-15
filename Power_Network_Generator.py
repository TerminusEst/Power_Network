from collections import Counter

"""
1) Make "master" list of substations.
2) Loop through transformers. Add each transformer to respective substation.
3) For each substation, calculate internal configuration
4) write transformers to output format, keeping correct trafo numbers.
5) worry about connections

6) Add in problem sites- Prospect, Woodland2, Louth
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
# Final write out
# write transformers to output format, keeping correct trafo numbers.
filename = "output.txt"

write_out(filename, refined_trafos, refined_connections, refined_connections_twixt_stations)

"""
filename = "Connections_meta.txt"
f = open(filename, 'w')

bleh1, bleh2 = [], []

for i in refined_connections2:
    if ((i[0], i[1]) not in bleh2) and ((i[1], i[0]) not in bleh2):
        bleh2.append((i[0], i[1]))

        bleh1.append([i[0], i[1], i[-1]])

coords = []

refined_trafos2 = []
for i in refined_trafos:
    refined_trafos2.extend(i)


for i in bleh1:
    nf = i[0]
    nf_lat = refined_trafos2[nf-1][1]
    nf_lon = refined_trafos2[nf-1][2]

    nt = i[1]
    nt_lat = refined_trafos2[nt-1][1]
    nt_lon = refined_trafos2[nt-1][2]

    v = i[-1]

    f.write(str(nf_lat) + "\t" + str(nf_lon) + "\t" + str(nt_lat) + "\t" + str(nt_lon) + "\t" + str(v) + "\n")
"""

# FIX META_DATA - trafos should have 1 value for HV, LV
# Connections. Make list of connections, sum their resistances
# sort out TEE connections

# loop through final list of connections
# go to substation in SUBSTATION_META
# work out if its HV-HV, LV-LV or not etc
# get numbers and resistance
# profit
# add in exceptional cases (MP, MAYNOOTH, TANDRAGEE, LOUTH etc)















































