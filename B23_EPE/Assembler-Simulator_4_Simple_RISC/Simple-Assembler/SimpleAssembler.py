#checkout memory overflow error when var cant be allocated memory due to many instructions as input
import sys
# dictionary to map instructions with their type
def category(lst):
    type={'add':1,'sub':1,'mov1':2,'mov2':3,'ld':4,'st':4,'mul':1,'div':3,'rs':2,'ls':2,'xor':1,'or':1,'and':1,'not':3,'cmp':3,'jmp':5,
    'jlt':5,'jgt':5,'je':5,'hlt':6,'addf':1,'subf':1,'movf':2}
    return type.get(lst[0])

# checks if instruction is valid or not
def instrcheck(lst):
    instr={'add','sub','mov','ld','st','mul','div','rs','ls','xor','or','and','not','cmp','jmp','jlt','jgt','je','hlt','var','addf','subf','movf'}
    c=0
    for i in lst:
        c=c+1
        try:
            if i[0] not in instr:
                print("error found on line no. "+str(c)+": "+i[0]+" is not a valid instruction")
                exit()
        except IndexError:
            print("error found on line no. "+str(c)+": empty label declaration")
            exit()
            

# checks if registor name is valid or not            
def regcheck(insrc,reg):
    c=0
    for i in insrc:
        c=c+1
        ctg=category(i)
        if ctg==1:
            if (i[1] not in reg):
                print("error found on line no. "+str(c)+": "+i[1]+" is not a valid register name")
                exit()
            if (i[2] not in reg):
                print("error found on line no. "+str(c)+": "+i[2]+" is not a valid register name")
                exit()
            if (i[3] not in reg):
                print("error found on line no. "+str(c)+": "+i[3]+" is not a valid register name")
                exit()
        if ctg==2 or ctg==4:
            if (i[1] not in reg):
                print("error found on line no. "+str(c)+": "+i[1]+" is not a valid register name")
                exit()
        if ctg==3:
            if (i[1] not in reg):
                if i[1]!='FLAGS':
                    print("error found on line no. "+str(c)+": "+i[1]+" is not a valid register name")
                    exit()
            if (i[2] not in reg):
                print("error found on line no. "+str(c)+": "+i[2]+" is not a valid register name")
                exit()
                

# checks if variable is defined or not                
def varcheck(src,varname):
    c=0
    for i in src:
        c=c+1
        ctg=category(i)
        if ctg==4:
            if i[2] not in varname:
                print("error found on line no. "+str(c)+": "+i[2]+" is an undefined variable")
                exit()
                
# checks if label is defined or not                
def labelcheck(insrc,labelname):
    c=0
    for i in insrc:
        c=c+1
        ctg=category(i)
        if ctg==5:
            if i[1] not in labelname:
                print("error found on line no. "+str(c)+": "+i[1]+" is an undefined label")
                exit()
                
# checks if flag registor is used illegally or not                
def FLAGScheck(insrc):
    c=0
    for i in insrc:
        c=c+1
        ctg=category(i)
        if ctg!=3:
            if 'FLAGS' in i:
                print("error found on line no. "+str(c)+": Illegal use of FLAGS register")
                exit()
        if ctg==3:
            if i[2]=='FLAGS':
                print("error found on line no. "+str(c)+": Illegal use of FLAGS register")
                exit()
                
# checks the range of immediate value                
def immvalcheck(insrc):
    c=0
    for i in insrc:
        c=c+1
        ctg=category(i)
        if ctg==2:
            if int(i[2][1:]) not in range(0,256):
                print("error found on line no. "+str(c)+": "+i[2][1:]+" is out of range")
                exit()
                
# checks if variable name is used in place of label name and vice versa                
def varandlabelcheck(insrc,varname,labelname):
    c=0
    for i in insrc:
        c=c+1
        ctg=category(i)
        if ctg==4:
            if i[2] not in varname and i[2] in labelname:
                print("error found on line no. "+str(c)+": label "+i[2]+" is used in place of a variable")
                exit()
        if ctg==5:
            if i[1] not in labelname and i[1] in varname:
                print("error found on line no. "+str(c)+": variable "+i[1]+" is used in place of a label")
                exit()
                
# checks if the variables are declared at the beginning or not                
def vardeclarecheck(varchecksrc,v):
    c=v
    for i in varchecksrc:
        c=c+1
        if i[0]=='var':
            print("error found on line no. "+str(c)+": variable "+i[1]+" not declared at the beginning")
            exit()
            
# checks is halt is present or not           
def hltcheck(insrc):
    j=['hlt']
    if j not in insrc:
        print("error: hlt instruction missing")
        exit()
        
# checks if halt is not used as the last instruction        
def hltplacecheck(insrc):
    c=0
    for i in range(0,len(insrc)-1):
        c=c+1
        if 'hlt' in insrc[i]:
            print("error found on line no. "+str(c)+": hlt not used as the last instruction")
            exit()
            
# checks if the label is used multiple time            
def labelcountcheck(labelname,srctext):
    s=set(labelname)
    for i in s:
        line=0
        c=0
        for j in srctext:
            line=line+1
            if j[0][0:-1]==i:
                c=c+1
                if c>1:
                    print("error found on line no. "+str(line)+": label \'"+str(j[0][0:-1])+"\' has been used earlier")
                    exit()
                    
# checks the general syntax of the instructions                    
def syntaxcheck(srctext):
    instrcheck(srctext)
    c=0
    for i in srctext:
        c=c+1
        ctg=category(i)
        if i[0]=='var':
            if len(i)!=2:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
        if ctg==1:
            if len(i)!=4:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
        if i[0]=='mov':
            if len(i)!=3:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
        if ctg==4:
            if len(i)!=3:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
        if ctg==5:
            if len(i)!=2:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
        if ctg==6:
            if len(i)!=1:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
        if i[0]=='var':
            if len(i)!=2:
                print("error found on line no. "+str(c)+": General syntax error")
                exit()
                
# dictionary to map instructions with their respective opcode                
def opc(s):
    opcode={'add':'10000','sub':'10001','mov1':'10010','mov2':'10011','ld':'10100','st':'10101','mul':'10110','div':'10111','rs':'11000',
    'ls':'11001','xor':'11010','or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111','jlt':'01100','jgt':'01101',
    'je':'01111','hlt':'01010','addf':'00000','subf':'00001','movf':'00010'}
    return opcode.get(s)

#dictionary to map registers with their respective address
def regadd(s):
    regadr={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}
    return regadr.get(s)

#function to convert integer to 8 bit binary
def binary(c):
    bit=[]
    s=''
    while c!=0:
        bit.append(str(c%2))
        c=c//2
    while len(bit)!=8:
        bit.append('0')
    for i in range(0,8):
        s=s+bit[7-i]
    return s

#fuctions to return binary codes of respective types of instructions
def typeA(lst):
    str=''
    str=opc(lst[0])+'00'+regadd(lst[1])+regadd(lst[2])+regadd(lst[3])
    return str+'\n'
def typeB(lst):
    str=''
    str=opc(lst[0])+regadd(lst[1])+binary(int(lst[2][1:]))
    return str+'\n'
def typeC(lst):
    str=''
    str=opc(lst[0])+'00000'+regadd(lst[1])+regadd(lst[2])
    return str+'\n'
def typeD(lst):
    str=''
    str=opc(lst[0])+regadd(lst[1])+lst[2]
    return str+'\n'
def typeE(lst):
    str=''
    str=opc(lst[0])+'000'+lst[1]
    return str+'\n'
def typeF(lst):
    str=''
    str=opc(lst[0])+'00000000000'
    return str+'\n'

#  MAIN
reg={'R0','R1','R2','R3','R4','R5','R6'}

#taking input
l=[]
l=sys.stdin.readlines()
l=[x.strip().split() for x in l]
for i in l:
    if i==[]:
        l.remove(i)
# with open("C:/Users/priya_5c9gi56/OneDrive/Desktop/stdin.txt","r") as f:
#     data=sys.stdout.readline()
#     x=data.strip().split()
#     while len(x)>0:
#         l.append(x)
#         data=sys.stdout.readline()
#         x=data.strip().split()


c=0
v=0
for i in l:
    if i[0]!='var':
        c=c+1
    else:
        v=v+1
varchecksrc=[]
varname=[]
varadd={}
insrc=[]
a=0
labeladd={}
labelname=[]
for i in l:
    if i[0][-1]==':':
        labelname.append(i[0][0:-1])
labelcountcheck(labelname,l)
for i in l:
    if i[0][-1]==':':
        if a+v!=len(l)-2:
            labeladd[i[0][0:-1]]=binary(a)
            del i[0]
        else:
            labeladd[i[0][0:-1]]=binary(a+1)
            del i[0]
    elif i[0]!='var':
        a=a+1
for i in range(0,len(l)):
    insrc.append(l[i])
syntaxcheck(insrc)
hltcheck(insrc)
hltplacecheck(insrc)
for i in range(0,v):
    varname.append(l[i][1])
for i in l:
    if i[0]=='mov':
        if i[2][0]=='$':
            i[0]='mov1'
        else:
            i[0]='mov2'
for i in range(v,len(l)):
    varchecksrc.append(l[i])
FLAGScheck(insrc)
regcheck(insrc,reg)
varandlabelcheck(insrc,varname,labelname)
varcheck(insrc,varname)
labelcheck(insrc,labelname)
immvalcheck(insrc)
vardeclarecheck(varchecksrc,v)
# hltcheck(insrc)
# hltplacecheck(insrc)
for i in l:
    if i[0]=='var':
        varadd[i[1]]=binary(c)
        c=c+1
for i in l:
    ctg=category(i)
    if ctg==1:
        sys.stdout.write(typeA(i))
    if ctg==2:
        sys.stdout.write(typeB(i))
    if ctg==3:
        sys.stdout.write(typeC(i))
    if ctg==4:
        i[2]=varadd.get(i[2])
        sys.stdout.write(typeD(i))
    if ctg==5:
        i[1]=labeladd.get(i[1])
        sys.stdout.write(typeE(i))
    if ctg==6:
        sys.stdout.write(typeF(i))
