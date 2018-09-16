#coding: utf-8
__author__ = 'Murphy'

import pandas as pd
from sklearn.externals import joblib
from pandas import Series, DataFrame
import numpy as np
import scipy
import matplotlib.pyplot as plt
import sklearn
import time
# import seaborn as sns
from scipy import stats
from sklearn.svm import LinearSVC
from sklearn.utils import shuffle
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_fscore_support
from sklearn.cross_validation import train_test_split


def run():
    df = pd.read_table('features.txt', sep='\t')
    X = df.iloc[:,:-1]
    y = df.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
    print X_test
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    joblib.dump(lr, 'model/lr.pkl')
    #测试集验证
    y_pred_lr = lr.predict_proba(X_test)[:, 1]
    y_pred_lr_c = lr.predict(X_test)
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_pred_lr)
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred_lr_c)

    '''
    # 画图
    plt.figure(1)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr_lr, tpr_lr, label='LR')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.show()
    '''

def pred(test_file, model_file):
    model = joblib.load(model_file)
    df = pd.read_table(test_file, sep='\t', header=None)
    X = df.iloc[:, 2:]
    result = model.predict(X)
    # 将预测结果写入特征文件结尾一列
    outfile = open('features_wiki_result.txt', 'w')
    cnt = 0
    for line in open("features_wiki.txt", 'r'):
        outfile.write(line.strip()+'\t'+str(result[cnt])+'\n') 
        cnt += 1
    outfile.close()

if __name__ == "__main__":
    # run()
    pred('features_wiki.txt', 'model/lr.pkl')
    
