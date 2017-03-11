################################################################################
################################################################################
################################################################################

def substation_internals(substation, count):
    """ Generate internal substation configuration with nodes and internal 
        connections.

            Follows the conventions of:
            http://onlinelibrary.wiley.com/doi/10.1002/2016SW001499/full

            Parameters
            -----------
            substation = list of transformers for one substation
            count = the node count before this substation

            Returns
            -----------
            transformers = list of output data for each node:
              -> number, lat, lon, trans_resist, earth_resist, voltage, 
                 substation symbol, transformer code

            connections = list of output data for internal connections
              -> nodefrom, nodeto, resistance, nan, nan, voltage

            meta_info = list of meta data for the substation
              -> Substation name, substation symbol, lat, lon, voltage, ground 
                 nodes, HV and LV busbar nodes
            
            number = the node number after this substation
            -----------------------------------------------------------------

    """
    count += 1          # transformer count
    infsmall = 1e-10    # 0 resistance equivalent
    infbig = 1e10       # inf resistance equivalent
    dist_incr = 0.00001 # distance increment

    # Substation info from first trafo
    ss_name, ss_sym, tf_sym, ss_voltage = substation[0][:4]

    trafo_number = len(substation)  # number of transformers
    lat = float(substation[0][4])  # baditude
    lon = float(substation[0][5])  # longitude
    ground_res = float(substation[0][9])    # grounding resistance for substation

    transformers, connections, real_grounds = [], [], []
    meta_info = [ss_name, ss_sym, lat, lon, ss_voltage] 

    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    # some terminology:
    # HVss, LVss = HV and LV substation buses
    # Gt = Grounded transformer    
    # Gt_HVss = Connection between Gt and HVss

    # In the case that there is a single transformer at the substation:
    if trafo_number == 1:
        res1 = float(substation[0][7])     # high winding res
        res2 = float(substation[0][8])     # low winding res
        tf_type = substation[0][6]
        #-----------------------------------------------------------------------

        if tf_type == "YY":    # Single YY transformer
            HVss = [count, lat + dist_incr, lon, infsmall, infbig, ss_voltage, ss_name, "--"]
            LVss = [count+1, lat - dist_incr, lon, infsmall, infbig, ss_voltage, ss_name, "--"]
            Gt = [count+2, lat, lon, infsmall, ground_res, ss_voltage, ss_name, tf_sym]

            Gt_HVss = [count, count+2, res1, nan, nan, nan, ss_voltage]
            Gt_LVss = [count+1, count+2, res2, nan, nan, nan, ss_voltage]

            transformers.extend([HVss, LVss, Gt])
            connections.extend([Gt_HVss, Gt_LVss])
            real_grounds.append(count+2)
            hilo = [count, count+1]
            number = count+2

        #-----------------------------------------------------------------------

        if tf_type == "A":    # auto
            HVss = [count, lat + dist_incr, lon, infsmall, infbig, ss_voltage, ss_name, "--"]
            Gt = [count+1, lat, lon, infsmall, ground_res + res2, ss_voltage, ss_name, tf_sym]

            Gt_HVss = [count, count+1, res1, nan, nan, nan, ss_voltage]

            transformers.extend([HVss, Gt])
            connections.extend([Gt_HVss])
            real_grounds.append(count+1)
            hilo = [count, count+1]
            number = count+1

        #-----------------------------------------------------------------------

        if tf_type == "G":    # "end" or "grounded" trafo
            transformers.append([count, lat, lon, res1, ground_res, ss_voltage, ss_name, tf_sym])
            real_grounds.append(count)
            hilo = [count, count]
            number = count

        #-----------------------------------------------------------------------

        if tf_type == "T":    # TEE
            transformers.append([count, lat, lon, infsmall, ground_res, ss_voltage, ss_name, tf_sym])
            real_grounds.append(count)
            hilo = [count, count]
            number = count

        meta_info.append(real_grounds)
        meta_info.append(hilo)
        return transformers, connections, meta_info, count

    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    # If there are multiple trafos, need HV and LV buses
    HVss = [count, lat + 2*dist_incr, lon - 0.5*dist_incr, infsmall, infbig, ss_voltage, ss_name, "--"]
    LVss = [count+1, lat - 2*dist_incr, lon + 0.5*dist_incr, infsmall, infbig, ss_voltage, ss_name, "--"]
    transformers.extend([HVss, LVss])

    number = int(count)+2  # we start with number 2: 0 = HVss, 1 = LVss...
    for index, trafo in enumerate(substation):
        res1 = float(trafo[7])     # high winding res
        res2 = float(trafo[8])     # low winding res
        tf_type = trafo[6]
        tf_sym = trafo[2]

        #-----------------------------------------------------------------------

        if tf_type == "YY":    # YY
            HVt = [number, lat + dist_incr, lon - index*dist_incr, infsmall, infbig, ss_voltage, ss_name, "--"]
            HVt_HVss = [count, number, infsmall, nan, nan, nan, ss_voltage]
            number += 1

            Gt = [number, lat, lon - index*dist_incr, infsmall, ground_res * trafo_number, ss_voltage, ss_name, tf_sym]
            real_grounds.append(number)
            Gt_HVt = [number-1, number, res1, nan, nan, nan, ss_voltage]
            number += 1

            LVt = [number, lat - dist_incr, lon - index*dist_incr, infsmall, infbig, ss_voltage, ss_name, "--"]
            LVt_Gt = [number-1, number, res2, nan, nan, nan, ss_voltage]
            LVt_LVss = [count+1, number, infsmall, nan, nan, nan, ss_voltage]
            number += 1

            transformers.extend([HVt, Gt, LVt])
            connections.extend([HVt_HVss, Gt_HVt, LVt_Gt, LVt_LVss])

        #-----------------------------------------------------------------------

        if tf_type == "A":    # autotransformer
            HVt = [number, lat + dist_incr, lon - index*dist_incr, infsmall, infbig, ss_voltage, ss_name, "--"]
            HVt_HVss = [count, number, infsmall, nan, nan, nan, ss_voltage]
            number += 1

            Gt = [number, lat, lon - index*dist_incr, res2, (ground_res * trafo_number), 
                    ss_voltage, ss_name, tf_sym]

            Gt_HVt = [number-1, number, res1, nan, nan, nan, ss_voltage]
            Gt_LVss = [count+1, number, infsmall, nan, nan, nan, ss_voltage]
            real_grounds.append(number)
            number += 1

            transformers.extend([HVt, Gt])
            connections.extend([HVt_HVss, Gt_HVt, Gt_LVss])

        #-----------------------------------------------------------------------

        if tf_type == "G":   # "end" or "grounded" trafo
            Gt = [number, lat, lon - index*dist_incr, res1, ground_res * trafo_number, ss_voltage, ss_name, tf_sym]
            print res1, ground_res * trafo_number, ss_voltage, ss_name, tf_sym
            real_grounds.append(number)
            Gt_HVss = [number, count, infsmall, nan, nan, nan, ss_voltage]
            number += 1

            transformers.extend([Gt])
            connections.extend([Gt_HVss])#, Gt_tGt])

    meta_info.append(real_grounds)
    meta_info.append([count, count+1])

    return transformers, connections, meta_info, number-1

################################################################################
################################################################################
################################################################################




def connections_adder3(filename, substation_meta):
    
    # read in the file
    #-----------------------------------------------------------------------
    f = open(filename, 'r')
    data = f.readlines()
    f.close()
    raw = [x.split("\t") for x in data[1:-1]]

    #-----------------------------------------------------------------------
    # work out resistances (incl. parallel lines)

    line_ids, resistances = [], []  # from, to, volt
    for i in raw:
        namefrom, nameto, volt, circuit, res = i
        
        idd = [namefrom, nameto, volt]

        if idd not in line_ids:
            line_ids.append(idd)
            resistances.append([float(res)])
        else:
            resistances[line_ids.index(idd)].append(float(res))

    for index, value in enumerate(resistances):
        if len(value) == 1:
            line_ids[index].append(value[0])
        else:
            line_ids[index].append(resistance_parallel(value))

    #-----------------------------------------------------------------------
    # now to work out the connections between nodes
    
    ss_meta = [x[0] for x in substation_meta]
    output = []

    for j in line_ids:
        namefrom, nameto, volt, res = j

        index1 = ss_meta.index(namefrom)
        volt1 = int(substation_meta[index1][4])
        hi1, lo1 = substation_meta[index1][6]
        
        index2 = ss_meta.index(nameto)
        volt2 = int(substation_meta[index2][4])
        hi2, lo2 = substation_meta[index2][6]

        line_volt = int(volt)   # voltage of power line

        if volt1 == volt2: # if the substations are same voltage
            if line_volt < volt1:    # if voltage of line is < voltage of substation - LO to LO
                thingy = sorted([lo1, lo2])

            else:               # if voltage of line == voltage of substation - HI to HI
                thingy = sorted([hi1, hi2])

        elif volt1 > volt2:  # LO to HI
            thingy = sorted([lo1, hi2])

        else:  # HI to LO
            thingy = sorted([hi1, lo2])

        connection = [thingy[0], thingy[1], res, nan, nan, nan, nan, line_volt]

        output.append(connection)

        print connection[-1]
    return output


filename = "/home/blake/Drive/Network_Analysis/Horton/Input/total_connect.csv"








def connections_adder2(filename):
    """Create connections between substations

            Parameters
            -----------
            filename = name of file with connections

            Returns
            -----------
            output_list = list of connections in form
              -> node_from, node_to, resistance, nan, nan, nan

            -----------------------------------------------------------------
    """

    individual_connections = []

    # read in the file
    f = open(filename, 'r')
    data = f.readlines()
    f.close()

    raw = [x.split("\t") for x in data[1:-1]]
    refined = []

    # get rid of duplicates
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

        line_volt = int(volt)   # voltage of power line

        if volt1 == volt2: # if the substations are same voltage
            if line_volt < volt1:    # if voltage of line is < voltage of substation - LO to LO
                thingy = sorted([lo1, lo2])
                connection = [thingy[0], thingy[1], round(total_res, 5), nan, line_volt, circuit]#, namefrom, nameto]
            else:               # if voltage of line == voltage of substation - HI to HI
                thingy = sorted([hi1, hi2])
                connection = [thingy[0], thingy[1], round(total_res, 5), nan, line_volt, circuit]#, namefrom, nameto]
       
        elif volt1 > volt2:  # LO to HI
            thingy = sorted([lo1, hi2])
            connection = [thingy[0], thingy[1], round(total_res, 5), nan, line_volt, circuit]#, namefrom, nameto]
            
        else:  # HI to LO
            thingy = sorted([hi1, lo2])
            connection = [thingy[0], thingy[1], round(total_res, 5), nan, line_volt, circuit]#, namefrom, nameto]

        # ignore duplicate lines (same connections + same circuit = duplicate)
        switch = False
        for j in individual_connections:
            if [j[0], j[1], j[5]] == [connection[0], connection[1], connection[5]]:
                switch = True
                break
        if switch == False:
            individual_connections.append(connection)
                    

    # parallel lines:
    output_list, temp = [], []
    mycopy = copy.deepcopy(individual_connections)

    while len(mycopy) > 0:
        subject = mycopy.pop(0)
        temp = [subject]

        for index, value in enumerate(mycopy):
            if [subject[0], subject[1]] == [value[0], value[1]]:
                temp.append(value)
                zzz = mycopy.pop(index)
        
        if len(temp) > 1:
            resistances = [x[2] for x in temp]
            res = resistance_parallel(resistances)
            
            xx = temp[0]
            xxx = [xx[0], xx[1], res, xx[3], xx[4], xx[5]]

            output_list.append(xxx)#, len(temp)])

        else:
            output_list.append(temp[0])#, len(temp)])


    return output_list





































def write_out(filename, refined_trafos, refined_connections, refined_connections2):
    """ write out trafos and connections"""

    f = open(filename, 'w')

    for i in refined_trafos:
        for j in i:
            f.write(str(j[0]) + "\t" + str(j[1]) + "\t" + str(j[2]) + "\t" + str(j[3]) + "\t" + str(j[4]) + "\t" + str(j[5]) + "\t" + str(j[6]) + "\t" + str(j[-1]) + "\n") 

    for i in refined_connections:
        for j in i:
            f.write(str(j[0]) + "\t" + str(j[1]) + "\t" + str(j[2]) + "\tnan\tnan\tnan\t" + str(j[-1]) + "\n")

    for j in refined_connections2:
        f.write(str(j[0]) + "\t" + str(j[1]) + "\t" + str(j[2]) + "\tnan\tnan\tnan\t" + str(j[-1]) + "\n")

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

def write_connections_data(filename2, refined_connections_twixt_stations):
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

def resistance_parallel(resistances):
    res = 0
    for i in resistances:
        res += 1./i

    return 1./res


