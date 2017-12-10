# -*- coding: utf-8 -*-
import numpy as np
import gensim
import logging
from logging.handlers import RotatingFileHandler
from gensim.models import *


def trans2txt(logger, sourcefile, targetfile, wordLen=200, wordCount=200):
    model = gensim.models.Word2Vec.load('result.model')
    f1 = open(sourcefile, "r")
    f2 = file(targetfile, "w")
    while 1:
        line = f1.readline()
        if line:
            a_old = np.zeros(wordLen, float)
            for i in range(0, wordCount):
                str_new, sep, str_rest = line.partition(',')
                str_utf8 = str_new.decode('utf-8')
                line = str_rest
                try:
                    a_new = model[str_utf8]
                except Exception, e:
                    a_new = np.zeros(wordLen, float)
                    logger.error(e.message)
                if i != 0:
                    a_old = np.vstack((a_old, a_new))
                else:
                    a_old = a_new
            m = np.asmatrix(a_old)
            m = m.reshape((1, wordLen * wordCount))
            np.savetxt(f2, m)
        else:
            break
    f1.close()
    f2.close()


if __name__ == "__main__":
    logger = logging.getLogger()
    fh = logging.FileHandler('./test.log', 'w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    trans2txt(logger=logger, sourcefile='result.txt', targetfile='matrix.txt',)
