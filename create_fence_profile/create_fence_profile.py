import re
from numpy import arange
import sys
from math import sin,pi


input_={}
keys = ["--refx=","--refy=","--start=","--end=","--step=","--h=","--drop=","--breaks=","--output_xml="]
for i in range(1,len(sys.argv)):                                                                                                  
    for key in keys:                                                                                                                   
        if sys.argv[i].find(key) == 0:                                        
            if sys.argv[i][2:(len(key)-1)] in ['refx','refy','output_xml']:
                input_[sys.argv[i][2:(len(key)-1)]]=str(sys.argv[i][len(key):])
            else:
                input_[sys.argv[i][2:(len(key)-1)]]=float(sys.argv[i][len(key):])
            break

if "refx" not in input_.keys():
	input_['refx']="dhill"


if "refy" not in input_.keys():
	refy=""
else:
	refy=" refy=\""+input_['refy']+"\" "

start=input_['start']
end=input_['end']
step=input_['step']
h=input_['h']
drop=input_['drop']
breaks=input_['breaks']




step_=(step/breaks)

lines_count=int((end-start)/(step/breaks))

print("WARNING - script will output file of size %i lines. Continue?[Y/N]" % lines_count)
choice = input().lower()
if choice in ['yes','y']:
	print('executing...')
elif choice in ['n','no']:
   exit()
else:
   sys.stdout.write("Please respond with 'y' or 'n'")

profile_str=     '<profile id="dhill-fence" refx="%s">\n\t' % input_['refx']
profile_str+=    '<start x="%0.2f" y="%0.2f" %s/>\n\t' % tuple([start,h,refy])

for a in arange(start+step_,end,step_):
	profile_str+='<line x="%0.2f" y="%0.2f" %s/>\n\t' % tuple([a,h-abs(drop*sin((a-start)/step*pi)),refy])

profile_str+='</profile>'

profile_str+='\n\n<railing refx="%s" refy="dhill-fence" w=".05" h=".05" x1="%0.2f" x2="%0.2f" t="Textures\\metal.png" m="Materials\\material1.xml" c="0xff0000"/>' % tuple([input_['refx'],start,end])
#print(profile_str)

f=open(input_['output_xml'],'w')
f.write(profile_str)
f.close()