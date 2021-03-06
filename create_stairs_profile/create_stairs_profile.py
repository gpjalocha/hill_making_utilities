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

profile_str=     '<!--STAIRS PROFILE-->\n\n'
profile_str+=     '<profile id="%s-stairs" refx="%s">\n\t' % tuple([input['refx'],input['refx']])
profile_str+=    '<start x="%0.2f" y="%0.2f" refy="%s"/>\n\t' % tuple([input['start'],input['h'],input['refy']])
for a in arange(input['start'],input['end'],input['step']):
	profile_str+='<line x="%0.2f" y="%0.2f" refyx="%0.2f"  refy="%s"/>\n\t' % tuple([a+input['step']-input['offset'],input['h'],a,input['refy']])
	profile_str+='<line x="%0.2f" y="%0.2f" refy="%s"/>\n\t' % tuple([a+input['step'],input['h'],input['refy']])

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