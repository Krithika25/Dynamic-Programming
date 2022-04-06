import pandas as pd
import numpy as np
import psutil
import time
import os
import sys

#Defining the gap and mismatching penalty
alpha=[[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
enum={'A':0,'C':1,'G':2,'T':3}
delta=30

#String Generation
def generate_string(s):
  A=[]
  s_a=[]
  s_b=[]
  s_found=0
  for i in range(len(s)):
    c=-1
    for j in range(len(s[i])):
      if s[i][j].isdigit():
        c=0
        c=(10*c)+int(s[i][j])
      else:
        break
    if c==-1:
      s_found=s_found+1
      if s[i][-1]=='\n':
        A.append(str(s[i][:-1]))
      else:
        A.append(str(s[i]))
    elif s_found==1:
      s_a.append(c)
    elif s_found==2:
      s_b.append(c)

  if len(A)==1:
    A.append('')

  gen_str_a=A[0]
  gen_str_b=A[1]
  for i in range(len(s_a)):
    gen_str_a=gen_str_a[0:s_a[i]+1]+gen_str_a+gen_str_a[s_a[i]+1:]

  for i in range(len(s_b)):
    gen_str_b=gen_str_b[:s_b[i]+1]+gen_str_b+gen_str_b[s_b[i]+1:]
  
  return gen_str_a, gen_str_b

#Dynamic Programming version of the Sequence alignment algorithm
def alignment(x,y):
  #pr=psutil.Process(os.getpid())
  m=len(x)
  n=len(y)
  A=np.zeros((m+1,n+1))
  #Path=np.empty((m+1,n+1), dtype=object)
  for i in range(m+1):
    A[i][0]=i*delta
    #Path[i][0]='l'
  for i in range(n+1):
    A[0][i]=i*delta
    #Path[0][i]='u'
  
  for i in range(1,m+1):
    for j in range(1,n+1):
      A[i][j]=min(alpha[enum[x[i-1]]][enum[y[j-1]]]+A[i-1][j-1], delta+A[i-1][j], delta+A[i][j-1])
    
  i=m
  j=n
  row=[]
  column=[]
  while i>0 and j>0:
    if A[i][j]==alpha[enum[x[i-1]]][enum[y[j-1]]]+A[i-1][j-1]:
      row.insert(0, x[i-1])
      column.insert(0, y[j-1])
      i=i-1
      j=j-1
    elif A[i][j]==delta+A[i][j-1]:
      row.insert(0, '_')
      column.insert(0, y[j-1])
      j=j-1
    elif A[i][j]==delta+A[i-1][j]:
      row.insert(0, x[i-1])
      column.insert(0, '_')
      i=i-1
      
  while i>0:
    row.insert(0, x[i-1])
    column.insert(0, '_')
    i=i-1
  
  while j>0:
    row.insert(0, '_')
    column.insert(0, y[j-1])
    j=j-1
  #mem=(pr.memory_info().rss)/1024
  #print(mem)
  return row, column

if __name__=='__main__':
  pr=psutil.Process(os.getpid())
  s_t=time.time()
  f=open(sys.argv[1],'r')
  s=f.readlines()
  gen_str_a,gen_str_b=generate_string(s)
  #print(len(gen_str_a)+len(gen_str_b))
  res=alignment(gen_str_a,gen_str_b)
  a=''.join(res[0])
  b=''.join(res[1])
  cost=0
  for i in range(len(a)):
    if a[i]!='_' and b[i]!='_':
      cost+=alpha[enum[a[i]]][enum[b[i]]]
    else:
      cost+=30
  e_t=time.time()
  #print(e_t-s_t)
  mem=(pr.memory_info().rss)/1024
  #print(mem)
  f=open('output.txt','w')
  if len(a)>=50:
    f.write(a[:50])
    f.write(' ')
    f.write(a[-50:])
    f.write('\n')
    f.write(b[:50])
    f.write(' ')
    f.write(b[-50:])
    f.write('\n')
    f.write(str(float(cost)))
    f.write('\n')
    f.write(str(round((e_t-s_t),4)))
    f.write('\n')
    f.write(str(mem))
  else:
    f.write(a)
    f.write(' ')
    f.write(a)
    f.write('\n')
    f.write(b)
    f.write(' ')
    f.write(b)
    f.write('\n')
    f.write(str(float(cost)))
    f.write('\n')
    f.write(str(round((e_t-s_t),4)))
    f.write('\n')
    f.write(str(mem))
  f.close()