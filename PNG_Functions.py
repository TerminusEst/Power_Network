# Program to make internal configuration of substation

import copy
################################################################################
# Load data
def substation_internals(substation):
    """ generate substation data from multiple input transformers"""
    trafo_name = substation[0][0]
    trafo_sym = substation[0][1]
    trafo_voltage = substation[0][2][:3]

    #print "SYM: ", trafo_sym

    trafo_number = len(substation)
    lat = float(substation[0][3])
    lon = float(substation[0][4])

    dist_incr = 0.00001
    transformers = []
    connections = []
    real_grounds = []
    meta_info = [trafo_name, trafo_sym, lat, lon, trafo_voltage]   # which transformers are real?

    if trafo_number == 1:   # if there is only 1 trafo
        if float(substation[0][5]) == 2:    # YY
            HVss = [0, lat + dist_incr, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            LVss = [1, lat - dist_incr, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]

            if float(substation[0][-1]) == 2: # if the trafo ground is open
                Gt = [2, lat, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            else:
                Gt = [2, lat, lon, 0.00001, float(substation[0][8]), trafo_voltage, trafo_sym]

            Gt_HVss = [0, 2, substation[0][6], nan, nan]
            Gt_LVss = [1, 2, substation[0][7], nan, nan]

            transformers.extend([HVss, LVss, Gt])
            connections.extend([Gt_HVss, Gt_LVss])
            real_grounds.append(2)
            hilo = [0, 1]

        if float(substation[0][5]) == 1:    # auto
            HVss = [0, lat + dist_incr, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            if float(substation[0][-1]) == 2: # if the trafo ground is open
                Gt = [1, lat, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            else:
                Gt = [1, lat, lon, 0.00001, float(substation[0][8]), trafo_voltage, trafo_sym]

            Gt_HVss = [0, 1, substation[0][6], nan, nan]

            transformers.extend([HVss, Gt])
            connections.extend([Gt_HVss])
            real_grounds.append(1)
            hilo = [0, 1]

        if float(substation[0][5]) == 3:    # reg
            transformers.append([0, lat, lon, substation[0][6], substation[0][8], trafo_voltage, trafo_sym])
            real_grounds.append(0)
            hilo = [0, 0]

        if float(substation[0][5]) == 4:    # TEE
            transformers.append([0, lat, lon, substation[0][6], substation[0][8], trafo_voltage, trafo_sym])
            real_grounds.append(0)
            hilo = [0, 0]

        meta_info.append(real_grounds)
        meta_info.append(hilo)
        return transformers, connections, meta_info

    HVss = [0, lat + 2*dist_incr, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]
    LVss = [1, lat - 2*dist_incr, lon, 0.00001, 100000.0, trafo_voltage, trafo_sym]
    transformers.extend([HVss, LVss])

    number = 2  # if there are multiple trafos
    for index, trafo in enumerate(substation):

        if float(trafo[5]) == 2:    # YY
            #print "YY"
            HVt = [number, lat + dist_incr, lon - index*dist_incr, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            HVt_HVss = [0, number, 0.00001, nan, nan]
            number += 1

            if float(trafo[-1]) == 2: # if the trafo ground is open
                Gt = [number, lat, lon - index*dist_incr, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            else:
                Gt = [number, lat, lon - index*dist_incr, 0.00001, float(trafo[8]), trafo_voltage, trafo_sym]
            real_grounds.append(number)
            Gt_HVt = [number-1, number, float(trafo[6]), nan, nan]
            number += 1

            LVt = [number, lat - dist_incr, lon - index*dist_incr, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            LVt_Gt = [number-1, number, float(trafo[7]), nan, nan]
            LVt_LVss = [1, number, 0.00001, nan, nan]
            number += 1

            transformers.extend([HVt, Gt, LVt])
            connections.extend([HVt_HVss, Gt_HVt, LVt_Gt, LVt_LVss])

        if float(trafo[5]) == 1:    # autotransformer
            #print "AUTO"
            HVt = [number, lat + dist_incr, lon - index*dist_incr, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            HVt_HVss = [0, number, 0.00001, nan, nan]
            number += 1

            if float(trafo[-1]) == 2:   # if the trafo ground is open
                Gt = [number, lat, lon - index*dist_incr, 0.00001, 100000.0, trafo_voltage, trafo_sym]
            else:
                Gt = [number, lat, lon - index*dist_incr, 0.00001, float(trafo[8]), trafo_voltage, trafo_sym]

            real_grounds.append(number)
            Gt_HVt = [number-1, number, float(trafo[6]), nan, nan]
            Gt_LVt = [1, number, 0.00001, nan, nan]
            number += 1

            transformers.extend([HVt, Gt])
            connections.extend([HVt_HVss, Gt_HVt, Gt_LVt])

    meta_info.append(real_grounds)
    meta_info.append([0, 1])
    return transformers, connections, meta_info

def number_adder(x, y, z, count):
    """ Change the numbers of each substation so that there are no multiples"""

    max_nums = []
    aa, bb, cc = copy.deepcopy(x), copy.deepcopy(y), copy.deepcopy(z)

    for i, v in enumerate(aa):
        aa[i][0] += count
        max_nums.append(aa[i][0])

    for i, v in enumerate(bb):
        bb[i][0] += count
        bb[i][1] += count
        
    for i, v in enumerate(cc[5]):
        cc[5][i] += count

    for i, v in enumerate(cc[6]):
        cc[6][i] += count

    return aa, bb, cc, max(max_nums) + 1


def connections_adder(filename, volt, refined_connections2):
    """ generate connections output"""
    f = open(filename, 'r')
    data = f.readlines()
    f.close()

    raw = [x.split("\t") for x in data[1:-1]]
    refined = []
    for i in raw:
        namefrom, nameto, volt, circuit, res = i
        
        a = [namefrom, nameto, volt, circuit]
        if a not in refined:
            refined.append(a)

    for i in refined:
        total_res = 0

        for j in raw:
            if i == j[:-1]:
            
                namefrom, nameto, volt, circuit, res = j

                total_res += float(res)

        index1 = ss_meta.index(namefrom)
        volt1 = int(substation_meta[index1][4])
        hi1, lo1 = substation_meta[index1][6]
        
        index2 = ss_meta.index(nameto)
        volt2 = int(substation_meta[index2][4])
        hi2, lo2 = substation_meta[index2][6]

        if volt1 == volt2: # if the substations are same voltage - HI to HI
            connection = [hi1, hi2, total_res, nan, volt]
       
        if volt1 > volt2:  # LO to HI
            connection = [lo1, hi2, total_res, nan, volt]
            
        if volt2 > volt1:  # HI to LO
            connection = [hi1, lo2, total_res, nan, volt]

        refined_connections2.append(connection)
    
    return refined_connections2

def write_out(filename, refined_trafos, refined_connections, refined_connections2):
    """ write out trafos and connections"""

    f = open(filename, 'w')

    for i in refined_trafos:
        for j in i:
            f.write(str(j[0]) + "\t" + str(j[1]) + "\t" + str(j[2]) + "\t" + str(j[3]) + "\t" + str(j[4]) + "\t" + str(j[5]) + "\t" + str(j[6]) + "\n") 

    for i in refined_connections:
        for j in i:
            f.write(str(j[0]) + "\t" + str(j[1]) + "\t" + str(j[2]) + "\t" + str(j[3]) + "\t" + str(j[4]) + "\tnan\n") 

    for j in refined_connections2:
        f.write(str(j[0]) + "\t" + str(j[1]) + "\t" + str(j[2]) + "\t" + str(j[3]) + "\t" + str(j[4]) + "\tnan\n") 

    f.close()

    print "Successfully written output file!"

def write_substation_data(filename, substation_meta):
    """ write out substation meta data """

    f = open(filename, 'w')

    for i in substation_meta:
        mystr = ""

        for j in i[:-2]:
            mystr += str(j) + "\t"

        for j in i[-2]:
            mystr += str(j) + "\t"

        mystr += "\n"

        f.write(mystr)

    f.close()
   
    print "Successfully written substation meta file!"

def write_connections_data(filename, refined_connections_twixt_stations):
    """ write out connections meta data """
    f2 = open(filename2, 'w')

    temp_connections = []

    for i in refined_connections_twixt_stations:
        x, y = i[0], i[1]

        if ([x, y] in temp_connections) or ([y, x] in temp_connections):
            continue
        else:
            temp_connections.append([x, y])

    for i in temp_connections:
        x, y = i[0], i[1]


        for j in substation_meta:
            if x in j[-1]:
                latfrom = j[2]
                lonfrom = j[3]
                voltfrom = j[4]
                break

        for j in substation_meta:
            if y in j[-1]:
                latto = j[2]
                lonto = j[3]
                voltto = j[4]
                break

        v = min(voltfrom, voltto)

        mystr = str(v) + "\t" + str(latfrom) + "\t" + str(lonfrom) + "\t" + str(latto) + "\t" + str(lonto) + "\n"
        f2.write(mystr)

    f2.close()
    print "Successfully written connections meta file!"
