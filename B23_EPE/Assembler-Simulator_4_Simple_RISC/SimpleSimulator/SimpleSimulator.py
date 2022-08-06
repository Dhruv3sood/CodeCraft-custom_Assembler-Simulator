#invalid format for mantissa treat as underflow
from itertools import count
import sys
regvaldict={'PC':'0','R0':'0000000000000000','R1':'0000000000000000','R2':'0000000000000000','R3':'0000000000000000','R4':'0000000000000000','R5':'0000000000000000','R6':'0000000000000000','FLAGS':'0000000000000000'}
register={'000':'R0','001':'R1','010':'R2','011':'R3','100':'R4','101':'R5','110':'R6','111':'FLAGS'}
def floatingpointtodecimal(val):
    val=val[8:]
    exp=int(val[:3],2)
    mantissa=val[3:]
    if exp<5:
        binaryform='1'+mantissa[:exp]+'.'+mantissa[exp:]
    else:
        binaryform='1'+mantissa[:5]+'0'*(exp-5)
    decimal=float(0)
    for i in range(0,exp+1):
        decimal=float(decimal+(int(binaryform[i],2)*2**(exp-i)))
    for i in range(exp+2,len(binaryform)):
        decimal=decimal+float(int(binaryform[i],2)*2**(exp+1-i))
    decimal=str(decimal)
    return decimal
def decimaltobinary(val):
    val=val.split('.')
    binaryform=[]
    left=int(val[0])
    while left!=0:
        r=left%2
        binaryform.append(str(r))
        left=int(left/2)
    binaryform=binaryform[::-1]
    if len(val)==2:
        right=float(int(val[1])/10**len(val[1]))
        if right!=0:
            binaryform.append('.')
            while True:
                if right==1:
                    binaryform.append('1')
                    break
                else:
                    right=right*2
                    if(right>1):
                        binaryform.append('1')
                        right=float(right-1)
                    if (right<1):
                        binaryform.append('0')
    binaryform=''.join(binaryform)
    return binaryform
def binarytofloatingpoint(val):
    c=0
    for i in val:
        if i=='.':
            break
        else:
            c=c+1
    if c-1<8:
        exp=c-1
    else:
        exp=7
    exp=decimaltobinary(str(exp))
    if len(exp)<3:
        exp='0'*(3-len(exp))+exp
    mantissa=[]
    for i in range(1,6):
        if val[i]!='.':
            mantissa.append(val[i])
    for i in range(6,len(val)):
        if val[i]==1:
            mantissa='11111'
    mantissa=''.join(mantissa)
    floatingpoint=exp+mantissa
    floatingpoint=list(floatingpoint)
    for i in range(len(floatingpoint),8):
        floatingpoint.append('0')
    floatingpoint=''.join(floatingpoint)
    return floatingpoint
def printreg(regvaldict):
    for i in regvaldict:
        regcorrect(regvaldict,i)
    pcval=bin(int(regvaldict['PC'],2))[2:]
    pcextra=str('0'*((8)-len(pcval)))
    pccorrect=pcextra+pcval
    # for i in regvaldict:
    #     if i!='PC':
    #         print(RF(regvaldict,i),end=' ')
    #     else:
    #         print(pccorrect,end=' ')
    # print()
    # r=[]
    # r.append(pccorrect)
    # for i in regvaldict:
    #     if i!='PC':
    #         r.append(RF(regvaldict,i))
    # temp=list(r[-1])
    # if temp[-1]==' ':
    #     temp=temp[:-1]
    # r[-1]="".join(temp)
    # r=" ".join(r)
    # print(r)
    sys.stdout.write(pccorrect+' ')
    for i in regvaldict:
        if i!='PC' and i!='FLAGS':
            sys.stdout.write(regvaldict[i]+' ')
    flagbits=regvaldict['FLAGS']
    sys.stdout.write(flagbits+'\n')
def regcorrect(regvaldict,regname):
    if (regname!='FLAGS'):
        if (len(RF(regvaldict,regname))!=16):
            extra=str('0'*((16)-len(RF(regvaldict,regname))))
            correct=extra+RF(regvaldict,regname)
            regvaldict[regname]=correct
    else:
        if (len(RF(regvaldict,regname))!=16):
            extra=str('0'*((16)-len(RF(regvaldict,regname))))
            correct=extra+RF(regvaldict,regname)
            regvaldict[regname]=correct
def reg(s,regdict):
    return regdict.get(s)
def MEM(pc,l):
    pos=int(pc,2)
    return l[pos]
def PC(cur,val):
    return cur+val
def RF(regvaldict,regname):
    return regvaldict.get(regname)
#overflow flag set is remaining
def EE(pc,l,regdict,regvaldict):
    inst=MEM(pc,l)
    strlist=list(RF(regvaldict,'FLAGS'))

    # strlist[12]='0'
    # regvaldict['FLAGS']="".join(strlist).strip(" ")
    # if (inst[:5]!='11110' or inst[:5]!='01100' or inst[:5]!='01101' or inst[:5]!='01111'):
    #     strlist[13]='0'
    #     strlist[14]='0'
    #     strlist[15]='0'
    #     regvaldict['FLAGS']="".join(strlist).strip(" ")
    if(inst[:5]=='10000'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        addi=int(RF(regvaldict,reg1),2)+int(RF(regvaldict,reg2),2)
        if addi<256:
            regvaldict[reg3]=bin(addi)[2:]
            strlist[12]='0'
        elif addi>=256:
            regvaldict[reg3]=bin(addi%(2**16))[2:]
            strlist[12]='1'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
        pc=bin(int(pc,2)+1)[2:]
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if(inst[:5]=='10001'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        if (int(RF(regvaldict,reg1),2)>=int(RF(regvaldict,reg2),2)):
            regvaldict[reg3]=bin(int(RF(regvaldict,reg1),2)-int(RF(regvaldict,reg2),2))[2:]
            strlist[12]='0'
        else:
            regvaldict[reg3]=bin(0)[2:]
            strlist[12]='1'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if(inst[:5]=='10010'):
        reg1=reg(inst[5:8],regdict)
        immval=inst[8:]
        regvaldict[reg1]=immval
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='10011'):
        reg1=reg(inst[10:13],regdict)
        reg2=reg(inst[13:],regdict)
        regvaldict[reg2]=RF(regvaldict,reg1)

        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='10100'):
        reg1=reg(inst[5:8],regdict)
        val=MEM(inst[8:],l)
        regvaldict[reg1]=val
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='10101'):
        reg1=reg(inst[5:8],regdict)
        l[int(inst[8:],2)]=regvaldict[reg1]
        if (len(l[int(inst[8:],2)])!=16):
            extra=str('0'*((16)-len(l[int(inst[8:],2)])))
            l[int(inst[8:],2)]=extra+regvaldict[reg1]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='10110'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        mult=int(RF(regvaldict,reg1),2)*int(RF(regvaldict,reg2),2)
        if mult<256:
            regvaldict[reg3]=bin(int(RF(regvaldict,reg1),2)*int(RF(regvaldict,reg2),2))[2:]
        else:
            regvaldict[reg3]=bin(mult%(2**16))[2:]
            strlist[12]='1'
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='10111'):
        reg1=reg(inst[10:13],regdict)
        reg2=reg(inst[13:],regdict)
        regvaldict['R0']=bin(int(RF(regvaldict,reg1),2)//int(RF(regvaldict,reg2),2))[2:]
        regvaldict['R1']=bin(int(RF(regvaldict,reg1),2)%int(RF(regvaldict,reg2),2))[2:]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='11000'):
        reg1=reg(inst[5:8],regdict)
        immval=inst[8:]
        regvaldict[reg1]=bin(int(RF(regvaldict,reg1),2)>>int(immval,2))[2:]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='11001'):
        reg1=reg(inst[5:8],regdict)
        immval=inst[8:]
        regvaldict[reg1]=bin(int(RF(regvaldict,reg1),2)<<int(immval,2))[2:]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[5:]=='11010'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        regvaldict[reg3]=bin(int(RF(regvaldict,reg1),2)^int(RF(regvaldict,reg2),2))[2:]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[5:]=='11011'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        regvaldict[reg3]=bin(int(RF(regvaldict,reg1),2)|int(RF(regvaldict,reg2),2))[2:]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[5:]=='11100'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        regvaldict[reg3]=bin(int(RF(regvaldict,reg1),2)&int(RF(regvaldict,reg2),2))[2:]
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='11101'):
        reg1=reg(inst[10:13],regdict)
        reg2=reg(inst[13:],regdict)
        lreg1=list(regvaldict[reg1])
        for i in range(len(lreg1)):
            if lreg1[i]=='0':
                lreg1[i]='1'
            elif lreg1[i]=='1':
                lreg1[i]='0'
        lreg1="".join(lreg1)

        regvaldict[reg2]=lreg1
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='11110'):
        reg1=reg(inst[10:13],regdict)
        reg2=reg(inst[13:],regdict)
        if (int(RF(regvaldict,reg1))>int(RF(regvaldict,reg2))):
            strlist[14]='1'
            strlist[13]='0'
            strlist[15]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            gflag=True
        elif (int(RF(regvaldict,reg1))<int(RF(regvaldict,reg2))):
            strlist[13]='1'
            strlist[14]='0'
            strlist[15]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            lflag=True
        elif (int(RF(regvaldict,reg1))==int(RF(regvaldict,reg2))):
            strlist[15]='1'
            strlist[14]='0'
            strlist[13]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            eflag=True
        pc=bin(int(pc,2)+1)[2:]
        
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='11111'):
        addr=inst[8:]
        pc=addr
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='01100'):
        if (RF(regvaldict,'FLAGS')[13]=='1'):
            addr=inst[8:]
            pc=addr
            strlist[13]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            printreg(regvaldict)
            regvaldict['PC']=pc
            EE(pc,l,regdict,regvaldict)
        else:
            strlist[12]='0'
            strlist[13]='0'
            strlist[14]='0'
            strlist[15]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            pc=bin(int(pc,2)+1)[2:]
            
            printreg(regvaldict)
            regvaldict['PC']=pc
            EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='01101'):
        if (RF(regvaldict,'FLAGS')[14]=='1'):
            addr=inst[8:]
            pc=addr
            
            strlist[14]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            printreg(regvaldict)
            regvaldict['PC']=pc
            EE(pc,l,regdict,regvaldict)
        else:
            strlist[12]='0'
            strlist[13]='0'
            strlist[14]='0'
            strlist[15]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            pc=bin(int(pc,2)+1)[2:]
            printreg(regvaldict)
            regvaldict['PC']=pc
            EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='01111'):
        if (RF(regvaldict,'FLAGS')[15]=='1'):
            addr=inst[8:]
            pc=addr
            
            strlist[15]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            printreg(regvaldict)
            regvaldict['PC']=pc
            EE(pc,l,regdict,regvaldict)
        else:
            strlist[12]='0'
            strlist[13]='0'
            strlist[14]='0'
            strlist[15]='0'
            regvaldict['FLAGS']="".join(strlist).strip(" ")
            pc=bin(int(pc,2)+1)[2:]
            
            printreg(regvaldict)
            regvaldict['PC']=pc
            EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='01010'):
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        pass
    if (inst[:5]=='00000'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        reg1val=RF(regvaldict,reg1)
        reg2val=RF(regvaldict,reg2)
        regval1=floatingpointtodecimal(reg1val)
        regval2=floatingpointtodecimal(reg2val)
        addi=float(regval1)+float(regval2)
        inbinary=decimaltobinary(str(addi))
        resfp=binarytofloatingpoint(inbinary)
        if resfp[3:]=='11111':
            strlist[12]='1'
        else:
            strlist[12]='0'
        s=list(regvaldict[reg3])
        for i in range(8,len(s)):
            s[i]=resfp[i-8]
        regvaldict[reg3]=''.join(s)
        pc=bin(int(pc,2)+1)[2:]
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if (inst[:5]=='00001'):
        reg1=reg(inst[7:10],regdict)
        reg2=reg(inst[10:13],regdict)
        reg3=reg(inst[13:16],regdict)
        reg1val=RF(regvaldict,reg1)
        reg2val=RF(regvaldict,reg2)
        regval1=floatingpointtodecimal(reg1val)
        regval2=floatingpointtodecimal(reg2val)
        addi=float(regval1)-float(regval2)
        if addi<0:
            strlist[12]='1'
            resfp='00000000'
        else:
            strlist[12]='0'
            inbinary=decimaltobinary(str(addi))
            resfp=binarytofloatingpoint(inbinary)
        s=list(regvaldict[reg3])
        for i in range(8,len(s)):
            s[i]=resfp[i-8]
        regvaldict[reg3]=''.join(s)
        pc=bin(int(pc,2)+1)[2:]
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
    if(inst[:5]=='00010'):
        reg1=reg(inst[5:8],regdict)
        immval=inst[8:]
        s=list(regvaldict[reg1])
        for i in range(8,len(s)):
            s[i]=immval[i-8]
        regvaldict[reg1]=''.join(s)
        pc=bin(int(pc,2)+1)[2:]
        
        strlist[12]='0'
        strlist[13]='0'
        strlist[14]='0'
        strlist[15]='0'
        regvaldict['FLAGS']="".join(strlist).strip(" ")
        printreg(regvaldict)
        regvaldict['PC']=pc
        EE(pc,l,regdict,regvaldict)
l=[]
l=sys.stdin.readlines()
l=[x.strip() for x in l]
for i in range(len(l),256):
    l.append('0000000000000000')
initialpos=RF(regvaldict,'PC')
EE(initialpos,l,register,regvaldict)
for i in l:
    sys.stdout.write(i)
    sys.stdout.write('\n')