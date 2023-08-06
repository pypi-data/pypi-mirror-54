import math
import numpy  as np
import sympy  as sym
import pandas as pd
from sympy import sqrt,sin,cos,tan,exp,log,diff
from pyperclip import copy
from pyperclip import paste
from IPython.display import display, Math, Latex, Image, Markdown, HTML
### my create
from .base  import to_list
from .calc  import weighted_mean, uncrt
from .disp  import digitnum, sgnf, roundup, effective_digit, to_sf, df_sf, rslt_ans, rslt_ans_array, rslt_ans_align
from .var   import *
### from .latex import sym

### display in ipython ---------------------------------------------------------
def newpage():display(Latex('\\newpage'))
def tiny():display(Latex(r'\tiny'))
def norm():display(Latex(r'\normalsize'))
def md(text= '')           :display( Md(text))
def caption(text= '')      :display( Caption(text) )
def figure(filepath,cap=''):display( Image(filepath), Caption(cap))

def table(data, cap='', text=None, index=None, is_sf= False, is_tiny=False):
    rslt= pd.DataFrame(data, index=index if index else ['']*len(list(data.values())[0])) if type(data) is type({}) else data
    if is_sf: rslt = df_sf(rslt)
    if text:display(Caption(text)) if type(text)==type('')else md('以上より, 以下の表を得る')
    if cap: display(Caption(cap))
    if is_tiny:tiny()
    display(rslt);
    if is_tiny:norm()
def freehand(text= '', line=12):
    for i in range(line):
        ### display(Markdown('<div style="page-break-after:always;color:transparent;"></div> '))
        ### display(Markdown('b<p style="page-break-after:always;"></p>'))
        ### display(Markdown('<div id="pagebreak" style="page-break-before:always;color:transparent;"></div>'))
        display(Markdown('<p style="page-break-after: always;">&nbsp;</p>'))
    display(Caption(text))

class Md():
    def __init__(self,s):
        self.s = s
    def _repr_html_(self):
        return '%s' % self.s
    def _repr_latex_(self):
        return '\n %s \n' % self.s

class Caption():
    def __init__(self,s= ''):
        self.s = s
    def _repr_html_(self):
        return '<center> %s </center>' % self.s
    def _repr_latex_(self):
        return '\\begin{center}\n %s \n\\end{center}' % self.s
### latex ----------------------------------------------------------------------
def align_asta_latex(unit=[],cp=True, ipynb=True):
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
def to_latex(s='x^2+ y^2',ans=0, x='z', rm='',dig=3, cp=True,ipynb=True,label=''):
    return align_asta_latex(['%s'%x, '%s'%s, r'%s\mathrm{%s}'%(to_sf(ans, dig*2), rm),
                      r'%s\mathrm{%s}'%(to_sf(ans, dig),rm)],cp,ipynb)
def frac(denom,numer,ans=0, x='z', rm='',dig=3, cp=True,ipynb=True,label=''):
    return to_latex(r'{\tiny \frac{%s}{%s}}'%(denom, numer), ans, x,rm,dig, cp,ipynb,label)
def weighted(mean_all, uncrt_all, x='z', rm='',dig=3,cp=True,ipynb=True, label=''):
    def tex_weighted_mean(mean_all, uncrt_all, x='z', rm='',cp=True,ipynb=True, label=''):
        denom = ''#分子
        numer = ''#分母
        for i in range(len(mean_all)):
            denom += '\\frac{%s}{(%s)^2}'%(to_sf(mean_all[i], dig), to_sf(uncrt_all[i], dig))
            numer += '\\frac{1}{(%s)^2}' % to_sf(uncrt_all[i], dig)
            if i != len(mean_all)-1:
                denom += '+'
                numer += '+'
        #LaTeX作成
        return frac(denom,numer,weighted_mean(mean_all,uncrt_all)[0],x,rm,dig)
    def tex_weighted_uncrt(mean_all, uncrt_all,x='z', rm='',cp=True,ipynb=True, label=''):
        numer = '\\sqrt{'#分母
        for i in range(len(mean_all)):
            numer += '\\frac{1}{(%s)^2}'%to_sf(uncrt_all[i], dig)
            if i != len(mean_all)-1:
                numer += '+'
            if i == len(mean_all)-1:
                numer += '}'#sqrt
        #LaTeX作成
        return frac('1',numer,weighted_mean(mean_all,uncrt_all)[1],x,rm,dig)
    display( tex_weighted_mean (mean_all, uncrt_all,           x, rm,cp,ipynb, label) )
    display( tex_weighted_uncrt(mean_all, uncrt_all,r'\Delta '+x, rm,cp,ipynb, label) )
    md('よって $%s$ は以下のようになる.' % x)
    rslt_ans_align(weighted_mean(mean_all,uncrt_all)[0],weighted_mean(mean_all,uncrt_all)[1],x,rm,dig)
### sub process ----------------------------------------------------------------
def dollar(arr):return [' $%s$ '%v for v in arr] if type(arr)!=type('') else ' $%s$ '%arr
def mark_number(text):
    rslt = text
    for i,j in zip([str(i) for i in range(10)], ['%{}%'.format(i) for i in range(10)]):
        rslt = rslt.replace(i,j)
    return rslt
### core process ---------------------------------------------------------------
class Var:
    ### set
    def __init__(self, var=sym.Symbol('x')):
        ### base ---------------------------------
        self.var = var ### var  type is sym.Symbol
        self.val = 0   ### val  type is float
        self.dig = 3   ### dig  type is int
        self.rm  = ''  ### rm   type is str
        ### err --------------------------------
        self.array = np.array([0])  ### vals type is np.array
        self.err = 1             ### err  type is float
        self.todiff= None           ### todiff type is sym.Symbols of (pa_*func)/(pa_*self.var)
        self.diffed= None           ### diffed type is diffed function of sym.Symbol by self
    ### init process -----------------------------------------------------------
    def set_var(self, var=None, val=None, rm=None, dig=None):
        if val is not None: self.set_array(val)
        if var: self.var = var
        if rm : self.rm  = str(rm)
        if dig: self.dig = int(dig)
    def set_array(self, val):
        self.array = np.array(val)
        if  self.array.size==1:
            self.val  =val
            self.err=0
            self.dig  =effective_digit(self.val)
        else:
            self.val  =np.mean(val)
            self.err=np.std(val)/np.sqrt(len(val)-1)
            self.dig  =effective_digit(self.array[0])
    ### err process ----------------------------------------------------------
    def set_diff(self, ans_obj, function):
        self.todiff= sym.Symbol(r'(\frac{{ \partial {} }}{{ \partial {} }})^2'.format(sym.latex(ans_obj.var),sym.latex(self.var)))
        self.diffed= sym.diff(function, self.var)**2;   ### display(self.diffed)
    ### latex subs process -----------------------------------------------------
    def subs_str(self, func):return func.subs(self.var, '%'+sym.latex(self.var)+'%')###vars to vars or str   : varをマーキング
    def subs_ans(self, func):return func.subs(self.var, self.val)                   ###vars to vars or float: varに数値を代入
    def subs_val(self, func):return func.subs(self.var, r'%s\mathrm{%s}'%(round(self.val,self.dig),self.rm) )###vars to vars or str   : varにstr(数値.round)+単位を代入
    def tex     (self)      :return r'%s'        %sym.latex( self.var )
    def d_tex   (self)      :return r'\Delta{%s}'%sym.latex( self.var )
    def tex_name(self,err=True, rm=True):
        text = r'%s\pm %s'%(self.tex(),self.d_tex()) if err else self.tex()
        return r'%s(%s)%s'%('(' if rm else '', text, r'/\mathrm{%s}'%self.rm if rm else '')
    ### latex output process ---------------------------------------------------
    def df(self, df_name='', name=''):
        ### md('%s回計測した%s $%s$ を記すと, 以下の表を得る.'%( self.array.size, (name if name else ''), self.tex()))
        data = {'%s'%name:self.array}
        df = pd.DataFrame(data, index=['']*len(self.array))
        return df.T
    def latex_mean(self, max=10, cp=True, ipynb=True):
        denom =  ''
        N=self.array.size
        for i in range(N):
            if i != 0 :denom=denom+'+'
            if i >=max:denom=denom+'..';break
            denom += r'%s \mathrm{%s}' %(to_sf(self.array[i],self.dig), self.rm)
        display( frac(denom,str(N),np.mean(self.array),self.tex(),self.rm,cp=True,ipynb=True))
    def latex_err(self, cp=True, ipynb=True):
        N=self.array.size ;m=to_sf(np.mean(self.array), self.dig);
        s = r'\sqrt{\frac{1}{%s\cdot%s}\sum_{i=1}^%s(%s_i-%s)^2}'%(N, N-1, N, self.tex(), m)
        display( to_latex(s, uncrt(self.array), self.d_tex(), self.rm, self.dig, cp=True,ipynb=True) )
    def latex(self, max=10, cp=True, ipynb=True):
        ### md(' $%s$ を計算すると, 以下のようになった.'%self.tex_name(rm=False))
        if self.err:
            self.latex_mean(max, cp, ipynb)
            self.latex_err(cp, ipynb)
        ### md('よって $%s$ は以下のようになった.'%self.tex_name(rm=False))
            rslt_ans_align( self.val, self.err, self.tex_name(rm=False), self.rm, self.dig )
''' Eq object ------------------------------------------------------------------
  * This object responsible for processing
-----------------------------------------------------------------------------'''
class Eq:
    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        ### 設定
        self.label      = label              ### to_latex用
        self.func    , self.todiff  , self.diffed   = [None]*3### diff: functionとsyn
        self.subs_str, self.subs_val, self.subs_ans = [None]*3###
        self.func_val, self.func_ans, self.func_rslt= [None]*3### Latex用
        self.syn_val , self.syn_ans , self.syn_rslt = [None]*3### syn : 合成不確かさ用
        self.eq         = sym.Eq(leq, req)   ### 方程式
        self.vars       = {}                 ### 方程式を構成する変数の辞書.
        self.ans        = None               ### ans tyoe is Var obj
        self.ans_val    = 0
        self.err_val    = 0
        if ans_sym: self.set_func(self.vars[ans_sym].var)### ans = Var();self.ans.set_var(leq)
        elif leq in self.vars: self.set_func(self.vars[leq].var)
    ### init setting -----------------------------------------------------------
    def set_var  (self, obj)      : self.vars[obj.var]   = obj### 辞書varsに追加
    def set_err(self, var, err) : self.vars[var].err = err
    def set_func (self, ans_sym=None) :
        if ans_sym : self.ans = self.vars[ans_sym]                    ### 入力があったらself.ansの変更
        if self.ans: self.func = sym.solve( self.eq, self.ans.var )[0]### 方程式から関数へ変形
        else       : print("please set ans_var_object as 'eq_obj.set_ans( var_obj )'")
    def set_ans  (self, obj)      : self.set_func(obj.var); self.ans= obj       ### 非推奨.未使用
    def set_eq   (self, leq, req) : self.eq=sym.Eq(leq, req);self.set_func()    ### 非推奨.未使用
    def set_obj (self, var=None, val=None, rm='', dig= 3, ans=False):
        obj = Var()
        obj.set_var(var, val, rm, dig)
        self.set_var(obj)
        if (val is None) or ans: self.set_func(obj.var)### set_ansだとfuncがNoneのままなので注意
    def set_err(self, var, err):self.vars[var].err = err       ### 非推奨
    ### manage process ---------------------------------------------------------
    def not_setting_obj(self):    ### set_objされていない変数をreturn
        return [v for v in self.eq.atoms(sym.Symbol)if not v in self.vars]
    def status(self): ### eqの代入状態を返す
        for v in self.not_setting_obj(): print('{0} is not setting. please run "f.set_obj({0})"'.format(v))
        display(pd.DataFrame({' $%s$ '%sym.latex(var):[ obj.val, r'$\mathrm{%s}$'%obj.rm, obj.dig, var==self.ans.var] for var, obj in self.vars.items() },
                            index=['val', 'rm'  , 'dig'  , 'is ans']).T)
    ### latex sub process ------------------------------------------------------
    ### subs 代入処理
    def set_tex(self, err=False):       ###Sym.subs_str:  vars -> vars or str
        if self.ans is None: [self.set_obj(var, None) for var in self.not_setting_obj()]
        self.subs_str = self.func ### 初期化  ### subs str
        for var, obj in self.vars.items():self.subs_str = obj.subs_str(self.subs_str)
        self.subs_ans = self.func ### 初期化 ### subs val and ans(subs_valは使われていない...)
        for var, obj in self.vars.items():self.subs_ans = obj.subs_ans(self.subs_ans);
        self.ans_val  = float(self.subs_ans)
        self.func_val = sym.latex(self.subs_str)  ### self.func_valの初期化
        self.func_val = mark_number(self.func_val)### 数字をマーキング
        for var, obj in self.vars.items():        ### 変数マーキング+数値代入
            txt = str(to_sf(float(obj.val), int(obj.dig)))+r'\mathrm{'+obj.rm+'}'### ;print(to_sf(float(obj.val)/100, 3), txt, mark_number(obj.tex()), obj.dig, to_sf(obj.val, int(obj.dig)))
            self.func_val = self.func_val.replace( '%{}%'.format(mark_number(obj.tex())), '%({})%'.format(txt) )### ;print('%{}%'.format(mark_number(obj.tex())), '%{}%'.format(txt) )
        self.func_val = self.func_val.replace(' ','').replace('%%',r'\times ').replace('%','')
        self.func_ans = r'%s\mathrm{%s}'%(to_sf(self.ans_val, self.ans.dig*2),self.ans.rm)
        self.func_rslt= r'%s\mathrm{%s}'%(to_sf(self.ans_val, 1 if err else self.ans.dig,up=True),self.ans.rm)
    def set_syn(self):
        for i, [var, obj] in enumerate(self.vars.items()):
            obj.set_diff(self.ans, self.func) ### Var()によるtodiffとdiffedのリセット
            diff_new = [Delta_(var)**2*obj.todiff, Delta_(var)**2*obj.diffed]
            if var is self.ans.var  :pass
            elif float(obj.err)<=0:pass
            elif self.todiff is None or self.diffed is None: self.todiff, self.diffed= diff_new
            else     : self.todiff, self.diffed= [self.todiff+diff_new[0], self.diffed+diff_new[1]]
        self.todiff = self.ans.var*sqrt(self.todiff)
        self.diffed = self.ans.var*sqrt(self.diffed)
        ### saved past value-------------------------
        past_eq   = self.eq
        past_func = self.func.copy()
        past_vars = self.vars.copy()
        past_ans  = self.ans;### print(past_ans.var)
        past_rslt = self.ans_val
        ### set err ---------------------------------
        self.set_eq ( Delta_(past_ans.var), self.diffed)### print(sym.sympify(self.diffed).atoms(sym.Symbol))
        self.set_obj( Delta_(past_ans.var), None, past_ans.rm, past_ans.dig, ans=1)
        for var, obj in past_vars.items():
            obj.set_diff(self.ans, self.func) ### Var()によるtodiffとdiffedのリセット
            self.set_obj( Delta_(var), obj.err, obj.rm, obj.dig)
        self.set_obj(past_ans.var , past_rslt, past_ans.rm, past_ans.dig, ans=0)
        self.set_tex(err=True);
        self.syn_val =self.func_val
        self.syn_ans =self.func_ans
        self.syn_rslt=self.func_rslt
        self.err_val =self.ans_val ### register the new value
        ### reset value -----------------------------------
        self.eq   = past_eq
        self.func = past_func
        self.vars = past_vars
        self.ans  = past_ans
        self.ans_val = past_rslt
        pass### TODO
    def ans_align(self):
        rslt_ans_align(self.ans_val, self.err_val, self.ans.tex_name(rm= False), self.ans.rm, self.ans.dig)
    ### latex process ----------------------------------------------------------
    def latex(self, cp=True, ipynb=True):
        self.set_tex()
        latex_text = align_asta_latex([
            self.ans.var, self.func,
                          self.func_val,
                          self.func_ans,
                          self.func_rslt,
        ],cp, ipynb)
        if ipynb: display(latex_text)
        else    : return latex_text
    ### error mainprocess ----------------------------------------------------------
    def syn(self, cp=True, ipynb=True, sub_val=True):
        self.set_syn()
        latex_text = align_asta_latex([
            self.ans.d_tex(),   sym.latex(self.todiff),
                                sym.latex(self.diffed),
                               (self.syn_val if sub_val else None),
                                self.syn_ans,
                                self.syn_rslt,
        ],cp, ipynb)
        if ipynb: display( latex_text )
        else    : return latex_text
''' F object--------------------------------------------------------------------
  * This object responsible for manipulating other objects
  * grammar
-----------------------------------------------------------------------------'''
class F:
    def __init__(self, leq, req, ans_sym=None, label='', **kwargs):
        ### init data -----------
        self.leq    = leq
        self.req    = req
        self.ans_sym= ans_sym
        self.label  = label
        ### process data --------
        self.obj    = Eq(self.leq, self.req, self.ans_sym, self.label)
        self.objs   = []
        ### get Eq_obj data -----
        self.eq = self.obj.eq
        ### ---------------------
    ### input sub process in ipython ------------------------------------
    def set_obj(self, var=None, val=None, rm='', dig=None, ans=False):
        self.obj.set_obj(var, val, rm, dig, ans)
    def set_err(self, var, err):
        self.obj.set_err(var, err)
    ### input process in ipython -----------------------------------------
    def set(self, var=None, val=None, rm='', dig=None, ans=False, err=None):
        self.obj.set_obj(var, val, rm, dig, ans)
        if err: self.obj.set_err(var, err)#Var.set_objにはerrキーはないので注意！
    def status(self):[obj.status() for obj in self.objs]
    def save(self):
        self.obj.set_tex()
        self.objs.append(self.obj)
        self.obj = Eq(self.leq,self.req, self.ans_sym, self.label) ### リセット
    ### output sub process in ipython ------------------------------------------
    def get_var(self,var=None):return self.objs[-1].vars[var] if var else self.objs[-1].ans
    def get_ans_val(self)     :return[obj.ans_val         for obj in self.objs]
    def get_ans_err(self)     :return[obj.err_val         for obj in self.objs]
    def get_var_val(self,var) :return[obj.vars[var].val   for obj in self.objs]
    def get_var_err(self,var) :return[obj.vars[var].err   for obj in self.objs]
    def get_var_arr(self, var):return[obj.vars[var].array for obj in self.objs]
    def get_rslt_ans(self)    :return rslt_ans_array(self.get_ans_val()   ,self.get_ans_err()   ,self.get_var().rm   ,self.get_var().dig)
    def get_rslt_var(self,var):return rslt_ans_array(self.get_var_val(var),self.get_var_err(var),self.get_var(var).rm,self.get_var(var).dig)
    def get_vars(self, var, num= None):
        if type(num)==type(0) :return [self.objs[num].vars[var]]
        if type(num)==type([]):return [self.objs[i].vars[var] for i in num]
        if num is None:return [obj.vars[var] for obj in self.objs ]
    ### output sub process in ipython ------------------------------------------
    def get(self, var=None, num=None, ans=False, err=False):
        if var:vals=self.get_rslt_var(var)if ans else self.get_var_err(var)if err else self.get_var_val(var)
        else  :vals=self.get_rslt_ans()   if ans else self.get_ans_err()   if err else self.get_ans_val()
        if type(num)==type(0) :return vals[num]
        if type(num)==type([]):return [vals[n] for n in num]
        ### if not var and len(self.objs)==1  :return vals[-1]
        return vals
    ### sub latex process in ipython -------------------------------------------
    def latex(self, num=None):self.tex_ans(num)### 非推奨(昔使ってたので)
    def tex_num(self,n,arr):return True if arr is None else True if n==arr or n in np.array(arr) else False
    def tex_var(self,var,num=None):[obj.latex() for obj in self.get_vars(var, num)];
    def tex_ans(self    ,num=None):[obj.latex(ipynb=self.tex_num(i,num)) for i,obj in enumerate(self.objs)]
    ### main latex process in ipython -----------------------------------------
    def tex(self, var=None, num=None):
        if self.objs==[]:self.save()
        if var:self.tex_var(var,num) if var!=self.objs[-1].ans.var else self.tex_ans(num)
        else  :self.tex_ans(var if var==0 else num)
    def syn(self, num=None, sub=True):
        [obj.syn(ipynb=self.tex_num(i, num),sub_val=sub) for i,obj in enumerate(self.objs)]
    ### main dataframe process in ipython --------------------------------------
    def df(self, var=None, cap='', index=None, name='', text=False, ans=True, err=False, ipynb=True):
        ans  = self.objs[0].ans;
        vals = self.get(var, num=None, ans=ans, err=err);
        ### index
        if type(index)==type({}):dict = {key: ['$%s$'%v for v in val ] for key, val in index.items()}
        else: dict= {'回数':['%s回目'% (i+1) for i in range(len((vals)))]} if index else {}
        if var:dict.update( {'測定結果$%s$'%(r'/\mathrm{%s}'%ans.rm if ans.rm else''):[[' $%s$'%to_sf(v) for v in arr] for arr in self.get_var_arr(var)]} );
        dict.update( {'$%s%s%s$'%(name,ans.var,r'/\mathrm{%s}'%ans.rm if ans.rm else''): dollar(vals) } );
        ### md
        if text: md(text) if type(text)==type('') else md(r'全項目の計算結果を下表にまとめた.単位は $\mathrm{%s}$ である.'%self.get_var().rm)
        if ipynb: display(Caption(cap), pd.DataFrame(dict, index=['']*len(vals)) );
        else    : return pd.DataFrame(dict, index=['']*len(vals))
    def md(self, name=None, err= True, text=None):
        if text: md(text)
        else   : md('以上より, %s $%s$ を求めると, 次のようになる.'%(name if name else '', self.get_var().tex_name(rm=False)))
    ###  Markdown自動出力 -------------------------------------------------------
    def auto(self, f_num=0):
        vars_str = ''
        for i, var in enumerate(self.vars.keys()):
            if i==0: vars_str  = sym.latex(var)
            else   : vars_str += ', '+sym.latex(var)
        md('{}{}を代入して{}を求めると, 次のようになる.'.format(
            ['式({})に'.format(f_num) if f_num else ''][0], vars_str, sym.latex(self.ans.var)))
    def mkdf(self, cap='全項目の計算結果', index=None, ref=''):
        md(r'全項目の計算結果を下表にまとめた.単位は $\mathrm{%s}$ である.'%self.objs[0].ans.rm)
        if index: pass
        data = {}
        for i, obj in enumerate(self.objs):
            data['%s回目'%(i+1)] = r'($%s\pm %s$)/$\mathrm{%s}$'%(
            to_sf(obj.ans_val, 3), to_sf(obj.err_val,1,up=1), obj.ans.rm)
        caption(cap)
        display( pd.DataFrame(data, index=['']) )

''' repo --------------------------------------------------------------------'''
from sympy import symbols as ss
from sympy import sqrt,sin,cos,tan,exp,log,diff
### def ss   (var)    : return symbols((r'%s'%var).strip) ### CHANGED
def sub  (var,any): return ss(r'%s_{%s}' % (sym.latex(var), sym.latex(any)))
def sup  (var,any): return ss(r'%s^{%s}' % (sym.latex(var), sym.latex(any)))
def sub_0(var    ): return sub(var, 0)
def sub_1(var    ): return sub(var, 1)
def sub_2(var    ): return sub(var, 2)
def sub_i(var    ): return sub(var, i_)
def sub_k(var    ): return sub(var, k_)
def sub_m(var    ): return sub(var, m_)
def sub_n(var    ): return sub(var, n_)
def sub_t(var    ): return sub(var, t_)
def _dash(var    ): return ss("%s'"               % sym.latex(var) )
def Delta_(var   ): return ss(r'\Delta{%s}'       % sym.latex(var) )### {%s}にスペース開けるとエラー
def delta_(var   ): return ss(r'd%s'              % sym.latex(var) )
def partial_(var ): return ss(r'\partial{%s}'     % sym.latex(var) )
def bar_ (var    ): return ss(r'\bar{%s}'         % sym.latex(var) )
def frac_(up,down): return ss(r'\frac{%s}{%s}'    %(Delta_(up), Delta_(down)))
def diff_(up,down): return ss(r'\frac{d%s}{d%s}'  %(sym.latex(up),sym.latex(down) ))
def part_(up,down): return ss(r'\frac{%s}{%s}'    %(partial_(up),partial_(down) ))
def para_(var,any): return ss(r'%s(%s)' % (var, any))
'''
f01_04 = F(g_, 4*(pi_**2)* h_ / (T_**2))
f01_07 = F(T_ , sub_0(T_) + i_* sub_0(T_)**2 / ( ta_ - i_*sub_0(T_) )  )
f01_10 = F(g_, 4*pi_*pi_*h_*( 1 + 2*r_*r_/(5*h_*h_) + th_*th_/8 )/(T_*T_))
f01_11 = F(h_, _dash(h_)-d_/2)

f05_01 = F( ss('V_{R}(t)')             , R_* ss('I(t)')                         , label='f05_01')
f05_02 = F( ss('q(t)')                 , C_* ss('V_{C}(t)')                     , label='f05_02')
f05_03 = F( ss('I(t)')                 , diff_('q(t)', 't')                     , label='f05_03')
f05_04 = F( ss('V_L(t)')               , -L_*diff_('I(t)', 't')                 , label='f05_04')
f05_05 = F( V_-L_*   diff_('I(t)', 't'), R_* ss('I(t)')+   diff_('q(t)', 't')   , label='f05_05')
f05_06 = F(frac_('d^2I(t)','dt^2')+2*ga_*diff_('I(t)','t')+sub_0(om_)**2*ss('I(t)'), 0, label='f05_06')
f05_07 = F( ss('I(t)'), e_**(-ga_*t_)*(a_*sin(sub_1(om_)*t_)+ b_*cos(sub_1(om_)*t_))  , label='f05_07')
f05_08 = F( ss('I(t)'), e_**(-ga_*t_)*(a_*e_**(sub_1(om_)*t_)+b_*e_**(-sub_1(om_)*t_)), label='f05_08')
f05_09 = F( ss('I(t)'), e_**(-ga_*t_)*(a_*t_+ b_ )                              , label='f05_09')

### f09
f09_N  = F( sin(sub_m(th_))      , m_*la_*N_ )
f09_01 = F( sub(E_, n_)          , -h_*c_*R_/(n_**2)                            , label='f09_01' )
f09_02 = F( h_*nu_               , sub('E',sub_1(n_))-sub('E',sub_2(n_))              , label='f09_02' )
f09_03 = F( 1/la_                , (1/(h_*c_))*(sub('E','n')-sub_2(E_))            , label='f09_03' )
f09_04 = F( d_*sin(sub(th_,m_))  ,  m_* la_                                     , label='f09_04' )
f09_05 = F( sub_m(th_)              , (   sub(th_, L_)-   sub(th_, R_))/2          , label='f09_05' )
f09_06 = F( sub(N_, i_)          , sin(   sub(th_,m_))/(m_*   sub(la_, i_))     , label='f09_06' )
f09_07 = F( la_                  , sin(   sub(th_,m_))/(m_*N_ )                 , label='f09_07' )
f09_08 = F( Delta_(sub_i(N_))/sub_i(N_)  ,sqrt((Delta_(th_)*cos(sub_m(th_))/sin(sub_m(th_)))**2+(Delta_(sub_i(la_))/sub_i(la_))**2), label='f09_08')
f09_09 = F( Delta_(sub_i(la_))/sub_i(la_),
         sqrt((Delta_(th_)*cos(sub_m(th_))/sin(sub_m(th_)))**2+(Delta_(sub_i(N_))/sub_i(N_))**2)  , label='f09_09')

### f11
f11_01 = F(m_*diff_('v', 't')      , -mu_* m_* g_* cos(th_)-la_*mu_+m_*g_*sin(th_) , label='f11_01')
f11_03 = F(bar_('a')   , mu_*g_*cos(th_)+(la_/m_)*v_+(ka_/m_)*v_**2-g_*sin(th_)   , label='f11_03')
f11_04 = F(bar_('a')/g_, mu_*cos(th_)+(la_/m_*g_)*v_+(ka_/m_*g_)*v_**2-g_*sin(th_), label='f11_04')
f11_05 = F(bar_('a')   , (la_/m_)*v_+(ka_/m_)*v_**2                               , label='f11_05')
f11_06 = F(bar_('a')/bar_('v'), (la_/m_)+(ka_/m_)*v_                                , label='f11_06')
f11_07 = F(ep_,(_dash(v_)+_dash(d_)*(la_+ka_*_dash(v_))/m_)/(v_-d_*(la_+ka_*v_)/m_), label='f11_07')
f11_08 = F(d_        , et_*S_/la_                                               , label='f11_08')
f11_09 = F(diff_(v_, t_), -mu_* g_                                                 , label='f11_09')
f11_11 = F(s_        , (   sub_1(v_)**2-   sub_2(v_)**2)/(2*mu_*g_)                   , label='f11_11')
f11_14 = F(s_        , m_*(sub_1(v_)-sub_2(v_))/la_                             , label='f11_14')
f11_15 = F(diff_(v_, t_), -   _dash(ka_)*v_**2                                     , label='f11_15')
f11_16 = F(x_        , (1/   _dash(ka_))*log(1+   _dash(ka_)*   sub_1(v_)*t_)      , label='f11_16')
f11_17 = F(s_        , (m_/ka_)*log(   sub_1(v_)/   sub_2(v_))                        , label='f11_17')
f11_18 = F(diff_(v_, t_), -(   _dash(la_)*v_+   _dash(ka_)*v_**2)                  , label='f11_18')
f11_19 = F(diff_(x_, v_), -1/(   _dash(la_)+   _dash(ka_)*v_)                      , label='f11_19')
f11_20 = F(x_, (m_/ka_)*log((_dash(la_)+_dash(ka_)*sub_1(v_))/(_dash(la_)+_dash(ka_)*v_  ))  , label='f11_20')
f11_21 = F(s_, (m_/ka_)*log((_dash(la_)+_dash(ka_)*sub_1(v_))/(_dash(la_)+_dash(ka_)*sub_2(v_))), label='f11_21' )
f11_22 = F(para_(v_,t_),(la_*sub_1(v_))/((la_+ka_*sub_1(v_))*e_**(la_*t_/m_)-ka_*sub_1(v_)), label='f11_22')
f11_23 = F(para_(x_,t_),(m_/ka_)*log(1+(ka_*sub_1(v_)/la_)*(1-e_**(-la_*t_/m_)))     , label='f11_23')
'''
