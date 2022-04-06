import pandas as pd
import numpy as np
import time
import os
import psutil
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
  #print(s_b)
  for i in range(len(s_a)):
    gen_str_a=gen_str_a[0:s_a[i]+1]+gen_str_a+gen_str_a[s_a[i]+1:]

  for i in range(len(s_b)):
    gen_str_b=gen_str_b[:s_b[i]+1]+gen_str_b+gen_str_b[s_b[i]+1:]
  
  return gen_str_a, gen_str_b

#Dynamic Programming version of the Sequence alignment algorithm
def alignment(x,y):
  m=len(x)
  n=len(y)
  A=np.zeros((m+1,n+1))

  for i in range(m+1):
    A[i][0]=i*delta

  for i in range(n+1):
    A[0][i]=i*delta
  
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
  
  return row, column

#Calculating Forward Space efficient algorithm
def space_efficient_algo(x,y):
  m=len(x)
  n=len(y)
  B=np.zeros((m+1,2))
  for i in range(m+1):
    B[i][0]=i*delta
  for j in range(1,n+1):
    B[0][1]=j*delta
    for i in range(1,m+1):
      B[i][1]=min(alpha[enum[x[i-1]]][enum[y[j-1]]]+B[i-1][0], delta+B[i-1][1],delta+B[i][0])
    if j!=n:
      for i in range(m+1):
        B[i][0]=B[i][1]
        B[i][1]=0
  return B[:,1]

def findq(L, R):
  min_index = -1
  min_sum = np.inf
  R=R[::-1]
  for i in range(len(L)):
    if L[i]+R[i]<min_sum:
        min_sum=L[i]+R[i]
        min_index=i
  return min_index

#Divide and Conquer function
def d_and_c_alignment(x,y):
  row=""
  column=""
  if len(x)<=2 or len(y)<=2:
    r,c=alignment(x,y)
    row, column = map(lambda x: "".join(x), [r, c])

  else:
    m=len(x)
    n=len(y)
    y_mid=(int)(len(y)/2)

    x_mid=findq(space_efficient_algo(x,y[:y_mid]),space_efficient_algo(x[::-1],y[y_mid:][::-1]))
    row_l, column_u = d_and_c_alignment(x[:x_mid], y[:y_mid])
    row_r, column_d= d_and_c_alignment(x[x_mid:], y[y_mid:])
    row = row_l + row_r
    column = column_u + column_d 
    
  return row, column
  
def alignment_func(gen_str_a,gen_str_b):
  #pr=psutil.Process(os.getpid())
  res=d_and_c_alignment(gen_str_a,gen_str_b)
  #mem=(pr.memory_info().rss)/1024
  #print(mem)
  return res

    
if __name__=='__main__':
  pr=psutil.Process(os.getpid())
  s_t=time.time()
  f=open(sys.argv[1],'r')
  s=f.readlines()
  gen_str_a,gen_str_b=generate_string(s)
  #print(len(gen_str_a)+len(gen_str_b))
  res=d_and_c_alignment(gen_str_a,gen_str_b)
  a=res[0]
  b=res[1]
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