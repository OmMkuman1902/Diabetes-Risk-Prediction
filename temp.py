from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import pandas as pd
from sklearn import svm
import category_encoders as ce
'''def modelinit():
    if options[0]=='LogisticRegression()':
            yield 1
    if options[1]=='RandomForestClassifier()':
            yield RandomForestClassifier()

option=['LogisticRegression()','DecisionTreeClassifier()','svm()']
models={}
for each in option:
    if each=='LogisticRegression()':
        lr=LogisticRegression()
        models.update({'1':lr})
    elif each=='RandomForestClassifier()':
        rr=RandomForestClassifier()
        models.update({'2':rr})
    elif each=='DecisionTreeClassifier()':
        dt=DecisionTreeClassifier()
        models.update({'3':dt})
    elif each=='svm()':
        sm=svm.SVC()
        models.update({'4':sm})

print(models)

for i in range(len(list(models))):
            model=list(models.values())[i]
            print(model)
length=len(options)
models={}
for i in range(length):
    modelname=modelinit()
    models.update({i:modelname})
options=['log','rf','dt','svc']
acc=['80','90','50','68']
dict={}
for i in range(len(options)):
    dict.update({options[i]:acc[i]})
print(dict)

#data=pd.DataFrame(dict)
print(dict)


#df=pd.DataFrame(list(dict.items()),columns=['model','acc'])
    #for i in range(len(acc)):
    #table_html=df.to_html(index=False)



acc=[10,10,10]
n=['a','t','d']
temp=0
for i in range(len(n)):
    temp+= acc[i]
avg=temp/len(n)

print(avg)

col=[]
for each in df.columns:
    if df[each].dtype=='object':
        col.append(each)
print(col)'''

col=['abc','xyz']
col.remove('xyz')
print(col)



