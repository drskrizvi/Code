#Final Supervised -  all algorithms
#Importing required libraries

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Input, Dense
from keras import regularizers
from keras.models import Model, load_model
from keras.callbacks import ModelCheckpoint
from  tensorflow.keras.layers import *
from tensorflow.keras.models import Model
from keras import models
from keras import layers
from keras.models import Model, load_model
from keras.layers import Dense, Multiply, Concatenate, Maximum, Flatten, Activation, RepeatVector, Permute, Dropout, BatchNormalization, GlobalAveragePooling2D
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import copy
from PIL import Image
import tensorflow as tf
from sklearn import tree
from keras import models
from keras import layers
from keras import *
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn import model_selection
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
import keras
from keras_attention import self_attention
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler
#import seaborn as sns
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
import scikitplot as skplt
#sns.set(font_scale=1)

train = pd.read_csv("train2.csv")
test = pd.read_csv("test.csv")
val = pd.read_csv("val.csv")

train_label = train['label'].values
train_data = train.drop(['label'], axis = 1)

test_label = test['label'].values
test_data = test.drop(['label'], axis = 1)

val_label = val['label'].values
val_data = val.drop(['label'], axis = 1)

scaler = MinMaxScaler()
scaler.fit(train_data)
train_data = scaler.transform(train_data)
test_data = scaler.transform(test_data)

val_data = scaler.transform(val_data)
#########################################################################################################################
                                           # FUNCTIONS FOR VISUALIZATION
#########################################################################################################################
# Helper function for visualization
def visualize_cumulative_gain(classifier_object, test_data = test_data, test_label  = test_label):
    target_prob = classifier_object.predict_proba(test_data)
    skplt.metrics.plot_cumulative_gain(test_label, target_prob)
    plt.show()


def visualize_lift_curve(classifier_object, test_data = test_data, test_label  = test_label):
    target_prob = classifier_object.predict_proba(test_data)
    skplt.metrics.plot_lift_curve(test_label, target_prob)
    plt.show()


def visualize_ks_statistics(classifier_object, test_data = test_data, test_label  = test_label):
    target_prob = classifier_object.predict_proba(test_data)
    skplt.metrics.plot_ks_statistic(test_label, target_prob)
    plt.show()


def precision_recall(classifier_object, test_data = test_data, test_label  = test_label):
    probs = classifier_object.predict_proba(test_data)
    probs = probs[:, 1]
    yhat = classifier_object.predict(test_data)
    precision, recall, thresholds = precision_recall_curve(test_label, probs)
    f1 = f1_score(test_label, yhat)
    # auc = auc(recall, precision)
    ap = average_precision_score(test_label, probs)
    print('F1 Score %.4f \nAverage Precision %.4f' % (f1, ap))
    #pyplot.plot([0, 1], [0.5, 0.5], linestyle='--')
    #pyplot.plot(recall, precision, marker='.')
    #pyplot.title("Precision - Recall")
    #pyplot.show()


def ROC_curve(classifier_object, test_data = test_data, test_label  = test_label):
    probs = classifier_object.predict_proba(test_data)
    probs = probs[:, 1]
    auc = roc_auc_score(test_label, probs)
    print('AUC %.4f' % auc)
    fpr, tpr, thresholds = roc_curve(test_label, probs)
    #pyplot.plot([0, 1], [0, 1], linestyle='--')
    #pyplot.plot(fpr, tpr, marker='.')
    #pyplot.xlabel('False Positive Rate')
    #pyplot.ylabel('True Positive Rate')
    #pyplot.title("ROC Curve")
    #pyplot.show()
    return fpr, tpr


def Confusion_Matrix(classifier_object, test_data = test_data):
     result = classifier_object.predict(test_data)
     # skplt.metrics.plot_confusion_matrix(test_label, result, normalize=True)
     # plt.show()
     # pyplot.title("Confusion Matrix")
     # pyplot.xlabel('Predicted Label')
     # pyplot.ylabel('True Label')
     # pyplot.show()


def Classifiction_report(classifier_object, test_data = test_data,  test_label  = test_label):
    result = classifier_object.predict(test_data)
    print(classification_report(test_label, result))


#########################################################################################################################
                                           # CLASSIFICATION ALGOS
#########################################################################################################################

# RANDOM FOREST #

#Model generation
rf_model = RandomForestClassifier(n_estimators=10, max_depth=1, random_state=0)

#Training = fitting the algorithm on the dataset
rf_model.fit(train_data,train_label)

#model.predict()
rf_prediction = rf_model.predict(test_data)
score = accuracy_score(test_label ,rf_prediction)
print("The Accuracy on Test Data = {}".format(score))
rf_val_prediction = rf_model.predict(val_data)
val_score = accuracy_score(val_label ,rf_val_prediction)

print("Accuracy - Random Forest")
print("Train Data ", rf_model.score(train_data , train_label) * 100)
print("Test Data ",rf_model.score(test_data , test_label) * 100)
print("Validation Data ",rf_model.score(val_data , val_label) * 100)

print(f"Test Metrices")
Confusion_Matrix(rf_model,test_data = test_data)
precision_recall(rf_model,test_data = test_data)
rf_fpr, rf_tpr = ROC_curve(rf_model,test_data = test_data)
Classifiction_report(rf_model,test_data = test_data)

print(f"Validation Metrices")
Confusion_Matrix(rf_model,test_data = val_data)
precision_recall(rf_model,test_data = val_data,  test_label  = val_label)
val_rf_fpr, val_rf_tpr = ROC_curve(rf_model,test_data = val_data,  test_label  = val_label)
Classifiction_report(rf_model,test_data = val_data,  test_label  = val_label)
# visualize_ks_statistics(rf_model)
# visualize_lift_curve(rf_model)
# visualize_cumulative_gain(rf_model)

# SUPPORT VECTOR MACHINE(SVM) #

#Model generation
svm_model =SVC(gamma='auto',probability=True)
#Training = fitting the algorithm on the dataset
svm_model.fit(train_data,train_label)


#Accuracy of trainig and testing data(result accuracy)
print("Accuracy - Support Vector Machine (SVM)")
print("Train Data",svm_model.score(train_data , train_label) * 100)
print("Test Data ",svm_model.score(test_data , test_label) * 100)

# EVALUATION MEASURES VISUALIZATION OF SVM #
Confusion_Matrix(svm_model)
precision_recall(svm_model)
svm_fpr, svm_tpr = ROC_curve(svm_model)
Classifiction_report(svm_model)
#visualize_ks_statistics(svm_model)
#visualize_lift_curve(svm_model)
#visualize_cumulative_gain(svm_model)


# Gradient Boosting #

#Model generation
grad_boost_model = GradientBoostingClassifier(criterion='friedman_mse', init=None, learning_rate=0.001, loss='deviance', max_depth=20, max_features=None, max_leaf_nodes=2,
min_impurity_split=1e-07, min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.001)
#Training = fitting the algorithm on the dataset
grad_boost_model.fit(train_data,train_label)

#Accuracy of trainig and testing data(result accuracy)
print("Accuracy - Gradient Boost")
print("Train Data",grad_boost_model.score(train_data , train_label) * 100)
print("Test Data ",grad_boost_model.score(test_data , test_label) * 100)

#EVALUATION MEASURES VISUALIZATION OF GRADIENT BOOSTING ALGORITHM #

Confusion_Matrix(grad_boost_model)
precision_recall(grad_boost_model)
gb_fpr, gb_tpr = ROC_curve(grad_boost_model)
Classifiction_report(grad_boost_model)

#visualize_ks_statistics(grad_boost_model)
#visualize_lift_curve(grad_boost_model)
#visualize_cumulative_gain(grad_boost_model)

# ADABOOST #

#Model generation
ada_boost_model = AdaBoostClassifier(algorithm='SAMME',n_estimators=5,random_state=0,learning_rate=0.001)
#Training = fitting the algorithm on the dataset
ada_boost_model.fit(train_data,train_label)

#Accuracy of trainig and testing data(result accuracy)
print("Accuracy - Ada Boost")
print("Train Data",ada_boost_model.score(train_data , train_label) * 100)
print("Test Data ",ada_boost_model.score(test_data , test_label) * 100)

#EVALUATION MEASURES VISUALIZATION OF ADABOOST ALGORITHM #

Confusion_Matrix(ada_boost_model)
precision_recall(ada_boost_model)
ab_fpr, ab_tpr = ROC_curve(ada_boost_model)
Classifiction_report(ada_boost_model)

#visualize_ks_statistics(ada_boost_model)
#visualize_lift_curve(ada_boost_model)
#visualize_cumulative_gain(ada_boost_model)

# NAIVE BAYES #

#Model generation
naive_bayes_model = GaussianNB()
#Training = fitting the algorithm on the dataset
naive_bayes_model.fit(train_data,train_label)

#Accuracy of trainig and testing data(result accuracy)
print("Accuracy - Naive Bayes")
print("Train Data",naive_bayes_model.score(train_data , train_label) * 100)
print("Test Data ",naive_bayes_model.score(test_data , test_label) * 100)

#EVALUATION MEASURES VISUALIZATION OF NAIVE BAYES ALGORITHM #

Confusion_Matrix(naive_bayes_model)
precision_recall(naive_bayes_model)
nb_fpr, nb_tpr = ROC_curve(naive_bayes_model)
Classifiction_report(naive_bayes_model)

#visualize_ks_statistics(naive_bayes_model)
#visualize_lift_curve(naive_bayes_model)
#visualize_cumulative_gain(naive_bayes_model)

# KNN(N=5) #
#Model generation
knn_model = KNeighborsClassifier(n_neighbors=5)
#Training = fitting the algorithm on the dataset
knn_model.fit(train_data,train_label)

print("Accuracy - KNN")
print("Train Data",knn_model.score(train_data , train_label) * 100)
print("Test Data ",knn_model.score(test_data , test_label) * 100)


# EVALUATION MEASURES VISUALIZATION OF KNN #

Confusion_Matrix(knn_model)
precision_recall(knn_model)
knn_fpr, knn_tpr = ROC_curve(knn_model)
Classifiction_report(knn_model)
#precision_recall(knn_model)
#visualize_lift_curve(knn_model)
#visualize_cumulative_gain(knn_model)

########################################################################################################################
                                           # MLP - NN
#########################################################################################################################

# Simple Neural Network
input_dim = train_data.shape[1]
input_layer = Input(shape=(input_dim, ))

#Before
x = Dense(38,  activation = 'relu')(input_layer)

atten_prob1 = Dense(38,  activation = 'sigmoid', name ='atten_prob1')(x)

atten_prob2 = Dense(38,  activation = 'relu', name ='atten_prob2')(x)

max = Maximum()([atten_prob1,atten_prob2])

x = Multiply()([max,x])
#atten_mul = Multiply()([atten_prob,x])
x = Dense(13,  activation = 'relu')(x)

x = Dense(1, name = "final", activation = 'sigmoid')(x)

#After
#x = Dense(39,  activation = 'relu')(input_layer)
#x = Dense(13,  activation = 'relu')(x)
#x = Dense(13,  activation = 'relu')(x)
#atten_prob = Dense(13,  activation = 'relu', name ='atten_prob')(x)
#atten_mul = Multiply()([atten_prob,x])
#x = Dense(1, name = "final", activation = 'sigmoid')(atten_mul)


model_mlp = Model(inputs=input_layer, outputs = x)
nb_epoch = 62
batch_size = 32
model_mlp.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath="mlp_nn.h5", verbose=0, save_best_only=True)
history = model_mlp.fit(train_data, train_label, epochs=nb_epoch, batch_size=batch_size, shuffle=True, validation_data=(val_data, val_label), verbose=1, callbacks=[checkpointer]).history
val_pred_label = model_mlp.predict(val_data)
pred_label = model_mlp.predict(test_data)
prediction = copy.deepcopy(pred_label)
val_prediction = copy.deepcopy(val_pred_label)

print(np.unique(prediction))
print(np.min(pred_label))
# training stats
print(history.keys())
plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss', fontname="Arial",fontweight="bold",fontsize=12)
plt.xlabel('Number of Epochs', fontname="Arial",fontweight="bold",fontsize=12)
plt.legend(['Train', 'Validation'], loc='center right')
plt.grid()
plt.show()
#plt.savefig(str(model_mlp.name)+"hello.png")


print(history.keys())
plt.plot(history['acc'])
plt.plot(history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy', fontname="Arial",fontweight="bold", fontsize=12)
plt.xlabel('Number of Epochs', fontname="Arial",fontweight="bold", fontsize=12)
plt.legend(['Train', 'Validation'], loc='center right')
plt.grid()
plt.show()

# Combine plot the training loss and accuracy
# plt.style.use("ggplot")
plt.figure()
N = number_of_epochs_it_ran = len(history['loss'])
plt.plot(np.arange(0, N), history["loss"], label="Training_Loss")
plt.plot(np.arange(0, N), history["val_loss"], label="Validation_Loss")
plt.plot(np.arange(0, N), history["acc"], label="Training_Accuracy")
plt.plot(np.arange(0, N), history["val_acc"], label="Validation_Accuracy")
plt.title("Training Accuracy and Loss")
plt.xlabel("Number of Epochs", fontname="Arial",fontweight="bold", fontsize=12)
plt.ylabel("Accuracy/Loss",fontname="Arial",fontweight="bold", fontsize=12)
plt.legend(loc="center right")
plt.grid()
plt.savefig('history_exp1')




print("Accuracy - Neural Network")
print("Train Data %0.04f" % np.max(history['acc']))

I = pred_label >= 0.5
pred_label[I] = 1

I = pred_label < 0.5
pred_label[I] = 0

print("Test Data %0.04f" %  accuracy_score(test_label, pred_label))

#Confusion_Matrix(model_mlp)
print(confusion_matrix(test_label, pred_label))
skplt.metrics.plot_confusion_matrix(test_label, pred_label, normalize=True)
pyplot.title("Confusion Matrix")
pyplot.xlabel('Predicted Label')
pyplot.ylabel('True Label')
pyplot.grid()
pyplot.show()


#precision_recall(model_mlp)
precision, recall, thresholds = precision_recall_curve(test_label, prediction)
# auc = auc(recall, precision)
f1 = f1_score(test_label, pred_label)
ap = average_precision_score(test_label, pred_label)
print('F1 Score %.4f \nAverage Precision %.4f' % (f1, ap))
pyplot.plot([0, 1], [0.5, 0.5], linestyle='--')
pyplot.plot(recall, precision, marker='.')
pyplot.title("Precision - Recall")
pyplot.grid()
pyplot.show()

#ROC_curve(model_mlp)
auc = roc_auc_score(test_label, prediction)
print('AUC: %.4f' % auc)
nn_fpr, nn_tpr, thresholds = roc_curve(test_label, prediction)
# pyplot.plot([0, 1], [0, 1], linestyle='--')
# pyplot.plot(fpr, tpr, marker='.')
# pyplot.xlabel('False Positive Rate')
# pyplot.ylabel('True Positive Rate')
# pyplot.title("ROC Curve")
# pyplot.show()

# Combine ROC NN and all
# plt.style.use("ggplot")
plt.figure()
#N = number_of_epochs_it_ran = len(history['loss'])
plt.plot(nn_fpr, nn_tpr , label="PROUD-MAL")
plt.plot(rf_fpr, rf_tpr, label="Random Forest")
plt.plot(svm_fpr, svm_tpr, label="SVM")
plt.plot(gb_fpr, gb_tpr, label="Gradient Boost")
plt.plot(ab_fpr, ab_tpr, label="ADA Boost")
plt.plot(nb_fpr, nb_tpr, label="Naive Bayes")
plt.title("ROC")
plt.xlabel("False Positive Rate",fontname="Arial",fontweight="bold", fontsize=12)
plt.ylabel("True Positive Rate",fontname="Arial",fontweight="bold", fontsize=12)
plt.legend(loc="center right")
plt.grid()
plt.show()


#Classifiction_report(model_mlp)
print(classification_report(test_label, pred_label))

#visualize_ks_statistics(model_mlp)
#skplt.metrics.plot_ks_statistic(test_label, pred_label)
#pyplot.title("KS Statisitcs")
#pyplot.show()

#visualize_lift_curve(model_mlp)
#skplt.metrics.plot_lift_curve(test_label, pred_label)
#pyplot.title("Lift Curve")
#pyplot.show()

#visualize_cumulative_gain(model_mlp)
#skplt.metrics.plot_cumulative_gain(test_label, pred_label)
#pyplot.title("Commulative Gain")
#pyplot.show()


#Diplay all saved images in one plot
#filelist = 'RF_ROC.png', 'SVM_ROC.png','GB_ROC.png', 'AB_ROC.png','NB_ROC.png','MLP_ROC.png'
#x = np.array([np.array(Image.open(fname)) for fname in filelist])
#fig = plt.figure(figsize=(6, 6))
#columns = 3
#rows = 2
#for i in range(0, columns * rows):
#    fig.add_subplot(rows, columns, i+1)
#    fig.subplots_adjust(hspace=0.2, wspace=0.1)
#    plt.imshow(x[i])
#    pyplot.title(filelist[i][:-4])

#plt.show()



##################################################### results for validation  ###############################################
I = val_pred_label >= 0.5
val_pred_label[I] = 1

I = val_pred_label < 0.5
val_pred_label[I] = 0

print("Validation Data %0.04f" %  accuracy_score(val_label, val_pred_label))

#Confusion_Matrix(model_mlp)
print(confusion_matrix(val_label, val_pred_label))
skplt.metrics.plot_confusion_matrix(val_label, val_pred_label, normalize=True)
pyplot.title("Confusion Matrix")
pyplot.xlabel('Predicted Label')
pyplot.ylabel('True Label')
pyplot.grid()
pyplot.show()


#precision_recall(model_mlp)
val_precision, val_recall, thresholds = precision_recall_curve(val_label, val_prediction)
# auc = auc(recall, precision)
val_f1 = f1_score(val_label, val_pred_label)
val_ap = average_precision_score(val_label, val_pred_label)
print('F1 Score %.4f \nAverage Precision %.4f' % (val_f1, val_ap))
pyplot.plot([0, 1], [0.5, 0.5], linestyle='--')
pyplot.plot(val_recall, val_precision, marker='.')
pyplot.title("Precision - Recall")
pyplot.grid()
pyplot.show()

#ROC_curve(model_mlp)
auc = roc_auc_score(val_label, val_prediction)
print('AUC: %.4f' % auc)
val_nn_fpr, val_nn_tpr, thresholds = roc_curve(val_label, val_prediction)
# pyplot.plot([0, 1], [0, 1], linestyle='--')
# pyplot.plot(fpr, tpr, marker='.')
# pyplot.xlabel('False Positive Rate')
# pyplot.ylabel('True Positive Rate')
# pyplot.title("ROC Curve")
# pyplot.show()

# Combine ROC NN and all
# plt.style.use("ggplot")
plt.figure()
#N = number_of_epochs_it_ran = len(history['loss'])
plt.plot(val_nn_fpr, val_nn_tpr , label="PROUD-MAL")
plt.plot(val_rf_fpr, val_rf_tpr, label="Random Forest")
# plt.plot(val_svm_fpr, val_svm_tpr, label="SVM")
# plt.plot(val_gb_fpr, val_gb_tpr, label="Gradient Boost")
# plt.plot(val_ab_fpr, val_ab_tpr, label="ADA Boost")
# plt.plot(val_nb_fpr, val_nb_tpr, label="Naive Bayes")
plt.title("ROC")
plt.xlabel("False Positive Rate",fontname="Arial",fontweight="bold", fontsize=12)
plt.ylabel("True Positive Rate",fontname="Arial",fontweight="bold", fontsize=12)
plt.legend(loc="center right")
plt.grid()
plt.show()


#Classifiction_report(model_mlp)
print(classification_report(val_label, val_pred_label))

#visualize_ks_statistics(model_mlp)
#skplt.metrics.plot_ks_statistic(test_label, pred_label)
#pyplot.title("KS Statisitcs")
#pyplot.show()

#visualize_lift_curve(model_mlp)
#skplt.metrics.plot_lift_curve(test_label, pred_label)
#pyplot.title("Lift Curve")
#pyplot.show()

#visualize_cumulative_gain(model_mlp)
#skplt.metrics.plot_cumulative_gain(test_label, pred_label)
#pyplot.title("Commulative Gain")
#pyplot.show()


#Diplay all saved images in one plot
#filelist = 'RF_ROC.png', 'SVM_ROC.png','GB_ROC.png', 'AB_ROC.png','NB_ROC.png','MLP_ROC.png'
#x = np.array([np.array(Image.open(fname)) for fname in filelist])
#fig = plt.figure(figsize=(6, 6))
#columns = 3
#rows = 2
#for i in range(0, columns * rows):
#    fig.add_subplot(rows, columns, i+1)
#    fig.subplots_adjust(hspace=0.2, wspace=0.1)
#    plt.imshow(x[i])
#    pyplot.title(filelist[i][:-4])

#plt.show()

