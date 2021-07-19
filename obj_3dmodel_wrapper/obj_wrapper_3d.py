#!/bin/python

import numpy as np
from re import findall,match,search,sub
import sys

#read input

input={}
keys = ["--model_tag=","--input_obj=","--output_xml=","--inv_faces=","--scale_uv=","--scale=","--use_normals="]
for i in range(1,len(sys.argv)):                                                                                                  
    for key in keys:                                                                                                                   
        if sys.argv[i].find(key) == 0:                                        
            if sys.argv[i][2:(len(key)-1)] in ['model_tag','input_obj','output_xml','use_normals']:
                input[sys.argv[i][2:(len(key)-1)]]=str(sys.argv[i][len(key):])
            else:
                input[sys.argv[i][2:(len(key)-1)]]=float(sys.argv[i][len(key):])
            break


def read_obj(path="./models/windmill.obj", read_normals='n'):
    f=open(path,'r')
    lines=f.readlines()
    v=[]
    vt=[]
    vn=[]
    f={}
    iv=1
    for line in lines:
        if(bool(match("^v ",line))):
                v=v+[[float(x) for x in findall('-?[\d.]+',line)]]
        if(bool(match("^vt ",line))):
                vt=vt+[[float(x) for x in findall('-?[\d.]+',line)]]
        if((read_normals == 'y') & bool(match("^vn ",line))):
                vn=vn+[[float(x) for x in findall('-?[\d.]+',line)]]
        elif(bool(match("^vn ",line))):
                vn=vn+[[1,1,1]]
        if(bool(match("usemtl",line))):
                material=search("usemtl (.+)",line).group(1)
                f[material]={}
                f[material]['v']=[]
                f[material]['uv']=[]
                f[material]['vn']=[]
        if(bool(match("^f ",line))):
                f[material]['v']+=[[int(x) for x in findall(' ([\d.]+)/',line)]]
                f[material]['uv']+=[[int(x) for x in findall(' [\d.]+?/([\d.]+)',line)]]
                if(read_normals=='y'):
                    f[material]['vn']+=[[int(x) for x in findall(' [\d.]+?/[\d.]+?/([\d.]+)',line)]]
                else:
                    f[material]['vn']+=[[0 for x in findall(' ([\d.]+)/',line)]]
    return v,f,vt,vn

def blend(color, alpha, base=[255,255,255]):
    out = [int(round((alpha * color[i]) + ((1 - alpha) * base[i]))) for i in range(3)]
    return out

def to_hex(color):
    return ''.join(["%02x" % e for e in color])

def transform_srgb(c):
    if c < 0.0031308:
        srgb = 0.0 if c < 0.0 else c * 12.92
    else:
        srgb = 1.055 * (c ** (1.0 / 2.4)) - 0.055
    return max(min(int(srgb * 255 + 0.5), 255), 0)

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
                f[material]+=to_hex(blend([transform_srgb(float(x)) for x in findall('([\d.]+)',line)],1))
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

def extract_alphatest(input_str):
    if(bool(match(r".*alphatest=",input_str))):
        parsed_alpha=match(r'.*?alphatest=([0-9]+?)',input_str).group(1)
        return('alphatest="'+parsed_alpha+'"')
    else:
        return("")
def extract_zbias(input_str):
    if(bool(match(r".*zbias=",input_str))):
        parsed_zbias=match(r'.*?zbias=([0-9]+?)',input_str).group(1)
        return('zbias="'+parsed_zbias+'"')
    else:
        return("")



def convert_3d(name,v,f,vt,vn,mtl,scale_uv,invert_faces,model_tag,scale,use_normals):
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
            alphatest=extract_alphatest(batch)
            zbias=extract_zbias(batch)
            batch_replace=sub(r'["_\\/\-.]','',batch)
            command+="<batch id=\""+batch_replace+'" texture1="'+texture+'" '+zbias+' material="'+material+'" fvf="322" '+alphatest+' order="0">\n\t\t'
            kl=0
            allVertsUv=[]
            print("processing texture batch name: %s\nmaterial: %s\ntexture: %s\ncolor=%s\n%s\n" %tuple([batch,material,texture,color,zbias]))
            for face_v,face_uv,face_vn in zip(f[batch]['v'],f[batch]['uv'],f[batch]['vn']):
                allVertsUv+=[str(a-1)+'_'+str(b-1)+('_'+str(c-1) if use_normals=='y' else '') for a,b,c in zip(face_v,face_uv,face_vn)]
            allVertsUv=list(set(allVertsUv))
            allVertsTableId=dict(zip(allVertsUv,range(len(allVertsUv))))
            for face_v,face_uv,face_vn in zip(f[batch]['v'],f[batch]['uv'],f[batch]['vn']):
                    if len(face_v)==3:
                            vertsInd=[i-1 for i in face_v]
                            verts=[v[int(i)-1] for i in face_v]
                            uvInd=[i-1 for i in face_uv]
                            uv=[vt[int(i)-1] for i in face_uv]
                            vNormalInd=[i-1 for i in face_vn]
                            vNormal=[vn[int(i)-1] for i in face_vn]
                            for Ind,vertex,UVind,UV,vNorInd,vNor in zip(vertsInd,verts,uvInd,uv,vNormalInd,vNormal):
                                    kl+=1
                                    vertVal=str(Ind)+'_'+str(UVind)+('_'+str(vNorInd) if use_normals=='y' else '')
                                    INDEX=allVertsTableId[vertVal]
                                    vert_vals=[float(vr)*float(scale) for vr in vertex]
                                    vert_vals[2]=-vert_vals[2]
                                    vert_n=[float(vn_) for vn_ in vNor]
                                    vert_n[2]=-vert_n[2]
                                    if (Ind,UVind,vNorInd) not in verts_all:
                                            if use_normals=='y':
                                                verts_str+=[('<vertex id="%i" x="%0.6f" y="%0.6f" z="%0.6f" u1="%0.6f" v1="%0.6f" nx="%0.6f" ny="%0.6f" nz="%0.6f" diffuse="0xff%s"/>\n\t\t') % tuple([INDEX]+vert_vals+[UV[0]/scale_uv,-UV[1]/scale_uv]+vert_n+[color])]
                                            else:
                                                verts_str+=[('<vertex id="%i" x="%0.6f" y="%0.6f" z="%0.6f" u1="%0.6f" v1="%0.6f" diffuse="0xff%s"/>\n\t\t') % tuple([INDEX]+vert_vals+[UV[0]/scale_uv,-UV[1]/scale_uv]+[color])]
                                            verts_all+=[tuple([Ind,UVind]) if use_normals=='n' else tuple([Ind,UVind,vNorInd])]
                            if(use_normals=='n'):
                                if(invert_faces == 0):
                                    faces+=['\n\t\t<face v2="%i" v1="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)] for a,b in zip(vertsInd,uvInd)])]
                                elif(invert_faces ==1):
                                    faces+=['\n\t\t<face v1="%i" v2="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)] for a,b in zip(vertsInd,uvInd)])]
                                elif(invert_faces ==2):
                                    faces+=['\n\t\t<face v1="%i" v2="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)] for a,b in zip(vertsInd,uvInd)])]
                                    faces+=['\n\t\t<face v2="%i" v1="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)] for a,b in zip(vertsInd,uvInd)])]
                            else:
                                if(invert_faces == 0):
                                   faces+=['\n\t\t<face v2="%i" v1="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)+'_'+str(c)] for a,b,c in zip(vertsInd,uvInd,vNormalInd)])]
                                elif(invert_faces ==1):
                                    faces+=['\n\t\t<face v1="%i" v2="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)+'_'+str(c)] for a,b,c in zip(vertsInd,uvInd,vNormalInd)])]
                                elif(invert_faces ==2):
                                    faces+=['\n\t\t<face v1="%i" v2="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)+'_'+str(c)] for a,b,c in zip(vertsInd,uvInd,vNormalInd)])]
                                    faces+=['\n\t\t<face v2="%i" v1="%i" v3="%i"/>' % tuple([allVertsTableId[str(a)+'_'+str(b)+'_'+str(c)] for a,b,c in zip(vertsInd,uvInd,vNormalInd)])]
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
scale=input['scale']
use_normals=input['use_normals']

v,f,vt,vn=read_obj(model+'.obj',use_normals)
mtl=read_mtl(model+'.mtl')
res=convert_3d(model,v,f,vt,vn,mtl,scale_uv,invert_faces,model_tag,scale,use_normals)

save_to_file(res,output)
print("Conversion finished, output file:\n"+output+".xml")
