#import required libraries
from flask import Flask, request, jsonify,render_template,redirect
import pandas as pd
import category_encoders as ce
import openpyxl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier,AdaBoostClassifier
from sklearn.ensemble import GradientBoostingRegressor,AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score,r2_score
from sklearn.preprocessing import StandardScaler

#create an object of flask
app = Flask(__name__)

#Initial Page HI
@app.route('/hi', methods=['GET','POST'])
def hi():
   return render_template("inputs.html")


#input Page
@app.route('/inputs', methods=['GET','POST'])
def hello():
   
   #fetching the choice for regression or classification
   choice=request.form.getlist('choice[]')
   print(choice) 

   #if it is classfication then redirect to classification page else regression
   if 'Classification' in choice:
       return render_template("classi.html")
   else:
       return render_template("reg.html")


#for Regression
@app.route('/regression', methods=['GET','POST'])
def regressor():
    #fetch the input file from the html page 
    file = request.files['file']

    #fetch the output variable from the user, as we have used forms in order to take the inputs so we use request.forms
    target_col=request.form['outputcol']
    
    #For fetching the options we need to use getlist. ie the options get stored in the form of list
    option=request.form.getlist('options[]')
    print(option)

    #Cheching the extension of the file 
    filename=file.filename
    print(filename)
    ext=filename.split('.')[1]
    print(ext)
    if ext=='csv':
        df = pd.read_csv(file)
    elif ext=='xlsx':
        df = pd.read_excel(file)
    
    #Creating a Dictonary which automatically appends all the selected alg as objects and not as simple strings
    models={}
    for each in option:
        if each=='LinearRegression()':
            lr=LinearRegression()
            models.update({'1':lr})
        elif each=='RandomForestRegressor()':
            rr=RandomForestRegressor()
            models.update({'2':rr})
        elif each=='DecisionTreeRegressor()':
            dt=DecisionTreeRegressor()
            models.update({'3':dt})
        elif each=='GradientBoostingRegressor()':
            gb=GradientBoostingRegressor()
            models.update({'4':gb})
        elif each=='AdaBoostRegressor()':
            ada=AdaBoostRegressor()
            models.update({'5':ada})
        elif each=='KNeighborsRegressor()':
            kn=KNeighborsRegressor()
            models.update({'6':kn})
        elif each=='svr()':
            sm=svm.SVR()
            models.update({'7':sm})


    # Perform machine learning algorithm
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    #code for itrating through the dataset columns and checking the datatpyes 
    #of each columns and if its object then store it in the list
    col=[]
    for each in df.columns:
        if df[each].dtype=='object':
            col.append(each)

    print(col)

     #fetching the response of textbox of "is the dataset contain string?"
    strcol=request.form['strcol']

    #checking if the response is yes or no for doing the encoding if the dataset contain string value
    if strcol=='Yes' or strcol=='yes' and df[target_col].dtype=='object':
        col.remove(target_col)
        encoder=ce.OrdinalEncoder(cols=col)
        X_train=encoder.fit_transform(X_train)
        X_test=encoder.transform(X_test)
    else:
        encoder=ce.OrdinalEncoder(cols=col)
        X_train=encoder.fit_transform(X_train)
        X_test=encoder.transform(X_test)

    
    #fetching the response of textbox of "is the dataset require standard scaling?"
    std_scale=request.form['standarscale']

    #checking if the response is yes or no for doing the SatndadScaling if Required
    if std_scale=='yes' or std_scale=='Yes':
        scaler=StandardScaler() 
        X_train=scaler.fit_transform(X_train)
        X_test=scaler.transform(X_test)
    
    print(X_train)


    #automation code which itratively fetch the algoriths from the dictonary and generates the accuracies accordingly
    acc=[]
    for i in range(len(list(models))):
        model=list(models.values())[i]
        model.fit(X_train, y_train)
        ypred=model.predict(X_test)
        accuracy = r2_score(y_test, ypred)*100
        rounded=round(accuracy,2)
        acc.append(rounded) #These rounded accuracies are stored in the list for further simplification in order to display it precisely
        
    print(acc)

    #Calculating Average Accuracy
    temp=0
    for i in range(len(option)):
        temp+= acc[i]
    avg=temp/len(option)
    roundavg=round(avg,2)

    #Generating a dictonary which automatically appends all the selected algorithms and their corresponding accuracies as a key value pair.
    dict={}
    for i in range(len(option)):
        dict.update({option[i]:acc[i]})
    print(dict)
    
    #Sorting the accuracies top to bottom
    sorted_acc=sorted(dict.items(),key=lambda item: item[1], reverse=True)

    #Sending the Sorted accuracies and avg accuracy to the output page
    return render_template('regoutput.html', accur=sorted_acc, avgacc=roundavg)


#for Classifications
@app.route('/classification', methods=['GET','POST'])
def classify():
    #fetch the input file from the html page 
    file = request.files['file']

    #fetch the output variable from the user, as we have used forms in order to take the inputs so we use request.forms
    target_col=request.form['outputcol']
    
    #For fetching the options we need to use getlist. ie the options get stored in the form of list
    option=request.form.getlist('options[]')
    print(option)

    #Cheching the extension of the file 
    filename=file.filename
    print(filename)
    ext=filename.split('.')[1]
    print(ext)
    if ext=='csv':
        df = pd.read_csv(file)
    elif ext=='xlsx':
        df = pd.read_excel(file)
    
    #Creating a Dictonary which automatically appends all the selected alg as objects and not as simple strings
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
        elif each=='GradientBoostingClassifier()':
            gb=GradientBoostingClassifier()
            models.update({'4':gb})
        elif each=='AdaBoostClassifier()':
            ada=AdaBoostClassifier()
            models.update({'5':ada})
        elif each=='KNeighborsClassifier()':
            kn=KNeighborsClassifier()
            models.update({'6':kn})
        elif each=='svm()':
            sm=svm.SVC()
            models.update({'7':sm})


    # Perform machine learning algorithm (example: Random Forest Classifier)
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #code for itrating through the dataset columns and checking the datatpyes 
    #of each columns and if its object then store it in the list
    col=[]
    for each in df.columns:
        if df[each].dtype=='object':
            col.append(each)

    print(col)

     #fetching the response of textbox of "is the dataset contain string?"
    strcol=request.form['strcol']

    #checking if the response is yes or no for doing the encoding if the dataset contain string value
    if strcol=='Yes' or strcol=='yes' and df[target_col].dtype=='object':
        col.remove(target_col)
        encoder=ce.OrdinalEncoder(cols=col)
        X_train=encoder.fit_transform(X_train)
        X_test=encoder.transform(X_test)
    else:
        encoder=ce.OrdinalEncoder(cols=col)
        X_train=encoder.fit_transform(X_train)
        X_test=encoder.transform(X_test)

    
    #fetching the response of textbox of "is the dataset require standard scaling?"
    std_scale=request.form['standarscale']

    #checking if the response is yes or no for doing the SatndadScaling if Required
    if std_scale=='yes' or std_scale=='Yes':
        scaler=StandardScaler() 
        X_train=scaler.fit_transform(X_train)
        X_test=scaler.transform(X_test)
    
    print(X_train)

    #automation code which itratively fetch the algoriths from the dictonary and generates the accuracies accordingly
    acc=[]
    for i in range(len(list(models))):
        model=list(models.values())[i]
        model.fit(X_train, y_train)
        ypred=model.predict(X_test)
        accuracy = accuracy_score(y_test, ypred)*100
        rounded=round(accuracy,2)
        acc.append(rounded) #These rounded accuracies are stored in the list for further simplification in order to display it precisely
        
    print(acc)

    #Calculating Average Accuracy
    temp=0
    for i in range(len(option)):
        temp+= acc[i]
    avg=temp/len(option)
    roundavg=round(avg,2)

    #Generating a dictonary which automatically appends all the selected algorithms and their corresponding accuracies as a key value pair.
    dict={}
    for i in range(len(option)):
        dict.update({option[i]:acc[i]})
    print(dict)
    
    #Sorting the accuracies top to bottom
    sorted_acc=sorted(dict.items(),key=lambda item: item[1], reverse=True)

    #Sending the Sorted accuracies and avg accuracy to the output page
    return render_template('classioutput.html', accur=sorted_acc , avgacc=roundavg)


if __name__ == '__main__':
    app.run(debug=True)