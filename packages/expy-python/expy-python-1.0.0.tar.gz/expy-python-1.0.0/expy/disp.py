### packages
import math
import numpy  as np
import pandas as pd
import sympy  as sym
import matplotlib.pyplot as plt
from pyperclip import copy
from pyperclip import paste
from IPython.display import Latex

### my create
from .base import *

''' the process to display (表示) --------------------------------------------'''
#丸め
def roundup(x,dig=2):
    func=lambda x:(math.ceil(x*(10**dig))) / (10**dig)
    return to_multi_d(func,x,0)
def rounder(x,dig=2):
    func=lambda x:round(x,dig)
    return to_multi_d(func,x,0)
# 桁数
def digitnum(x):
    y = abs(x)+abs(x)*0.0000000000001
    if y>=1 : return  np.floor(np.log10(float(y)))
    if 1>y>0: return -np.floor(np.log10(float(1/y))+1)
    if y==0 : return  0

### 有効数字何桁か計算. 例)effective_digit( 0.03412/1000000000) -> 4
def effective_digit(num):
    num_str = str( num*(10**-digitnum(num)) )
    num_i, num_d = num_str.split('.') if '.' in num_str else (num_str, '0')
    if   '0000'in num_d: num_d = num_d.split('0000')[0]
    elif '9999'in num_d: num_d = num_d.split('9999')[0]
    return len(num_d)+1

# 有効n桁 (return float) ### this is used in tex.py
def sgnf(n_in,num_sgnf= 3):# 有効n桁
    dig = digitnum(n_in)
    n_rslt = n_in * (10**(-dig))
    n_rslt = np.round(float(n_rslt),int(num_sgnf-1));
    n_rslt = n_rslt * (10**(dig))
    return n_rslt

'''to interpret the results (結果の表示)--------------------------------------'''
def to_sf(n_in, sf_in=None, up=False):# 有効数字化
    dig = digitnum(n_in)
    sf  = sf_in if sf_in is not None  else effective_digit(n_in)
    n_rslt = n_in * (10**(-dig))
    n_rslt = roundup(float(n_rslt),int(sf-1)) if up else np.round(float(n_rslt),int(sf-1));
    if dig==0:return '%s'% roundup(n_in,sf-1) if up else np.round(n_in, sf-1)
    if dig==1:return r'%s\times 10'%(n_rslt)
    return r'%s\times 10^{%s}'%(n_rslt, int(dig))

def rslt_ans(mean, uncrt=None, rm=None, dig=None, dollar=False):
    #def roundup(x,dig):return (np.ceil(x*(10**dig))) / (10**dig)
    sf  = dig if dig else effective_digit(mean)
    if not uncrt:return '%s%s'%(to_sf(mean, sf), r'\mathrm{%s}'%rm if rm else '')
    dig_u = int(-digitnum(uncrt)) ### 以降はuncrtに桁を合わせる
    ans = r"%s\pm %s"%(to_sf(round(mean, dig_u)), to_sf(roundup(uncrt,dig_u)))
    rslt= r'%s%s%s'%('('if rm else '', ans, r')/\mathrm{%s}'%rm if rm else '')
    return ' $%s$ '%rslt if dollar else rslt

def rslt_ans_array(mean,uncrt=None,rm=None,dig=None):
    return [rslt_ans(m, u, rm, dig) for m, u in zip(mean, uncrt)]

def rslt_ans_align(mean, uncrt,x, rm='',dig=None):
    def _align_asta_latex(unit=[],cp=True, ipynb=True):
        tex=""
        for i in range(len(unit)):
            if unit[i]:
                if i!=0:tex+='\n\t&='
                tex +=sym.latex(unit[i])
                if i!=0:tex+=r'\\'
        tex = r'\begin{align*}'+'\n\t'+tex+'\n\t'+r'\end{align*}'
        if cp   : copy( tex )
        if ipynb: return Latex( tex )
        else    : return tex
    display(_align_asta_latex([x, rslt_ans(mean, uncrt, rm, dig)]))

def df_sf(data, dig=3): #DataFrameの数値をto_sf する
    df = data.copy()
    for key, val in data.items():
        df[key] = ['$%s$'%to_sf(v, dig) if type(v)!= type('') else v for v in val]
    return df
### pd-------------------------
def mkdf(in_data):
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

### plt  ----------------------
def rslt_polyfit(x,y,dig=3):
    a,b = np.polyfit(x,y,1)
    return 'y='+str(round(a,dig))+'x+'+str(round(b,dig))

def rslt_polyfit_plot(x, y1, graph=None,point='v--',line=0.75,back=False, plot=True, input=True):
    a,b = np.polyfit(x, y1, 1)
    y2=[]
    for i in x:
        y2.append(i*a+b)
    if plot:
        if graph: [fig.plot(x,y,point, lw=line) for y in [y1, y2]]
        else    : [plt.plot(x,y,point, lw=line) for y in [y1, y2]]
    if back: return a, b

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



''' (非推奨) -----------------------------------------------------------------'''
# 有効数字化 (return str)==to_sf >> to_sgnf_fig is not recommended.
def rslt(mean,uncrt):
    def roundup(x,dig):return (math.ceil(x*(10**dig))) / (10**dig)
    def rslt_unit(mean,uncrt):
        dig = -digitnum(uncrt)
        return "{0}±{1}".format(rounder(mean, dig), roundup(uncrt,dig))
    func=lambda m,u: rslt_unit(m,u)
    return to_multi_d(func,mean,0,uncrt)
def to_sgnf_fig(n_in,num_sgnf):
    dig = digitnum(n_in)
    if dig==0:return str(np.round(n_in, num_sgnf))
    n_rslt = n_in * (10**(-dig))
    n_rslt = np.round(float(n_rslt),int(num_sgnf-1));
    rslt = r'{0}\times 10^{{{1}}}'.format(n_rslt, int(dig))
    return rslt
