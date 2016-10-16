import cwiid

def winit(address=None, num_of_tries=3):
    print "press 1 and 2 button on a wiimote!!!"
    wm = None
    ok = False
    iinit = 0
    while not ok and iinit < num_of_tries:
        # print iinit  
        try:
            if address is None:
                wm = cwiid.Wiimote()
            else:
                wm = cwiid.Wiimote(address)
            wm.rumble = 1
            time.sleep(0.2)
            wm.rumble = 0
            wm.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
            ok = True
        except:
            ok = False
            iinit += 1
    ok = False
    return wm


def test_wii():
    """simple test of wiimote communication"""
    w = winit()
    print "konec inicializace"
    print "end of initialisation"
    time.sleep(1)
    try:
	 for i in range(16):
	      w.led = i
	      time.sleep(0.5)
	      time.sleep(1)
	      w.led = 0
    except:
        print "nebyla navazana komunikace s ovladacem..."
    return w

