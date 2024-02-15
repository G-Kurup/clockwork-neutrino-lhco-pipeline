import numpy as np
from numpy import linalg
import datetime
from sys import argv

# Output file
output_file = open('Clockwork.fr', 'a+')   
output_file.truncate(0)

#Parameters
N = 13
q = 1.15
m = 50.0
y = np.array([0.0133466, 0.0134794, 0.0173801])

def eigen(n, q, y):
    p = y*246/(np.sqrt(2)*m)
    A = np.identity(n+1)

    for i in range(0, n+1):
        for j in range(0, n+1):
            if(j-i == 1):
                A[i,j] = -q*(n-i)

    A[n,n] = p

    # Singular value decomposition
    L, M, R = linalg.svd(A, full_matrices=1, compute_uv=1)
    return L, M, R

def info():
    Istr = "M$ModelName = \"Clockwork_Neutrino\"; \n\nM$Information = {\n\
    \tAuthors      -> {\"G. Kurup\"},\n\
    \tVersion      -> \"1.0\",\n\
    \tDate         -> \"%s\",\n\
    \tInstitutions -> {\"Cornell University\"},\n\
    \tEmails       -> {\"gk377@cornell.edu\"}\n\
    }; \n\nFeynmanGauge = False; \n " % (datetime.date.today())
    return Istr        

def param():
    Pstr = "M$Parameters = { \n\tyCW == {\n\
    \t\tParameterType    -> External,\n\
    \t\tIndices          -> {Index[Generation]}, \n\
    \t\tValue            -> {yCW[1] -> %.10f, yCW[2] -> %.10f, yCW[3] -> %.10f},\n\
    \t\tComplexParameter -> False,\n\
    \t\tInteractionOrder -> {QED,1}, \n\
    \t\tDescription      -> \"Yukawa couplings to Nth clockwork gear\"\n\
	\t},\n\n\
    PMNS == {\n\
    \t\tParameterType    -> External,\n\
    \t\tIndices          -> {Index[Generation], Index[Generation]}, \n\
    \t\tUnitary          -> True, \n\
    \t\tValue            -> {PMNS[1,1] ->  0.8294,  PMNS[2,1] ->  0.5391,  PMNS[3,1] ->  0.1466, \n\
                     \t\t\t PMNS[1,2] -> -0.4934,  PMNS[2,2] ->  0.5837,  PMNS[3,2] ->  0.6449, \n\
                     \t\t\t PMNS[1,3] ->  0.2621,  PMNS[2,3] -> -0.6072,  PMNS[3,3] ->  0.7501},\n\
    \t\tComplexParameter -> False,\n\
    \t\tDescription      -> \"Transpose of PMNS matrix\"\n\
	\t}\n\
    };\n" % (y[0], y[1], y[2])
    return Pstr

def fieldDef(num, m):
    pdg = str(990000 + num)
    Fstring = "\tF[%s1] == { \n \
        \tClassName       -> Ns%s1, \n \
        \tSelfConjugate   -> False, \n \
        \tMass            -> {mN%s1, %s}, \n \
        \tWidth           -> 1.0, \n \
        \tPDG             -> %s1, \n \
        \tQuantumNumbers  -> {LeptonNumber -> 1}, \n\
        \tPropagatorType  -> Straight, \n \
        \tParticleName    -> \"Ns%s1\" \n \
    \t},\n\n \
   F[%s2] == { \n \
        \tClassName       -> Ns%s2, \n \
        \tSelfConjugate   -> False, \n \
        \tMass            -> {mN%s2, %s}, \n \
        \tWidth           -> 1.0, \n \
        \tPDG             -> %s2, \n \
        \tQuantumNumbers  -> {LeptonNumber -> 1}, \n\
        \tPropagatorType  -> Straight, \n \
        \tParticleName    -> \"Ns%s2\" \n \
    \t},\n\n \
   F[%s3] == { \n \
        \tClassName       -> Ns%s3, \n \
        \tSelfConjugate   -> False, \n \
        \tMass            -> {mN%s3, %s}, \n \
        \tWidth           -> 1.0, \n \
        \tPDG             -> %s3, \n \
        \tQuantumNumbers  -> {LeptonNumber -> 1}, \n\
        \tPropagatorType  -> Straight, \n \
        \tParticleName    -> \"Ns%s3\" \n \
    \t}" % (str(100+num), num, num, m[0], pdg, num, str(100+num), num, num, m[1], pdg, num, str(100+num), num, num, m[2], pdg, num) 
    return Fstring
    
def fieldDefList(n, M):
    FLstr = "M$ClassesDescription = { \n"    
    for i in range(1,n):
        FLstr = FLstr + fieldDef(i,M[i-1,:]) + ",\n\n"
    FLstr = FLstr + fieldDef(N,M[N-1,:]) + "\n};\n"    
    return FLstr    
    
def lagKin(n):
    Lstring = "LCW :=  "
    for i in range(1, n+1):
        temp  = "I Ns%(i)s1bar[s1] Ga[v,s1,s2] del[Ns%(i)s1[s2],v] - mN%(i)s1 Ns%(i)s1bar[s1] Ns%(i)s1[s1] +\\\n \t\t" % {'i': str(i) }
        temp += "I Ns%(i)s2bar[s1] Ga[v,s1,s2] del[Ns%(i)s2[s2],v] - mN%(i)s2 Ns%(i)s2bar[s1] Ns%(i)s2[s1] +\\\n \t\t" % {'i': str(i) }
        temp += "I Ns%(i)s3bar[s1] Ga[v,s1,s2] del[Ns%(i)s3[s2],v] - mN%(i)s3 Ns%(i)s3bar[s1] Ns%(i)s3[s1] +\\\n \t\t" % {'i': str(i) }
        Lstring = Lstring + temp
    Lstring = Lstring[:-6] + '\n'
    return Lstring    
   
def lagInt(n, ULarray, URarray):
    Lstring = "Lint := "
    for i in range(1, n+1):
        temp  = "- gw/Sqrt[2] *(%.10f)* PMNS[1, 1] Ns%s1bar.W[m].ProjM[m].e  \\\n \t\t" % (ULarray[i-1,0], str(i))
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[1, 2] Ns%s1bar.W[m].ProjM[m].mu \\\n \t\t" % (ULarray[i-1,0], str(i))
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[1, 3] Ns%s1bar.W[m].ProjM[m].ta \\\n \t\t" % (ULarray[i-1,0], str(i))
        
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[2, 1] Ns%s2bar.W[m].ProjM[m].e  \\\n \t\t" % (ULarray[i-1,1], str(i))
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[2, 2] Ns%s2bar.W[m].ProjM[m].mu \\\n \t\t" % (ULarray[i-1,1], str(i))
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[2, 3] Ns%s2bar.W[m].ProjM[m].ta \\\n \t\t" % (ULarray[i-1,1], str(i))
        
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[3, 1] Ns%s3bar.W[m].ProjM[m].e  \\\n \t\t" % (ULarray[i-1,2], str(i))
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[3, 2] Ns%s3bar.W[m].ProjM[m].mu \\\n \t\t" % (ULarray[i-1,2], str(i))
        temp += "- gw/Sqrt[2] *(%.10f)* PMNS[3, 3] Ns%s3bar.W[m].ProjM[m].ta \\\n \t\t" % (ULarray[i-1,2], str(i))
        
        Lstring = Lstring + temp
        
    for i in range(1, n+1):
        temp  = "- gw/(2 cw) *(%.10f)* PMNS[1, 1] Ns%s1bar.Z[m].ProjM[m].ve \\\n \t\t" % (ULarray[i-1,0], str(i))
        temp += "- gw/(2 cw) *(%.10f)* PMNS[1, 2] Ns%s1bar.Z[m].ProjM[m].vm \\\n \t\t" % (ULarray[i-1,0], str(i))
        temp += "- gw/(2 cw) *(%.10f)* PMNS[1, 3] Ns%s1bar.Z[m].ProjM[m].vt \\\n \t\t" % (ULarray[i-1,0], str(i))
        
        temp += "- gw/(2 cw) *(%.10f)* PMNS[2, 1] Ns%s2bar.Z[m].ProjM[m].ve \\\n \t\t" % (ULarray[i-1,1], str(i))
        temp += "- gw/(2 cw) *(%.10f)* PMNS[2, 2] Ns%s2bar.Z[m].ProjM[m].vm \\\n \t\t" % (ULarray[i-1,1], str(i))
        temp += "- gw/(2 cw) *(%.10f)* PMNS[2, 3] Ns%s2bar.Z[m].ProjM[m].vt \\\n \t\t" % (ULarray[i-1,1], str(i))
        
        temp += "- gw/(2 cw) *(%.10f)* PMNS[3, 1] Ns%s3bar.Z[m].ProjM[m].ve \\\n \t\t" % (ULarray[i-1,1], str(i))
        temp += "- gw/(2 cw) *(%.10f)* PMNS[3, 2] Ns%s3bar.Z[m].ProjM[m].vm \\\n \t\t" % (ULarray[i-1,1], str(i))
        temp += "- gw/(2 cw) *(%.10f)* PMNS[3, 3] Ns%s3bar.Z[m].ProjM[m].vt \\\n \t\t" % (ULarray[i-1,1], str(i))
        
        Lstring = Lstring + temp
        
    for i in range(1, n+1):
        temp  = "- yCW[1]/Sqrt[2] *(%.10f)* PMNS[1, 1] H vebar.ProjM.Ns%s1 \\\n \t\t" % (URarray[i-1, 0], str(i))
        temp += "- yCW[1]/Sqrt[2] *(%.10f)* PMNS[1, 2] H vmbar.ProjM.Ns%s1 \\\n \t\t" % (URarray[i-1, 0], str(i))
        temp += "- yCW[1]/Sqrt[2] *(%.10f)* PMNS[1, 3] H vtbar.ProjM.Ns%s1 \\\n \t\t" % (URarray[i-1, 0], str(i))
        
        temp += "- yCW[2]/Sqrt[2] *(%.10f)* PMNS[2, 1] H vebar.ProjM.Ns%s2 \\\n \t\t" % (URarray[i-1, 0], str(i))
        temp += "- yCW[2]/Sqrt[2] *(%.10f)* PMNS[2, 2] H vmbar.ProjM.Ns%s2 \\\n \t\t" % (URarray[i-1, 0], str(i))
        temp += "- yCW[2]/Sqrt[2] *(%.10f)* PMNS[2, 3] H vtbar.ProjM.Ns%s2 \\\n \t\t" % (URarray[i-1, 0], str(i))
        
        temp += "- yCW[3]/Sqrt[2] *(%.10f)* PMNS[3, 1] H vebar.ProjM.Ns%s3 \\\n \t\t" % (URarray[i-1, 0], str(i))
        temp += "- yCW[3]/Sqrt[2] *(%.10f)* PMNS[3, 2] H vmbar.ProjM.Ns%s3 \\\n \t\t" % (URarray[i-1, 0], str(i))
        temp += "- yCW[3]/Sqrt[2] *(%.10f)* PMNS[3, 3] H vtbar.ProjM.Ns%s3 \\\n \t\t" % (URarray[i-1, 0], str(i))
        
        Lstring = Lstring + temp
        
    Lstring = Lstring[:-6] + '\n'
    return Lstring   

L1, d1, R1 = eigen(N, q, y[0])  
L2, d2, R2 = eigen(N, q, y[1])  
L3, d3, R3 = eigen(N, q, y[2])  

M  = np.column_stack((m*d1[0:N], m*d2[0:N], m*d3[0:N]))
UL = np.column_stack((L1[N,:], L2[N,:], L3[N,:]))
UR = np.column_stack((R1[:,N], R2[:,N], R3[:,N]))

#M[M<1e-12]=0
   
output_file.write(info()+'\n')
output_file.write(param()+'\n')
output_file.write(fieldDefList(N,M)+'\n')
output_file.write(lagKin(N)+'\n')
output_file.write(lagInt(N, UL, UR)+'\n')
output_file.write('LFull := LSM + LCW + Lint + HC[Lint];\n')
output_file.close() 