import pandas as pd
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import unittest

import warnings
warnings.filterwarnings('ignore') 


class SpamDetector(object):
    def __init__(self):
        self.model=None
        self.sms_model=None
        
    def prob_spam(self,string,model):
        self.model=model
        self.sms_model=pickle.load(open(self.model,"rb"))
        self.test=unittest.TestCase()
        self.string=string
        self.prob=self.sms_model.predict_proba([self.string])
        self.probspam=self.prob[0][1]
        return self.probspam
    
    def is_spam(self,string,model):
        self.model=model
        self.sms_model=pickle.load(open(self.model,"rb"))
        self.test=unittest.TestCase()
        self.result=None
        self.string=string
        self.predict=self.sms_model.predict([self.string])
        if self.predict[0]=='ham':
            self.result='False'
            return self.result,self.string,
        elif self.predict[0]=='spam':
            self.result='True'
            self.string=""
            return self.result,self.string





        
