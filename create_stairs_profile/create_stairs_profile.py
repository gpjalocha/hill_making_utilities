import re
from numpy import arange
import sys
import os
input={}
keys = ["--refx=","--refy=","--start=","--end=","--step=","--h=","--offset=","--output="]
for i in range(1,len(sys.argv)):                                                                                                       
    for key in keys:                                                                                                                   
        if sys.argv[i].find(key) == 0:                                                                                        
            #print(f"The Given value is: {sys.argv[i][len(key):]}")
            if sys.argv[i][2:(len(key)-1)] in ['refx','refy','output']:
            	input[sys.argv[i][2:(len(key)-1)]]=str(sys.argv[i][len(key):])
            else:
                input[sys.argv[i][2:(len(key)-1)]]=float(sys.argv[i][len(key):])
            break

def is_input_valid(input):
    if(input['start']>input['end']):
        print("ERROR: end should have bigger value than start")
        sys.exit()
    if(input['step']<0):
        print("ERROR: step should be bigger than zero")
        sys.exit()
    if(input['offset']<0):
        print("ERROR: offset should be bigger than zero")
        sys.exit()
    if(input['offset']>input['step']):
        print("ERROR: offset should be smaller than the step")
        sys.exit()

def print_warnings(input):
    if(input['refx'] not in ['inrun','dhill']):
        print("WARNING: Using custom refx:\"%s\". Make sure you have this refx defined in your hill xml" % input['refx'])
    if(input['refy'] not in ['inrun-top','dhill-top']):
        print("WARNING: Using custom refy:\"%s\". Make sure you have this refy defined in your hill xml" % input['refy'])
    if(input['offset']>.05):
        print("WARNING: offset is quite big. It's ok if the stairs are supposed to be thin. But if not, consider using a smaller value")
    if(input['h']<0):
        print("WARNING: height of the steps is less than zero. It might be intended to put the stairs below the profile, but this might be wrong.")

is_input_valid(input)
print_warnings(input)

profile_str=     '<!--STAIRS PROFILE-->\n\n'
profile_str+=     '<profile id="%s-stairs" refx="%s">\n\t' % tuple([input['refx'],input['refx']])
profile_str+=    '<start x="%0.3f" y="%0.3f" refy="%s"/>\n\t' % tuple([input['start'],input['h'],input['refy']])
for a in arange(input['start'],input['end'],input['step']):
	profile_str+='<line x="%0.3f" y="%0.3f" refyx="%0.3f"  refy="%s"/>\n\t' % tuple([a+input['step']-input['offset'],input['h'],a,input['refy']])
	profile_str+='<line x="%0.3f" y="%0.3f" refy="%s"/>\n\t' % tuple([a+input['step'],input['h'],input['refy']])

profile_str+='\n</profile>'

pillar_str='<!--EXAMPLE STAIRS-->\n\n'
pillar_str+='<pillar refx="%s" refy="%s-stairs"\n\t' % tuple([input['refx'], input['refx']])
pillar_str+='x1="%0.3f" x2="%0.3f" ty=".05" lz="1" rz="-1" step="%0.3f" count="%i"\n\t' % tuple([input['start'],input['start']+input['step']-input['offset'],input['step'],round((input['end']-input['start'])/input['step'])])
pillar_str+='t="Textures\\grid.png" m="Materials\\material1.xml" c="0xcccccc"/>'

#print(profile_str)
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(os.path.join(__location__, input['output']))
f=open(os.path.join(__location__, input['output']) ,'w')
f.write(profile_str+'\n\n'+pillar_str)
f.close()
