import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sympy import init_printing
from sympy import sqrt,sin,cos,tan,exp,log,diff

### my create
def p(a,b=''):print(b+'>>'+str(a))
### init_printing()

#多次元化
def to_list(data):
    if type(data) is  type(pd.Series([])):
        return data.values.tolist()
    if type(data) is  type(pd.DataFrame([])):
        return data.values.tolist()
    if type(data) is  type(np.array([])):
        return data.tolist()
    else:
        return data

def to_discrete(arr,method=lambda a,b: b-a,axis=0):
    if type(arr) is type(pd.DataFrame([]))and axis==0:
        arr=arr.T
    def _to_discrete(arr,method=lambda a,b: b-a):
        arr_rslt=[np.NaN]
        for i in range(len(arr)-1):
            arr_rslt.append(method(arr[i],arr[i+1]))
        return arr_rslt
    arr_in=to_list(arr)
    func=lambda arr:_to_discrete(arr,method)
    return to_multi_d(func,arr_in,1)

#単位変換
def mm_to_cm(a):func=lambda a:a/10;return to_multi_d(func,a,0)
def cm_to_m(a):func=lambda a:a/100;return to_multi_d(func,a,0)
def cm_to_mm(a):func=lambda a:a*10;return to_multi_d(func,a,0)


def reshape_df(arr,col_num,col=None): ### 非推奨
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

def to_multi_d(func,data,is_list,data2=None,is_none=None):#(非推奨)
    data = to_list(data)
    #p(type(data),"data_type")
    #p(is_list,"is_list")
    def do(to_arr= 0):
        if data is None:
            return is_none
        if to_arr==0 :
            if data2 is None:
                return func(data)
            else:
                return func(data,data2)
        if to_arr==1:
            if data2 is None:
                return func([data])
            else:
                return func([data],[data2])
    def repeat():
        #print("repeat-------------------start")
        output=[];
        for i in range(len(data)):
            if data2 is None:
                output.append(to_multi_d(func,data[i],is_list,is_none))
            else:
                output.append(to_multi_d(func,data[i],is_list,data2[i],is_none))
        #print("repeat-------------------end")
        return output
    #1. 入力が数値の場合
    if type(data) is not list:
        if is_list==0: return do()
        if is_list==1: return do(1)
        else:p("not ? but 0")
    #2. 入力が配列の場合
    if type(data) is     list:
        if is_list==0:
            return repeat()
        elif is_list==1:
            if type(data[0]) is not list: return do()
            if type(data[0]) is     list: return repeat()
        else:p("not ? but 1")
    else:return "??"
