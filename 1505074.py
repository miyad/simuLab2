from scipy import stats
import numpy as np
n = int(input("Enter how many numbers: "))
z = 1505074
mod = 2**31
rand_set = []
for i in range(n):
    z = (65539*z) % mod
    rand_set.append(z/mod)
#print(rand_set)

def uniformity_test(k,alpha):
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
        print("rejected for alpha = ",alpha, " k = ",k)
    else:
        print("accepted for alpha = ",alpha, " k = ",k)


q_list = [0.25,0.5,0.75,0.9,0.95,0.975,0.99]
k_list = [5, 10, 15, 20, 25, 30, 35]
def call_unifromity():
    for q in q_list:
        for k in k_list:
            uniformity_test(k,q)
#call_unifromity()

def serial_test(k,d):
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
    print(index)
    for i in range(int(n/d)):
        cur_d = []
        for j in range(d):
            print(rand_set[i*d+j],end=',')
            cur_d.append(rand_set[i*d+j])
        
        tmp_index = [0]*d
        for i in range(d):
            for j in range(k):
                if cur_d[i] >=j*(1/k) and cur_d[i]<= (j+1)*(1/k):
                    tmp_index[i] = j
        dictionary[tuple(tmp_index)]+=1
    print(dictionary)
    chi_squared = 0
    term = n/(k**d)
    for i in dictionary:
        print(dictionary[i])
        chi_squared = chi_squared + (d*dictionary[i]-term)**2
    chi_squared = chi_squared/(term)
    print(chi_squared)
    print(stats.chi2.ppf(q=1-0.5,df=k**d-1))
serial_test(3,2)





