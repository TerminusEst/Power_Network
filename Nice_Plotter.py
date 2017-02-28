import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.patheffects as path_effects
import seaborn as sns
sns.set()
################################################################################
# Plot 1 - Traformers

clf()

fig = plt.figure(1)
ax = plt.subplot(111)

water = "CadetBlue"
land = "AliceBlue"

ww = 'white'
bb = 'black'

m = Basemap(projection = 'merc', llcrnrlat= 51.3, urcrnrlat= 55.5, llcrnrlon=-10.5, urcrnrlon=-5, resolution='h',area_thresh=100)
m.drawcoastlines(color = 'k', linewidth = 2)
m.drawparallels(np.arange(0,360,1) ,labels=[1, 0, 0, 0], color = 'k', fontsize =24)
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

# Get a legend up in the club

x, y = m([-4, -3], [1, 2])

plot(x, y, 'or', label = "400kV Station")
plot(x, y, 'ob', label = "275kV Station")
plot(x, y, 'og', label = "220kV Station")
plot(x, y, 'ok', label = "110kV Station")

plot(x, y, 'r', label = "400kV Line")
plot(x, y, 'b', label = "275kV Line")
plot(x, y, 'g', label = "220kV Line")
plot(x, y, ':k', label = "110kV Line")

leg = legend(loc = "upper left", fontsize = 18, markerscale = 1.5, frameon = True, fancybox = True)
frame = leg.get_frame()
frame.set_color('white')

title("Model B", fontsize = 24)




# INTERCONNECTORS

xs = [-5.7865, -4]
ys = [54.843, 54.843 + 1]
x, y = m(xs, ys)
plot(x, y, '--', color = 'DarkOrange', lw = 4)
#thing = text(x[0], y[0], "      Moyle\nInterconnector", fontsize = 22, color = "white", zorder = 1000)
thing = text(x[0] - 80000, y[0] + 50000, "      Moyle\nInterconnector", fontsize = 22, color = "white", zorder = 1000)
thing.set_path_effects([path_effects.Stroke(linewidth=5, foreground='black'), path_effects.Normal()])

xs = [-6.5694, -4]
ys = [53.4756, 53.4756]
x, y = m(xs, ys)
plot(x, y, '--', color = 'DarkOrange', lw = 4)
thing = text(x[0] + 40000, y[0] + 40000, "   East-West\nInterconnector", fontsize = 22, color = "white", zorder = 10000)
thing.set_path_effects([path_effects.Stroke(linewidth=5, foreground='black'), path_effects.Normal()])



plt.show()

################################################################################
################################################################################




























