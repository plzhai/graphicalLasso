# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 15:51:53 2019

@author: plzhai
"""


print(__doc__)
from sklearn import preprocessing
from sklearn import linear_model

import numpy as np


class graphicalLasso:
    # X is data (n_samples*n_features)
    # A is precision matrix (n_features*n_features)
    # S is covariance matrix (n_features*n_features)
    # rho is regularizer
    
    # initialization
    def __init__(self, rho=0.1, maxItr=1e+3, tol=1e-2):

        self.rho=rho
        self.maxItr=int(maxItr)
        self.tol=tol
        self.scaler=None

        
    # graphical lasso    
    def fit(self,X):
        n_samples,n_features=X.shape[0],X.shape[1]
        
        # sample covariance S = X'X/n;
        self.scaler=preprocessing.StandardScaler().fit(X)
        self.X=self.scaler.transform(X)
        
        S=self.X.T.dot(self.X)/n_samples
        
        # initialization of precision matrix;
        A=np.linalg.pinv(S)
        A_old=A
        invA=S
        
        # graphical lasso can be seperated into many single lasso optimization;
        # the problem can be formulated as: min{log detA -tr SA - rho|A|}
        clf=linear_model.Lasso(alpha=self.rho)
        # block cordinate descent
        for i in range(self.maxItr):
            for j in range(n_features):
                R,s,sii=self.__get(S)
                W=self.__get(invA)[0]
                L=self.__get(A)[0]
                
                # find sigma
                sigma=sii+self.rho            
                U,D,V=np.linalg.svd(W)
                W_half=U.dot(np.diag(np.sqrt(D)).dot(U.T))
                
                b=np.linalg.pinv(W_half).dot(s)
                
                # performs lasso : min_{beta}{1/2||W_{11}^{1/2}*beta-b||+rho|beta|} 
                beta=-clf.fit(W_half,b).coef_
            
                # find w
                w=W.dot(beta)
                
                l=-beta/(sigma-beta.T.dot(W).dot(beta))
                lmbd=1/(sigma-beta.T.dot(W).dot(beta))
            
                A=self.__put(L,l,lmbd)
                invA=self.__put(W,w,sigma)
                S=self.__put(R,s,sii)

            
            if np.linalg.norm(A-A_old,ord=2)<self.tol:
                break
            else:
                A_old=A
        
        self.covariance=S
        self.precision=A
        return self
         
            
    # select pth row and column from ndarray X;
    def __get(self,S):
        end=S.shape[0]-1
        R=S[:-1,:-1]
        s=S[end,:-1]
        sii=S[end][end]
            
        return [R,s,sii]
    
    # permute the columns and rows : let s to be the first column and row of X;
    def __put(self,R,s,sii):
        n=R.shape[0]+1
        X=np.empty([n,n])
        X[1:,1:]=R
        X[1:,0]=s
        X[0,1:]=s
        X[0][0]=sii
        
        return X