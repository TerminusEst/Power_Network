import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.patheffects as path_effects

################################################################################
# Plot 1 - Traformers

clf()

fig = plt.figure(1)
ax = plt.subplot(111)

water = "CadetBlue"
land = "AliceBlue"

ww = 'white'
bb = 'black'

m = Basemap(projection = 'merc', llcrnrlat= 51.3, urcrnrlat= 55.5, llcrnrlon=-10.5, urcrnrlon=-5, resolution='l',area_thresh=100)
m.drawcoastlines(color = 'k', linewidth = 2)
m.drawparallels(np.arange(0,360,0.5) ,labels=[1, 0, 0, 0], color = 'k', fontsize =24)
m.drawmeridians(np.arange(0,360,1),labels=[0,0,0,1], color = 'k', fontsize =24)
m.drawcountries(linewidth = 2)
m.drawmapboundary(fill_color=water)
m.fillcontinents(color=land,lake_color=water)

# read in substations
filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/Substation_meta.txt"
f = open(filename, 'r')
data = f.readlines()
f.close()

sslats, sslons, ssvolts, sizes = [], [], [], []
for i in data:

    j = i.split("\t")

    sslats.append(float(j[2]))
    sslons.append(float(j[3]))

    volti = ["400", "275", "220", "110"].index(j[4])
    color = ["r", "b", "g", "k"][volti]

    if volti == 3:
        sizes.append(100)
    else:
        sizes.append(200)

    ssvolts.append(color)

xxx, yyy = m(sslons, sslats)
scatter(xxx[::-1], yyy[::-1], s = sizes[::-1], c = ssvolts[::-1], zorder = 1000)

# read in connections
filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/Connections_meta.txt"
data = np.loadtxt(filename)

cvolts, clatfrom, clonfrom, clatto, clonto = data[:,0], data[:,1], data[:,2], data[:,3], data[:,4]

for v, t1, n1, t2, n2 in zip(cvolts, clatfrom, clonfrom, clatto, clonto):
    xxx, yyy = m([n1, n2], [t1, t2])

    if v == 110.0:
        lss = ":"
    else:
        lss = "-"

    volti = [400.0, 275.0, 220.0, 110.0].index(v)
    color = ["r", "b", "g", "k"][volti]



    plot(xxx, yyy, color = color, linestyle = lss, lw = 2)


plt.show()

################################################################################
################################################################################




























