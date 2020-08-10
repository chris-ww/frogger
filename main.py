# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:24:39 2020

@author: cwerw
"""


def main():
    level = 0
    USER = 'HUMAN'
    if len(sys.argv) > 2:
        user = sys.argv[1]
        level = sys.argv[2]
    elif len(sysargv) >1:
        user = sys.argv[1]
    if(user == 'LEARN'):
        USER='LEARN'
    elif(user == 'EVALUATE"):
        USER = 'EVALUATE
    else:
        USER = 'HUMAN'
    if(level>=0 && level <=1):
        LEVEL=level

if __name__ == "__main__":
    main()
    