import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.patheffects as path_effects

################################################################################

def on_pick(event):

    if isinstance(event.artist, Line2D):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()

        a = list(xdata) + list(ydata)
        num = ref_points.index(a)

        if str(event.artist.get_linestyle()) == "-":
            event.artist.set_linestyle("--")
        else:
            event.artist.set_linestyle("-")

        connections[num] = 1 - connections[num]

        #print "Line", num, ":", connections[num]
        print "Num: ", num
        print "R_l: ", lineresist[num]
        print "\n"

    if "matplotlib.collections.PathCollection" in str(event.artist):
        num = int(str(event.ind[0]))
        grounds[num] = 1 - grounds[num]

        if grounds[num] == 0.0:
            coll._facecolors[num] = np.array([0., 0., 0., 0.])
        else:
            coll._facecolors[num] = colors[num]
    
        #print "Point", num, ":", grounds[num]
        #print num,"\n"
        print "Num: ", num
        print "R_t: ", transresist[num]
        print "R_e: ", earthresist[num]
        print "Name: ", site_name[num]
        print "\n"

    fig.canvas.draw()
    
    return

################################################################################
# READ IN DATA
#-------------------------------------------------------------------------------
# Substations

#filename = "/home/blake/Drive/Network_Analysis/Program/Input/test_trans9.txt"
#filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/output_with_PRO2MP_paralell_connections.txt"
filename = "/home/blake/Drive/Network_Analysis/master_Eirgrid/Output/test.txt"

a, b, c, d, e, f = np.loadtxt(filename, usecols = (0, 1, 2, 3, 4, 5), unpack = True)

f = open(filename, 'r')
data = f.readlines()
f.close()

nnodes = 541#511#56
nconnects = len(a) - nnodes

site_name = [x.split("\t")[-1] for x in data[:nnodes]]

sitenum = a[0:nnodes]
geolat = b[0:nnodes]
geolon = c[0:nnodes]


transresist = d[0:nnodes]
earthresist = e[0:nnodes]

grounds = np.ones(len(geolon))
voltages = [400]*16 + [275]*61 + [220]*204 + [110]*302
colors = [[[1., 0., 0., 1.], [0., 0., 1., 1.], [0., 0.50196078, 0., 1.], [0, 0, 0, 0.5]][[400, 275, 220, 110].index(x)] for x in voltages]

#-------------------------------------------------------------------------------
# Connections
nodefrom = a[nnodes:]
nodeto = b[nnodes:]

latsfrom = [geolat[list(sitenum).index(x)] for x in nodefrom]
lonsfrom = [geolon[list(sitenum).index(x)] for x in nodefrom]

latsto = [geolat[list(sitenum).index(x)] for x in nodeto]
lonsto = [geolon[list(sitenum).index(x)] for x in nodeto]

lineresist = c[nnodes:]

connections = np.ones(len(latsfrom))

t_cnn = sorted(list(set(list(nodefrom) + list(nodeto))))

#for i in range(1, 511, 1):
#    if i not in t_cnn:
#        print i, site_name[i-1]

################################################################################
# Plot 1 - Initial Selection

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

xxx, yyy = m(geolon, geolat)
coll = ax.scatter(xxx, yyy, color=colors, picker = 2, s=200, zorder = 100)

ref_points = []

for index, value in enumerate(nodefrom):
    
    a = [lonsfrom[index], lonsto[index]]
    b = [latsfrom[index], latsto[index]]
    xxx, yyy = m(a, b)

    plot(xxx, yyy, c = 'k', picker=2, linestyle = "-", zorder = 100)

    ref_points.append(xxx + yyy)
    
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', on_pick)

title("Substation in Model B", fontsize = 24)

plt.show()

################################################################################
################################################################################
# Output:

def super_output():
    try:
        filename = "/home/blake/Drive/Network_Analysis/Program/Input/output.txt"

        f = open(filename, 'w')

        for i, v in enumerate(grounds):
            mystr = ""

            if v == 1:
                res = earthresist[i]
            if v == 0:
                res = "10000000.0"

            mystr += str(int(sitenum[i])) + "\t" + str(geolat[i]) + "\t" + str(geolon[i]) + "\t0.5\t" + str(res) + "\n"

            f.write(mystr)

        for i, v in enumerate(connections):
            mystr = ""

            if v == 0:
                continue
            else:
                mystr += str(int(nodefrom[i])) + "\t" + str(int(nodeto[i])) + "\t" + str(lineresist[i]) + "\tnan\tnan\n"

            f.write(mystr)

        f.close()

        print "Exported to: ", filename

    except:
        print "Something went wrong..."

def super_output2():
    filename = "/home/blake/Drive/Network_Analysis/Program/Input/output.txt"

    f = open(filename, 'w')

    for i, v in enumerate(grounds):
        mystr = ""

        if v == 1:
            res = earthresist[i]
        if v == 0:
            res = "10000000.0"

        mystr += str(int(sitenum[i])) + "\t" + str(geolat[i]) + "\t" + str(geolon[i]) + "\t0.5\t" + str(res) + "\n"

        f.write(mystr)

    for i, v in enumerate(connections):
        mystr = ""

        if v == 0:
            continue
        else:
            mystr += str(int(nodefrom[i])) + "\t" + str(int(nodeto[i])) + "\t" + str(lineresist[i]) + "\tnan\tnan\n"

        f.write(mystr)

    f.close()

    print "Exported to: ", filename


































