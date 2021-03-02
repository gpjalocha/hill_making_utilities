import re
from numpy import arange
from math import sin,radians,cos
import sys
import os
input={}
keys = ["--refx=","--refy=","--refz=","--x=","--y=","--z=","--radius=","--segments=","--rings=","--color=","--output="]


def return_r(alpha,radius): return(radius*sin(radians(alpha)))
def return_y(alpha,radius,y): return(y+radius*cos(radians(alpha)))


for i in range(1,len(sys.argv)):                                                                                                       
    for key in keys:                                                                                                                   
        if sys.argv[i].find(key) == 0:                                                                                        
            #print(f"The Given value is: {sys.argv[i][len(key):]}")
            if sys.argv[i][2:(len(key)-1)] in ['refx','refy','refz','color','output']:
            	input[sys.argv[i][2:(len(key)-1)]]=str(sys.argv[i][len(key):])
            else:
                input[sys.argv[i][2:(len(key)-1)]]=float(sys.argv[i][len(key):])
            break

if "refx" not in input.keys():
	input['refx']="dhill"


if "refy" not in input.keys():
	refy=""
else:
	refy=" refy=\""+input['refy']+"\" "

if "refz" not in input.keys():
	refz=""
else:
	refz=" refz=\""+input['refz']+"\" "

refx=" refx=\""+input['refx']+"\" "

beam_str="<beam %s %s %s" % tuple([refx,refy,refz])
beam_str+="""
    x="%0.3f" """ % input['x']
beam_str+="""
    z="%0.3f" """ % input['z']
beam_str+="""
    edges="%i" """ % input['segments']
beam_str+="""
    y1="%0.3f" y2="%0.3f"
    r1="%0.3f" r2="%0.3f"
    t="Textures\\metal.png" m="Materials\\light.xml" c="0x%s"/>\n"""


step=180.0/float(input['rings'])
beams_all="<!-- UV SPHERE-->\n\n"
for alpha in arange(0,180,step):
    beams_all+=beam_str % tuple([
    	return_y(alpha,input['radius'],input['y']),
    	return_y(alpha+step,input['radius'],input['y']),
    	return_r(alpha,input['radius']),
    	return_r(alpha+step,input['radius']),
    	input['color']])

f=open(input['output']+'.xml','w')
f.write(beams_all)
f.close()
print("Output written to "+input['output']+'.xml')
