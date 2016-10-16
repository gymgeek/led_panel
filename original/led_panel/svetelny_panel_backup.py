"""svetelny panel s led paskem 
seriova komunikace s arduinem
atp.

light (luminary) panel with led strip
serial communication with arduino

funkcni vzorek
15 x 9 px

FUNCTION SAMPLE
15 x 9 px
- first diod at left bottom corner
- odd rows (from bottom) from left to right
- even rows from right to left
- matrix numbering:
top line - 0 index
left column - 0 index

"""

from bbio import * 
import time
import math

def set_pixel_color(num_of_pixel, color="", timeout=0.1): 
    if Serial2.baud ==0: 
        setup()
    command = "x{} {}\n".format(num_of_pixel, color)
    Serial2.write(command)
    itime = time.time()
    icommand = ""
    while(icommand.count(command)==0 and time.time() < itime + 0.1):
        ichar = Serial2.read()
        if ichar != "\r": 
            icommand += ichar
    if icommand.count(command) > 0: 
        return True
    else: 
        return False

def panel_show(): 
    if Serial2.baud ==0: 
        setup()
    command = "show\n"
    Serial2.write(command)
    itime = time.time()
    icommand = ""
    while(icommand.count(command)==0 and time.time() < itime + 0.1):
        ichar = Serial2.read()
        if ichar != "\r": 
            icommand += ichar
    if icommand.count(command) > 0: 
        return True
    else: 
        return False

def set_panel_color(color="", timeout=0.1): 
    if Serial2.baud ==0: 
        setup()
    command = "color {}\n".format(color)
    Serial2.write(command)
    itime = time.time()
    icommand = ""
    while(icommand.count(command)==0 and time.time() < itime + 0.1):
        ichar = Serial2.read()
        if ichar != "\r": 
            icommand += ichar
    if icommand.count(command) > 0: 
        return True
    else: 
        return False

def set_panel_memory(rgb_string, from_pixel=0): 
    if Serial2.baud ==0: 
        setup()
    memblock_len = 120
    count_of_pixels = memblock_len / 3
    number_of_memblocks = len(rgb_string) / memblock_len 
    if len(rgb_string) % memblock_len != 0: 
        number_of_memblocks += 1

    for memblock in range(number_of_memblocks):
        data = rgb_string[memblock * memblock_len:(memblock + 1) * memblock_len]
        command = "m{} {}".format(from_pixel + memblock * count_of_pixels, \
                len(data) / 3)
        #print command
        #m = ser.write(prikaz + "\n")
        #while ser.inWaiting() < len(prikaz) + 2:
        #    pass
        #j = ser.read(len(prikaz) + 2)
        Serial2.write(command + "\n")
        itime = time.time()
        icommand = ""
        while(icommand.count(command)==0 and time.time() < itime + 0.1):
            icommand += Serial2.read()
        #print icommand
        #print len(data)
        #print data
        #m = ser.write(data)
        Serial2.write(data)
        # answer is OK or KO
        #while ser.inWaiting() < 2 + 2:
        #    pass
        #j = ser.read(2 + 2)
        itime = time.time()
        icommand = ""
        while(icommand.count("OK")==0 and icommand.count("KO")==0 and time.time() < itime + 0.1):
            icommand += Serial2.read()




#-------------Added 2/3/2015------------------------
#---------------------------------------------------
#---------------------------------------------------
            


def set_panel_memory_from_matrix(matrix):
    from_pixel = 0

    #Convert matrix to continuos rgb_string
    rgb_string = from_matrix_to_rgb_string(matrix)
    set_panel_memory(rgb_string)
    panel_show()





def from_matrix_to_rgb_string(matrix):
    rgb_string=""
    #Led pasek jde smeren od sdola nahoru,
    for r in range(len(matrix))[::-1]:
        row_from_bottom = len(matrix)-1-r
        for c in range(len(matrix[0]))[::(-1 if row_from_bottom%2==1 else 1)]:
            #print "R:{}, C:{}".format(str(r), str(c))
            rgb_string += convert_to_binary(matrix[r][c])



    return rgb_string




def get_led_number(row, column):
    #designed for 15x9
    #[0,0] is top left

    if row%2:
        return (8-row+1)*15 - 1 - column
    else:
        return (8-row)*15 + column



def show_matrix(matrix):
    for r, row in enumerate(matrix):
        for c, col in enumerate(row):
            if col:
                set_pixel_color_matrix(r, c, convert_to_binary(col))


def set_pixel_color_matrix(row, column, color="", timeout=0.1):
    num_of_pixel = get_led_number(row, column)
    if Serial2.baud == 0:
        setup()
    command = "x{} {}\n".format(num_of_pixel, color)
    Serial2.write(command)
    itime = time.time()
    icommand = ""
    while(icommand.count(command)==0 and time.time() < itime + 0.1):
        ichar = Serial2.read()
        if ichar != "\r":
            icommand += ichar
    if icommand.count(command) > 0:
        return True
    else:
        return False



def convert_to_binary(str_rgb):
    result = ""

    for part in (str_rgb[:2], str_rgb[2:4], str_rgb[4:]):
        result += chr(int(part, 16))

    

    return result


#---------------------------------------------
#---------------------------------------------
#-------------Added 2/3/2015------------------

            









    

def setup(speed=115200):
  # Start Serial2 at speed baud:
  Serial2.begin(speed)

def nacti():
    data = ""
    while Serial2.available():
        data += Serial2.read()
    return data

def rotate(l,n):
    """ list rotation """
    return l[n:] + l[:n]

def test(count=12):
    #ser = serial.Serial('/dev/ttyACM3', 115200, timeout=0.1)
    setup()
    #time.sleep(1)
    #print ser.readlines()
    for b in range(1,count + 1):
        for i in range(135):
            command = "x" + str(i) + " " + hex((b % 4 == 1) * 255 + (b % 4 == 2) * 256 * 255 + (b % 4 == 3) * 256 * 256 * 255)[2:]
            #x = ser.write(prikaz + "\n")
            Serial2.write(command + "\n")
            itime = time.time()
            icommand = ""
            while(icommand.count(command)==0 and time.time() < itime + 0.1):
                icommand += Serial2.read()
            #print icommand
    return #ser

def test1(count=1000):
    """writing into video memory"""
    
    #ser = serial.Serial('/dev/ttyACM3', 115200, timeout=0.1)
    # time.sleep(1)
    r = 0.5
    g = 0
    b = 0
    #j = ser.readlines()
    j = nacti()
    data_pattern = '\x00\x00\x00\x10\x10\x10   @@@'
    count_of_pixels = 40
    begin_time = time.time()
    for change_number in range(count):
        for memblock in range(4):
            command = "m{} {}".format(memblock * count_of_pixels, count_of_pixels)
            #print command
            #m = ser.write(prikaz + "\n")
            #while ser.inWaiting() < len(prikaz) + 2:
            #    pass
            #j = ser.read(len(prikaz) + 2)
            Serial2.write(command + "\n")
            itime = time.time()
            icommand = ""
            while(icommand.count(command)==0 and time.time() < itime + 0.1):
                icommand += Serial2.read()
            #print icommand

            # apply rgb modifying
            r = max(math.sin(change_number/50.), 0)
            g = max(math.sin(change_number/50. + math.pi * 2 / 3), 0)
            b = max(math.sin(change_number/50. + math.pi * 4 / 3), 0)
            modif_data_pattern = ""
            for i in range(len(data_pattern)):
                modif_data_pattern += chr(int(ord(data_pattern[i]) * \
                    (r * (i % 3 == 0) + g * (i % 3 == 1) + b * (i % 3 == 2))))
            # data writing
            data = rotate(modif_data_pattern, (change_number * 3) % len(data_pattern)) \
                   * (count_of_pixels * 3 / len(data_pattern))

            print data
            
            #print len(data)
            #print data
            #m = ser.write(data)
            Serial2.write(data)
            # answer is OK or KO
            #while ser.inWaiting() < 2 + 2:
            #    pass
            #j = ser.read(2 + 2)
            itime = time.time()
            icommand = ""
            while(icommand.count("OK")==0 and icommand.count("KO")==0 and time.time() < itime + 0.1):
                icommand += Serial2.read()
            #print icommand

        command = "show"
        Serial2.write(command + "\n")
        itime = time.time()
        icommand = ""
        while(icommand.count(command)==0 and time.time() < itime + 0.1):
            icommand += Serial2.read()
        #print icommand
 
    end_time = time.time()
    print "{} changes".format(count)
    print "total time {} seconds".format(end_time - begin_time)
    print "one change period {} seconds".format((end_time - begin_time) / count)
        
    return #ser


