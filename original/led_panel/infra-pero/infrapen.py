
wi, sp = None, None

"""
--- How to use ---

import infrapen
infrapen.init(svetelny_panel, wimote)


x, y = infrapen.get_coords()
# (x, y) are transformed coordinates

"""




class Pohled:
    """Used to map pixels in a non-rectangular quad to a rectangular one"""
    srcmatrix = [0.0,0.0,
    1.0,0.0,
    0.0,1.0,
    1.0,1.0]
    dstmatrix = [0.0,0.0,
    1.0,0.0,
    0.0,1.0,
    1.0,1.0]
    dstdots = [(0.0,0.0),(1.0,0.0),(0.0,1.0),(1.0,1.0)]
    srcdots = [(0.0,0.0),(1.0,0.0),(0.0,1.0),(1.0,1.0)]
    
    def __init__(self):
        self.computeWarpMatrix()

    #konfigurace, rohy z pohledu kamery
    def setsrc(self,dot1,dot2,dot3,dot4):
        
        self.srcdots = [(float(dot[0]),float(dot[1])) for dot in [dot1,dot2,dot3,dot4]]
        
        self.computeWarpMatrix()

    #rozmery panelu
    # (0,0), (15,0), (0, 9), (15,9) 
    def setdst(self,dot1,dot2,dot3,dot4):
        self.dstdots = [dot1,dot2,dot3,dot4]
        self.computeWarpMatrix()
        
    def computeWarpMatrix(self):
        self.srcmatrix = self.computeQuadToSquare(self.srcdots)
        self.dstmatrix = self.computeSquareToQuad(self.dstdots)
        self.warpmatrix = self.multMats(self.srcmatrix,self.dstmatrix)
        
    def computeSquareToQuad(self,inputdots):
        x0,y0 = inputdots[0]
        x1,y1 = inputdots[1]
        x2,y2 = inputdots[2]
        x3,y3 = inputdots[3]
        dx1 = x1 - x2
        dy1 = y1 - y2
        dx2 = x3 - x2
        dy2 = y3 - y2
        sx = x0 - x1 + x2 - x3
        sy = y0 - y1 + y2 - y3
        g = (sx * dy2 - dx2 * sy) / (dx1 * dy2 - dx2 * dy1)
        h = (dx1 * sy - sx * dy1) / (dx1 * dy2 - dx2 * dy1)
        a = x1 - x0 + g * x1
        b = x3 - x0 + h * x3
        c = x0
        d = y1 - y0 + g * y1
        e = y3 - y0 + h * y3
        f = y0
        
        mat = [0.0]*16
            
        mat[ 0] = a
        mat[ 1] = d
        mat[ 2] = 0
        mat[ 3] = g
        mat[ 4] = b
        mat[ 5] = e
        mat[ 6] = 0
        mat[ 7] = h
        mat[ 8] = 0
        mat[ 9] = 0
        mat[10] = 1
        mat[11] = 0
        mat[12] = c
        mat[13] = f 
        mat[14] = 0
        mat[15] = 1
        return mat
        
    def computeQuadToSquare(self,inputdots):
        x0,y0 = inputdots[0]
        x1,y1 = inputdots[1]
        x2,y2 = inputdots[2]
        x3,y3 = inputdots[3]
        mat = self.computeSquareToQuad(inputdots)
        
        a = mat[ 0]
        d = mat[ 1]
        g = mat[ 3]
        b = mat[ 4]
        e = mat[ 5]
        h = mat[ 7]         
        c = mat[12]
        f = mat[13]
        
        A = e - f * h
        B = c * h - b
        C = b * f - c * e
        D = f * g - d
        E =     a - c * g
        F = c * d - a * f
        G = d * h - e * g
        H = b * g - a * h
        I = a * e - b * d
        idet = 1.0 / (a * A           + b * D           + c * G)
         
        mat[ 0] = A * idet
        mat[ 1] = D * idet
        mat[ 2] = 0
        mat[ 3] = G * idet
        
        mat[ 4] = B * idet
        mat[ 5] = E * idet
        mat[ 6] = 0
        mat[ 7] = H * idet
        
        mat[ 8] = 0       
        mat[ 9] = 0       
        mat[10] = 1
        mat[11] = 0       
        
        mat[12] = C * idet
        mat[13] = F * idet
        mat[14] = 0
        mat[15] = I * idet
        return mat
    
    def multMats(self,srcMat,dstMat):
        resMat = [0]*16
        for r in range(0,4):
            ri = r * 4
            for c in range(0,4):
                resMat[ri + c] = (srcMat[ri    ] * dstMat[c     ] +
                srcMat[ri + 1] * dstMat[c +  4] +
                srcMat[ri + 2] * dstMat[c +  8] +
                srcMat[ri + 3] * dstMat[c + 12])
        return resMat
            
    def warp(self, srcX, srcY):
        result = [0.0]*4
        mat = self.warpmatrix
        z=0.0
        result[0] = (srcX * mat[0] + srcY*mat[4] + z*mat[8] + 1*mat[12])
        result[1] = (srcX * mat[1] + srcY*mat[5] + z*mat[9] + 1*mat[13])
        result[2] = (srcX * mat[2] + srcY*mat[6] + z*mat[10] + 1*mat[14])
        result[3] = (srcX * mat[3] + srcY*mat[7] + z*mat[11] + 1*mat[15])        
        dstX = result[0]/result[3]
        dstY = result[1]/result[3]
        return dstX,dstY
        





def init(svetelny_panel, wimote):
    #Needs svetelny_panel module and wimote instance
    
    global wi, pohl, sp
    wi = wimote
    sp = svetelny_panel
    pohl = Pohled()

    
    BOARDX = 15
    BOARDY = 9
    
    #Set output dimensions of led panel
    pohl.setdst((0,0), (BOARDX-1,0), (0,BOARDY-1), (BOARDX-1, BOARDY-1))

    sp.panel_clear()


    #----Configure physical led panel dimensions----
    
    #Down-left
    sp.set_pixel_color(sp.matrix(0,0),"ffffff")	
    print "klikni vlevo dole"
    downleft = get_raw_cords()
    sp.panel_clear()
    print downleft
    waituntilreleased()
    

    #Down-right
    sp.set_pixel_color(sp.matrix(0,14),"ffffff")
    print "klikni vpravo dole"
    downright = get_raw_cords()
    sp.panel_clear()
    print downright
    waituntilreleased()
    

    #Up-left
    sp.set_pixel_color(sp.matrix(8,0),"ffffff")
    print "klikni vlevo nahore"
    upleft = get_raw_cords()
    sp.panel_clear()
    print upleft
    waituntilreleased()
    

    #Up-right
    sp.set_pixel_color(sp.matrix(8,14),"ffffff")
    print "klikni pravo nahore"
    upright = get_raw_cords()
    sp.panel_clear()
    print upright
    waituntilreleased()
	
    pohl.setsrc(upleft, upright, downleft, downright)
    print "konfigurace dokoncena"



def get_raw_cords():
    #Return non-transformed raw infrapen coordinates (x, y), or None if canceled
    
    if not wi:
        print "Not initialized!"
        return None

    cords = wi.state["ir_src"][0]
    
    while True:
        if cords:
            break
        buttons = wi.state["buttons"]
        if buttons & 4:     #Don't wait for infrapen
            print "Waiting for position was interrupted"
            return None

	cords = wi.state["ir_src"][0]

    return cords["pos"]

    
    

def get_cords():
    #Returns transformed infrapen coordinates (x, y), or None if canceled 
    
    if not wi or not sp:
        print "Not initialized!"

    
    cords = wi.state["ir_src"][0]
    
    while True:
        if cords:
            break
        
        buttons = wi.state["buttons"]
        if buttons & 4:     #Don't wait for infrapen, cancel 
            return None

	cords = wi.state["ir_src"][0]

    x, y = cords["pos"]


    #calculate coordinates transformations
    x, y = pohl.warp(x, y)
    x, y = int(x), int(y)

    

    return x, y
    




def waituntilreleased():
    while True:
        cord = wi.state["ir_src"][0]
        if cord == None:
            return
	    






