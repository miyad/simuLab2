from scipy import stats
import numpy as np
'''
Code to generate chi-square values where q are the levels and df is the degrees of freedom.
'''
q_list = [0.25,0.5,0.75,0.9,0.95,0.975,0.99]

for df in range(1,20):
    st = ""
    for q in q_list:
        a = stats.chi2.ppf(q=q,df=df)
        st = st + str(a) + " "

    print("________",st)

'''
Code to generate upper q critical point of the normal distribution
'''
print(stats.norm.ppf(q=0.95))


dictionary = {}
a = [2,2,3]
a = tuple(a)
print(a)
dictionary[a] = 1
dictionary[a]+=2

print(dictionary[a])