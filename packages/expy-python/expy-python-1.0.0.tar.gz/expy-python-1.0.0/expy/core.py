import math
import numpy as np
import pandas as pd
import sympy as sym
from sympy import init_printing
from sympy import sqrt,sin,cos,tan,exp,log,diff
### helper
from .base  import *
from .calc  import *
from .disp  import *
from .var   import *
from .tex   import *
### from .tex import Tex
### theme11
init_printing()

def init_ep():
    #init_printing()
    init_pd()
    init_plt()
    global added

def init_pd():
    try:
        pd = globals()['pd']
        ### nbconvert: using pandas DataFrame by xelatex
        def _repr_html_(self):
            return '<center> %s </center>' % self.to_html()
        def _repr_latex_(self):
            return "\\begin{center} %s \\end{center}" % self.to_latex(escape=False)

        pd.set_option('display.notebook_repr_html', True)
        pd.set_option('display.max_colwidth', -1)
        pd.DataFrame._repr_html_  = _repr_html_
        pd.DataFrame._repr_latex_ = _repr_latex_  # monkey patch pandas DataFrame
    except:
        print('ImportError: No module named \'pandas\'')


def init_plt(name='test.jpg'):#dx,dy):
    try:
        #plt.rcParams['font.family'] ='IPAGothic'### 'sans-serif'
        plt = globals()['plt']
        plt.rcParams['mathtext.default'] = 'regular'
        plt.rcParams['xtick.top'] = 'True'
        plt.rcParams['ytick.right'] = 'True'
        plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
        plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
        plt.rcParams['axes.grid'] = 'True'
        plt.rcParams['axes.xmargin'] = '0' #'.05'
        plt.rcParams['axes.ymargin'] = '.05'
        plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ
        #plt.rcParams['savefig.facecolor'] = 'None'
        #plt.rcParams['savefig.edgecolor'] = 'None'
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['font.size'] = 8 #フォントの大きさ
        plt.rcParams['xtick.labelsize'] = 8 # 横軸のフォントサイズ
        plt.rcParams['ytick.labelsize'] = 8 # 縦軸のフォントサイズ
    except:
            print('ImportError: No module named \'pandas\'')


''' (非推奨) -----------------------------------------------------------------'''
DSP              = 1
