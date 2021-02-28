#!/bin/python

import numpy as np
from re import findall,match,search
import sys

#read input

input={}
keys = ["--model_tag=","--input_obj=","--output_xml=","--inv_faces=","--scale_uv="]
for i in range(1,len(sys.argv)):                                                                                                       
    for key in keys:                                                                                                                   
        if sys.argv[i].find(key) == 0:                                        
            if sys.argv[i][2:(len(key)-1)] in ['model_tag','input_obj','output_xml']:
                input[sys.argv[i][2:(len(key)-1)]]=str(sys.argv[i][len(key):])
            else:
                input[sys.argv[i][2:(len(key)-1)]]=float(sys.argv[i][len(key):])
            break


def read_obj(path="./models/windmill.obj"):
    f=open(path,'r')
    lines=f.readlines()
    v=[]
    vt=[]
    f={}
    iv=1
    for line in lines:
        if(bool(match("^v ",line))):
                v=v+[[float(x) for x in findall('-?[\d.]+',line)]]
        if(bool(match("^vt ",line))):
                vt=vt+[[float(x) for x in findall('-?[\d.]+',line)]]
        if(bool(match("usemtl",line))):
                material=search("usemtl (.+)",line).group(1)
                f[material]={}
                f[material]['v']=[]
                f[material]['uv']=[]
        if(bool(match("^f ",line))):
                f[material]['v']+=[[int(x) for x in findall(' ([\d.]+)/',line)]]
                f[material]['uv']+=[[int(x) for x in findall(' [\d.]+?/([\d.]+)',line)]]
    return v,f,vt

def blend(color, alpha, base=[255,255,255]):
    out = [int(round((alpha * color[i]) + ((1 - alpha) * base[i]))) for i in range(3)]
    return out

def to_hex(color):
    return ''.join(["%02x" % e for e in color])

def read_mtl(path="./models/windmill.mtl"):
    f=open(path,'r')
    lines=f.readlines()
    v=[]
    f={}
    iv=1
    for line in lines:
        if(bool(match("newmtl",line))):
                material=search("newmtl (.+)",line).group(1)
                f[material]=''
        if(bool(match("^Kd ",line))):
                f[material]+=to_hex(blend([float(x)*255 for x in findall('([\d.]+)',line)],1))
    return f

def extract_texture(input_str):
    if(bool(match(r".*Textures\\.+?\.(png|jpg)",input_str))):
        parsed_texture=match(r".*(Textures\\.+?\.(png|jpg))",input_str).group(1)
        return(parsed_texture)
    else:
        return("Textures\\metal.png")

def extract_material(input_str):
    if(bool(match(r".*Materials\\.+?\.xml",input_str))):
        parsed_material=match(r".*?(Materials\\.+?\.xml)",input_str).group(1)
        return(parsed_material)
    else:
        return("Materials\\material1.xml")

def convert_3d(name,v,f,vt,mtl,scale_uv,invert_faces,model_tag):
    if model_tag=="3dmodel":
        prefix="3d"
    else:
        prefix=""
    command = ('<%smodel id="'+name+'">\n\t') % prefix
    for batch in f:
            verts_str=[]
            faces=[]
            verts_all=[]
            color=mtl[batch]
            material=extract_material(batch)
            texture=extract_texture(batch)
            command+="<batch id=\""+batch+'" texture1="'+texture+'" zbias="3" material="'+material+'" fvf="322" order="0">\n\t\t'
            kl=0
            allVertsUv=[]
            print("processing texture batch name: %s\nmaterial: %s\ntexture: %s\ncolor=%s\n" %tuple([batch,material,texture,color]))
            for face_v,face_uv in zip(f[batch]['v'],f[batch]['uv']):
                allVertsUv+=[str(a-1)+'_'+str(b-1) for a,b in zip(face_v,face_uv)]
            allVertsUv=list(set(allVertsUv))
            allVertsTableId=dict(zip(allVertsUv,range(len(allVertsUv))))
            for face_v,face_uv in zip(f[batch]['v'],f[batch]['uv']):
                    if len(face_v)==3:
                            vertsInd=[i-1 for i in face_v]
                            verts=[v[int(i)-1] for i in face_v]
                            uvInd=[i-1 for i in face_uv]
                            uv=[vt[int(i)-1] for i in face_uv]
                            for Ind,vertex,UVind,UV in zip(vertsInd,verts,uvInd,uv):
                                    kl+=1
                                    vertVal=str(Ind)+'_'+str(UVind)
                                    INDEX=allVertsTableId[vertVal]
                                    vert_vals=[float(vr) for vr in vertex]
                                    vert_vals[2]=-vert_vals[2]
                                    if (Ind,UVind) not in verts_all:
                                            verts_str+=[('<vertex id="%i" x="%0.4f" y="%0.4f" z="%0.4f" u1="%0.4f" v1="%0.4f" diffuse="0x%s"/>\n\t\t') % tuple([INDEX]+vert_vals+[UV[0]/scale_uv,-UV[1]/scale_uv]+[color])]
                                            verts_all+=[tuple([Ind,UVind])]
                            if(invert_faces == 0):
                                faces+=['\n\t\t<face v2="%i" v1="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)] for a,b in zip(vertsInd,uvInd)])]
                            else:
                                faces+=['\n\t\t<face v1="%i" v2="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)] for a,b in zip(vertsInd,uvInd)])]
                    else:
                        print("Detected face with more than 3 vertices:\n")
                        print(face_v)
                        print('\n\n Triangulate your model!')
                        quit()
            verts_numbs=[int(findall(' id="(.+?)"',j)[0]) for j in verts_str]
            zipped_verts=list(set(zip(verts_numbs,verts_str)))
            sorted_verts=sorted(zipped_verts)
            verts_str=[x for _,x in sorted_verts]
            faces_numbs=[int(findall(' v1="(.+?)"',j)[0]) for j in faces]
            zipped_faces=zip(faces_numbs,faces)
            sorted_faces=sorted(zipped_faces)
            faces=[x for _,x in sorted_faces]
            command+=''.join(verts_str)+'\n\n'+''.join(faces)
            command+='\n\t</batch>\n\t'
    command+=("\n</%smodel>\n\n<%smodel-instance id=\""+name+"\"/>") % tuple([prefix,prefix])
    return(command)

def save_to_file(io,path):
    file=open(path+'.xml','w')
    file.write(io)
    file.close()



    # execute only if run as a script
model=input['input_obj']
output=input['output_xml']
scale_uv=input['scale_uv']
invert_faces=input['inv_faces']
model_tag=input['model_tag']

v,f,vt=read_obj(model+'.obj')
mtl=read_mtl(model+'.mtl')
res=convert_3d(model,v,f,vt,mtl,scale_uv,invert_faces,model_tag)

save_to_file(res,output)
print("Conversion finished, output file:\n"+output+".xml")
