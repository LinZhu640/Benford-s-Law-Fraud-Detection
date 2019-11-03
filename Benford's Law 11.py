#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Benford’s law is the nonintuitive fact that the first digit of many measurements is not uniformly distributed, and the first digit “1” appears about 30% of the time!
We could use this law for fraud detection when a potential fraudster is making up a large amount of numbers
'''


# In[ ]:

import pandas as pd
import numpy as np
import math


# In[ ]:


# import dataset
mydata = pd.read_excel('C:/Users/Lin/Documents/DSO562/Assignment/card transactions.xlsx')


# # Data cleaning
# clean categorical dataset


# In[ ]:


'''general text columns cleanning strategy:
1. uppercase all letters
2. remove all symbols
3. check miss spelling
4. words order
'''

data = data.drop_duplicates(subset = 'Product Name')
#contain only letters, space, and number
data['Name_noPunc'] = data['Product Name'].apply(lambda x: re.sub(r'[^a-zA-Z0-9 ]+', '', x))
data['Name_noPunc1'] = data['Name_noPunc'].str.upper()
#split words in a list
data['Name_list'] = data['Name_noPunc1'].apply(lambda x: sorted(x.split()))
#Letter, mark, and order
#convert to hashable objects
data['Name_list1'] = [str(i) for i in data['Name_list']]
data = data[data.duplicated(['Name_list1'],keep=False)].sort_values(by = 'Product Name')
#renumber the items with same name
data['new_number'] = pd.factorize(data['Name_list1'])[0] + 1


# In[ ]:


#drop null value
Merchan = data.dropna(subset = ['Merchnum'])


# In[ ]:


# drop string contain 'FEDEX'
Merchan = Merchan[~Merchan['Merch description'].str.contains('FEDEX')]


# # Benford's Law for MerchanNum

# In[ ]:


#get the first digit and find how different the first difit distribution
#from the Benford's Law distribution
amount = list(Merchan['Amount'].astype('float'))
first = []
for am in amount:
    while am < 1:
        am = am*10
    #int(str(am)[:1])
    first.append(int(str(am)[:1]))


# In[ ]:


Merchan['first'] = first


# In[ ]:


mydict={}
for number in np.unique(Merchan['Merchnum']):
    nu = []
    p = Merchan[Merchan['Merchnum'] == number]
    for digit in p['first']:
        nu.append(digit)
    mydict[number] = nu


# In[ ]:


#count the first digits beginning with either 1 or 2
RR = []
Rs = []
KKey = []
for key in mydict:
    nlow = 0
    for b in mydict[key]:
        if b == 1 or b == 2:
            nlow = nlow + 1
        nhigh = len(mydict[key])-nlow
    if nhigh == 0:
        nhigh = 1
    if nlow == 0:
        nlow = 1
    #measure of unusualness
    R = 1.096*nlow/nhigh
    Rstar = 1+((R-1)/(1+math.exp(-(len(mydict[key])-15)/3)))
    RR.append(R)
    KKey.append(key)
    Rs.append(Rstar)


# In[ ]:


d = {'Card':KKey, 'R':RR, 'Rsta':Rs}
final = pd.DataFrame(d)
final['1/Rsta'] = final.apply(lambda x: 1/x['Rsta'], axis=1)
final['result'] = final.apply(lambda x: max(x['Rsta'],x['1/Rsta']),axis=1)


# In[ ]:


df2=final.sort_values(by='result',ascending = False)


# In[ ]:


df2.to_csv('C:/Users/Lin/Documents/DSO562/Assignment/card Benford.csv')

