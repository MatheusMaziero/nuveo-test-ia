import pandas as pd
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import unittest
from scr.spamhamclass import SpamDetector

import csv
import os

import warnings
warnings.filterwarnings('ignore') 


        
class TestMain(unittest.TestCase):
    
    def testmain(self):
        import warnings
        warnings.filterwarnings('ignore') 
        model=str(input('Entre com o endereço do modelo: '))
        string=str(input('Entre com o endereço do arquivo para test: '))
        test=SpamDetector()
        listdir,listname = os.path.split(string)
        with open(string, 'r') as f:
            csvreader= csv.reader(f, delimiter=';')
            listlist=[]
            for row in csvreader:
                listlist.append(row[0]+row[1]+row[2]+row[3]+row[4])
                
            for llist in listlist:
                with self.subTest(line=llist):
                    prob=test.prob_spam(llist,model)
                    result,mensagem=test.is_spam(llist,model)
                    self.assertEqual(result, 'False','É um Ham')
                    self.assertEqual(result, 'TRUE','É um Spam')
                    self.assertEqual(mensagem, llist,'é Ham ,esta certo para caixa de mensagem')
                    self.assertGreaterEqual(prob,0.5,'é Spam')
                    self.assertGreaterEqual(prob,0.5,'é Ham')

    
                

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore') 
    unittest.main()


        
