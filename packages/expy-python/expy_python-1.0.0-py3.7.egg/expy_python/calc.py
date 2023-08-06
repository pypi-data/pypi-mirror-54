'''1.解析-------------------------------------------------------------------------'''
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
def to_multi_d(func,data,is_list,data2=None,is_none=None):
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
#mmからcmへ変換
def mm_to_cm(a):func=lambda a:a/10;return to_multi_d(func,a,0)
#cmからmへ変換
def cm_to_m(a):func=lambda a:a/100;return to_multi_d(func,a,0)
#cmからmmへ変換
def cm_to_mm(a):func=lambda a:a*10;return to_multi_d(func,a,0)
#平均
def mean(a):func=lambda a:np.mean(a);return to_multi_d(func,a,1)
#関数のすべての変数に値を代入
def subs(func,sym,val):
    for i in range(len(val)):
        func = func.subs([(sym[i],val[i])])
    return func
#標準不確かさ計算
def STDEV(data):
    def STDEV_unit(d):
        #unit
        ave = np.sum(d) / len(d)
        siguma = 0
        for i in range(len(d)):
            siguma += math.pow(d[i] - ave, 2)
        if len(d)<=1:
            return 0
        else:
            output = math.sqrt( siguma / (len(d)-1) )
            return output
    func=lambda d:STDEV_unit(d)
    return to_multi_d(func,data,1)
#平均値の不確かさ計算
def uncrt(data):
    def uncrt_unit (data):
        output = STDEV(data) / math.sqrt(len(data))
        return output
    func=lambda d:uncrt_unit(d)
    return to_multi_d(func,data,1)
#相対不確かさ
def rlt_uncrt(data):
    def rlt_uncrt_unit (data):
        return uncrt(data) / np.mean(data)
    func=lambda d:rlt_uncrt_unit(d)
    return to_multi_d(func,data,1)
def cul(data,p=0):
    def cul_unit(data):
        mean  = np.mean (data)
        uncrt = ep.uncrt(data)
        rslt  = ep.rslt(mean,uncrt)
        rlt   = ep.rlt_uncrt(data)
        #結果まとめ
        df_cul = pd.DataFrame([uncrt,rslt,rlt],index=['uncrt','rslt','rlt/%',])
        df_cul = pd.Series(data).describe().append(df_cul)
        if p==1:display(df_cul.T)
        return df_cul.T
    unit=lambda d:cul_unit(d)
    return to_multi_d(unit,data,1)
#二乗和平均
def mean_sq(data):
    def mean_sq_unit(data1,data2):
        import math
        synth = math.sqrt(math.pow(data1,2)+math.pow(data2,2))
        return synth
    func=lambda d1,d2:mean_sq_unit(d1,d2)
    synth = data[0]
    for i in range(1,len(data)):
        synth = to_multi_d(func,synth,0,data[i])
    return synth
#合成不確かさ(非推奨)
def syn_uncrt(func=sym.Symbol('f'),
              uncrt_sym=[],
              uncrt_all=[],
              sym_all=[sym.Symbol('f')],
              val_all=[0],
              rm_all =[],
              arr=0):
    def sym_to_val_to_latex(func,sym_all=[],val_all=[],rm_all=[]):#sym, valは配列
        #初期化
        sym_str = []
        if rm_all==[]:rm_all=['',]*len(sym_all)
        for i in sym_all:
            sym_str.append(sym.Symbol('[]'+str(i)+'[]'));
        func_str = subs(func,sym_all,sym_str)#;print(1,func_str)
        func_str = sym.latex(func_str)       #;print(2,func_str)
        for i in range(len(sym_all)):
            func_str=func_str.replace(str(sym.latex(sym_str[i])),
                                      '('+str(round(val_all[i],3))+r'\mathrm{'+rm_all[i]+'}'+')')
        return func_str
    def syn_uncrt_unit(uncrt_all=[],val_all=[0]):#偏微分用
        #fはlen(uncrt_all)変数関数(いらない数値は代入しておく)
        syn  = 0
        partial_all      = []#各偏微分したSym    ：
        all_sym_to_val   = []#各変数を代入したSym：         ：
        uncrt_unit_all   = []#各計算したInt：1.0
        def uncrt_to_unit_uncrt(u,sym):#不確かさuと対応する変数
            df_dsym = diff(func,sym);
            for i in range(len(sym_all)):
                df_dsym=df_dsym.subs([(sym_all[i],val_all[i])] );
            return u*float(df_dsym)
        for i in range(len(uncrt_all)):
            unit_uncrt= 0
            unit_uncrt_sym = sym.Symbol(r'\Delta '+str(uncrt_sym[i]))**2
            unit_parcial = unit_uncrt_sym
            if uncrt_sym[i] is None:
                syn = mean_sq([syn,uncrt_all[i]])
                unit_uncrt = uncrt_all[i]
            else:
                #print('--in',uncrt_sym[i],'=',uncrt_all[i],'---------------')
                unit_uncrt= uncrt_to_unit_uncrt(uncrt_all[i],uncrt_sym[i])
                unit_parcial = (diff(func,uncrt_sym[i]))**2
                unit_sym_to_val = sym_to_val_to_latex(unit_parcial,sym_all,val_all,rm_all)+'('+str(uncrt_all[i])+')^{2}'
                unit_parcial = sym.latex(unit_parcial)+sym.latex(unit_uncrt_sym)
                syn = mean_sq([syn,unit_uncrt])
            partial_all.append(unit_parcial)
            uncrt_unit_all.append(unit_uncrt)
            all_sym_to_val.append(unit_sym_to_val)
        if arr==0:return syn
        else     :return [syn,               #答え（合成不確かさ）
                          partial_all,       #各偏微分したSym
                          all_sym_to_val,    #各変数を代入したStr
                          uncrt_unit_all]    #各計算したInt：1.0
    unit=lambda u,v:syn_uncrt_unit(u,v)
    return to_multi_d(unit,uncrt_all,1,val_all)
#加重平均       （不確かさの二乗の逆数で重みを浸けて平均）
def weighted_mean(mean_all, uncrt_all):
    def weighted_uncrt_unit(mean_all, uncrt_all):
        numer1 = mean_all / np.square(uncrt_all)
        denom1 =     1 / np.square(uncrt_all)
        mean  = np.sum(numer1) / np.sum(denom1)
        denom2 = 1 / np.square(uncrt_all)
        uncrt = 1 / np.sqrt(np.sum(denom2))
        return mean, uncrt
    func=lambda m,u:weighted_uncrt_unit(m,u)
    return to_multi_d(func,mean_all,1,uncrt_all)
