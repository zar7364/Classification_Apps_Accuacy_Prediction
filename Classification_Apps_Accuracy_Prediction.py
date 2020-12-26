import streamlit as st
from sklearn import datasets
import numpy as np

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score


st.title("Hallo ini Aplikasi untuk Machine Learning")
st.write("Oleh : Nezar Abdilah Prakasa")



dataset_name=st.sidebar.selectbox("Data Set yang digunakan",("Iris","Breast Cancer","Wine dataset"))
st.write("Pilih datasetmu di sidebar sebelah kiri")
st.write("Kamu memlih dataset", dataset_name)

classifier_name=st.sidebar.selectbox("Metode Klasifikasi yang digunakan",("KNN","SVN","Random Forest"))

def get_dataset(dataset_name):
    if dataset_name=='Iris':
        data=datasets.load_iris()
    elif dataset_name=='Breast Cancer':
        data=datasets.load_breast_cancer()
    else:
        data=datasets.load_wine()
    X=data.data
    y=data.target
    return X,y

X,y=get_dataset(dataset_name)
st.write("Shape of Dataset", X.shape)
st.write("Number of Classes", len(np.unique(y)))


def add_parameter_ui(clf_name):
    params = dict()
    if clf_name == "KNN":
        K = st.sidebar.slider("K", 1, 15)
        params["K"] = K
    elif clf_name == "SVM":
        C = st.sidebar.slider("C", 0.01, 10.0)
        params["C"]=C
    else:
        max_depth=st.sidebar.slider("max_depth",2,15)
        n_estimators = st.sidebar.slider("n_estimators",1,100)
        params["max_depth"]=max_depth
        params["n_estimators"]=n_estimators
    return params
params=add_parameter_ui(classifier_name)


def get_classifier(clf_name, params) :
    clf = None
    if clf_name=='SVM':
        clf=SVM(C=params['C'])
    elif clf_name=="KNN":
        clf=KNeighborsClassifier(n_neighbors=params['K'])
    else:
         clf=RandomForestClassifier(max_depth=params["max_depth"],n_estimators=params["n_estimators"],random_state=1234)
    return clf

clf=get_classifier(classifier_name,params)


#CLASSIFICATION

X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.1, random_state=12)

clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)

acc=accuracy_score(y_test,y_pred)


st.write(f'classifier={classifier_name}')
st.write(f'Accuracy=',acc)


#Plot Dataset
#Project Data into 2 primary principal components

pca=PCA(2)
X_projected=pca.fit_transform(X)


x1=X_projected[:,0]
x2=X_projected[:,1]


fig=plt.figure()
plt.scatter(x1,x2,
            c=y,
            alpha=0.8,cmap='viridis')

plt.xlabel=("Principal Component 1")
plt.ylabel=("Principal Component 2")
plt.colorbar()

#Show Plot
st.pyplot(fig)
