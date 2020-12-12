from scipy import stats
import numpy as np
import csv
import math
def return_row(file):
    f = open(file,'r')
    usable = csv.reader(f)
    arr = []
    for j in usable:
        for k in j:
            a = list(map(float,k.split()))
            arr.append(a)
    return arr

def generate_random(n):
    z = 1505074
    mod = 2**31
    rand_set = []
    for i in range(n):
        z = (65539*z) % mod
        rand_set.append(z/mod)
    return rand_set
#print(rand_set)

def uniformity_test(k,alpha,rand_set):
    n = len(rand_set)
    interval_frequency = []
    for i in range(k):
        interval_frequency.append(0)
    for i in rand_set:
        for j in range(k):
            if i >= j*(1/k) and i<= (j+1)*(1/k):
                interval_frequency[j]+=1
                break
    sum = 0
    ratio = n/k
    for i in interval_frequency:
        sum = sum + (i-ratio)**2
    chi_squared = sum / ratio
    print(chi_squared)
    chi2 = stats.chi2.ppf(q=1-alpha,df = k-1)
    print("chi2 = ",chi2)
    if chi_squared > chi2:
        print("rejected for n = ",n, " k = ",k)
    else:
        print("accepted for n = ",n, " k = ",k)

n_set = [20,500,4000,10000]
print("____________Uniformity Test:________________")
for n in n_set:
    rand_set = generate_random(n)
    uniformity_test(10,0.1,rand_set=rand_set)
    uniformity_test(20,0.1,rand_set)
"""
n = int(input("Enter how many numbers: "))
rand_set = generate_random(n)
k = int(input("Enter value of k: "))
alpha = float(input("Enter value of alpha: "))
uniformity_test(k,alpha,rand_set)

"""

q_list = [0.25,0.5,0.75,0.9,0.95,0.975,0.99]
k_list = [5, 10, 15, 20, 25, 30, 35]
def call_unifromity():
    for q in q_list:
        for k in k_list:
            uniformity_test(k,q,rand_set)
#call_unifromity()

def serial_test(k,d,alpha,rand_set):
    dictionary = {}
    index = []
    single_tuple = [0]*d
    while True:
        tmp_tuple = np.zeros(d)
        for i in range(d):
            tmp_tuple[i] = int(single_tuple[i])
            
        index.append(tuple(tmp_tuple))
        go_out = False
        ind_d = 0
        while single_tuple[ind_d] == k-1:
            ind_d+=1
            if ind_d == d:
                break
        if ind_d == d:
            break
        single_tuple[ind_d]+=1
        for i in range(ind_d):
            single_tuple[i] = 0
    for each_tuple in index:
        dictionary[each_tuple] = 0 #f val
    #print(index)
    for i in range(int(n/d)):
        cur_d = []
        for j in range(d):
            #print(rand_set[i*d+j],end=',')
            cur_d.append(rand_set[i*d+j])
        
        tmp_index = [0]*d
        for i in range(d):
            for j in range(k):
                if cur_d[i] >=j*(1/k) and cur_d[i]<= (j+1)*(1/k):
                    tmp_index[i] = j
        dictionary[tuple(tmp_index)]+=1
    #print(dictionary)
    chi_squared = 0
    term = n/(k**d)
    for i in dictionary:
        #print(dictionary[i])
        chi_squared = chi_squared + (dictionary[i]-term)**2
    chi_squared = chi_squared/(term)
    print(chi_squared)
    chi_2 = stats.chi2.ppf(q=1-alpha,df=k**d-1)
    print("chi2 = ",chi_2)
    if chi_squared > chi_2:
        print("rejected for n = ",n," k = ",k, " d = ",d)
    else:
        print("accepted for n = ",n, " k = ",k, " d = ",d)
#serial_test(3,2)


print("___________________Serial Test______________________________")

k_set = [4,8]
d_set = [2,3]
for n in n_set:
    rand_set = generate_random(n)
    for k in k_set:
        for d in d_set:
            serial_test(k,d,0.1,rand_set)

"""
n = int(input("Enter How many numbers: "))
k = int(input("enter value of k: "))
d = int(input("enter value of d: "))
alpha = float(input("Enter value of alpha : "))
rand_set = generate_random(n)
serial_test(k,d,alpha,rand_set)
"""


def run_test(alpha,rand_set):
    a = return_row('a.txt')
    b = [1/6, 5/24, 11/120, 19/720, 29/5040, 1/840]
    r = [0,0,0,0,0,0,0]
    run_len = 0
    i = 0
    while i < n:
        j = i
        run_len = 1
        if j+1 < n:
            while rand_set[j]<=rand_set[j+1]:
                run_len += 1
                j = j + 1
                if j+1 >=n:
                    break
        r[min(run_len,6)]+=1
        i = j+1
    
    #print(r)
    #print(b)
    #print(a)
    R = 0
    for i in range(1,7):
        for j in range(1,7):
            R = R + a[i-1][j-1]*(r[i]-n*b[i-1])*(r[j]-n*b[j-1])
    R = R / n
    if R > stats.chi2.ppf(q=1-alpha,df=6):
        print("rejected for n = ",n)
    else:
        print("accepted for n = ", n)

#run_test(0.1)
print("__________________________Run Test__________________________")
for n in n_set:
    rand_set = generate_random(n)
    run_test(0.1,rand_set)

"""
n = int(input("Enter How many numbers: "))
rand_set = generate_random(n)
alpha = float(input("Enter value of alpha: "))
run_test(alpha=alpha,rand_set=rand_set)

"""
def corelation_test(j,alpha,rand_set):
    n = len(rand_set)
    h = int(-1+(n-1)/j)
    roe_j = 0
    for k in range(h+1):
        roe_j = roe_j + rand_set[k*j]*rand_set[(k+1)*j]
    roe_j = roe_j*12/(h+1)-3
    var = (13*h+7)/((h+1)**2)
    A_j = roe_j/math.sqrt(var)
    z_alpha = stats.norm.ppf(q=1-alpha/2)
    if abs(A_j)>z_alpha:
        print("rejected for n = ",n," j = ",j)
    else:
        print("accepted for n = ",n," j = ",j)
print("_____________________Co-Relation Test_________________________")
j_set = [1,3,5]
for n in n_set:
    rand_set = generate_random(n)
    for j in j_set:
        corelation_test(j,0.1,rand_set)
"""
n = int(input("Enter How many numbers: "))
j = int(input("Enter value of j: "))
alpha = float(input("Enter value of alpha: "))
rand_set = generate_random(n)
corelation_test(j,alpha,rand_set)
"""





