def add(x, y):
    return x + y
#設定
import math
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import time
import datetime as dt

import pyperclip
from pyperclip import copy
from pyperclip import paste

def p(a,b=''):print(b+'>>'+str(a))

import sympy as sym
from sympy import init_printing
from sympy import sqrt,sin,cos,tan,exp,log,diff
init_printing()

### グローバル変数定義
__DATAPATH__   = './data'
__LATEXPATH__  = './LaTeX'
__TEXDATAPATH__= './LaTeX/data'

(a_,b_,c_,d_,e_,
 f_,g_,h_,i_,j_,
 k_,l_,m_,n_,o_,
 p_,q_,r_,s_,t_,
 u_,v_,w_,x_,y_,
 z_) = sym.symbols('a b c d e f g h i j k l m n o p q r s t u v w x y z')
(A_,B_,C_,D_,E_,
 F_,G_,H_,I_,J_,
 K_,L_,M_,N_,O_,
 P_,Q_,R_,S_,T_,
 U_,V_,W_,X_,Y_,
 Z_) = sym.symbols('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')
oo_,pi_ = sym.oo,sym.pi
lamda_, theta_= sym.symbols('lamda theta')

def matplotlib_setup(name='test.jpg'):#dx,dy):
    #描画設定
    #plt.rcParams['font.family'] ='IPAGothic'### 'sans-serif'
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
def begin_plt():#by
    plt.figure(figsize=(3.14,3.14))    #3.14 インチは約8cm
    #軸の数値の桁数指定
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))#y軸小数点以下3桁表示.
    #軸の数字が整数になるようにする
    plt.gca().xaxis.get_major_formatter().set_useOffset(False)
    plt.locator_params(axis='x',nbins=12)#軸目盛りの個数指定.x軸，6個以内
    plt.locator_params(axis='y',nbins=12,rotation=30)#軸目盛りの個数指定.y軸，6個以内
    ### plt.gca().yaxis.set_major_formatter(plt.ticker.MultipleLocator(20))           # 20ごと
    ### plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(5))                # 最大5個
    #軸目盛りの向きおよび枠のどの位置はありにするかを指定
    plt.gca().yaxis.set_tick_params(which='both', direction='in',bottom=True,
                                    top=True, left=True, right=True)
    plt.xticks(rotation=70)### x軸目盛を重ならないように
def end_plt(figname='test.jpg'):
    plt.tight_layout()#グラフが重ならず，設定した図のサイズ内に収まる。
    plt.savefig(figname, dpi=600)
    return plt
def mkdf(in_data):
### debug
### importlib.reload(ep)
### display(ep.mkdf([[0,11,11],[0,2,2],[0,3,3]]))
### display(ep.mkdf([[0,0,0],[11,1,1],[22,2,2]]))
### display(ep.mkdf([[0,11,11],[22,3,3],[22,3,3]]))
    ind = []
    col = in_data[0]
    data= []
    for i in in_data:
        ind.append(i[0])
        data.append(i[1:])
    if ind[1]==0:### DATA_IS_NO_INDEX
        return pd.DataFrame(data[1:],index=None,columns=col[1:])
    elif col[1]==0:### DATA_IS_NO_COLUMNS
        return pd.DataFrame(data[1:],index=ind[1:],columns=None)
    else: return pd.DataFrame(data[1:],index=ind[1:],columns=col[1:])
def reshape_df(arr,col_num,col=None):#(非推奨)
    ind = []
    data=[]
    for i in range(int(len(arr)/col_num)):
        n1=i*col_num+1;### print(n1)
        n2=(i+1)*col_num
        ind.append(str(n1)+'to'+str(n2))#;print(ind)
        data.append([arr[n1-1: n2]])#;print(data)
    else:
        n1 = int(len(arr)/col_num)*col_num+1#;print(n1)
        n2 = int(len(arr)/col_num+1)*col_num#;print(n2)
        ind.append(str(n1)+'to'+str(len(arr)))#;print(ind)
        data.append([arr[n1-1:]])#;print(data)
    return pd.DataFrame(data,ind,col)
