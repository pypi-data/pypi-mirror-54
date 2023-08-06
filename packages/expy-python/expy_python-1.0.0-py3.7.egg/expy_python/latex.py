'''3.to_latex-------------------------------------------------------------------------'''
#LaTeX_cmd
begin1 = r'\begin{align}'+'\n'+'\t'#there is x
begin2 = '&='                         #there is func
newln  = r'\\'+'\n' + '\t\t&='
end1   = r'\mathrm{'                   #there is rm
end2   = r'}\\'+'\n\t'+r'\label{'      #there is label
end3   = '}'+'\n'+r'\end{align}'
# Setting
def print_latex(text):
    latex=text.replace('\t','').split('\n')
    h = len(latex)
    for i in range(len(latex)):
        t=latex[i];
        print(str(i+1)+'>  '+t)
        if not('begin'in t or 'end' in t):
            plt.figure(figsize=(1, 0.5))
            if '&=' in t:
                t=t.replace('&=','').replace('\\\\','')
                plt.text(0,1,'\t\t=  $'+t+r'$',size='25',va='center',alpha=0.9)
            else:
                plt.text(0,1,'$'+t+r'$',size='25',va='center',alpha=0.9)
            plt.axis('off')
            plt.show()

#基本型
def to_latex(s='%%',answer=0, x='%%', rm='%%',p=0,label=''):
    tex = begin1+x+begin2+ s +newln+ str(answer) +end1+rm+end2+label+end3
    print('')
    plt.show()
    if p!=0: print_latex(tex);return tex
    else:           copy(tex);return tex
def align_latex(unit=[],label='',p=0,s=''):
    tex=''
    for i in range(len(unit)):
        if i!=0:tex+='='
        tex +=sym.latex(unit[i])
    begin = r'\begin{align}'+'\n\t'
    end   = '\n\t'+'\label{'+label+'}'+'\n\t'+r'\end{align}'
    tex = begin + tex + s + end
    if p!=0: print_latex(tex);return tex
    else:           copy(tex);return tex
def align_asta_latex(unit=[],p=0):
    tex=''
    for i in range(len(unit)):
        if i!=0:tex+='\n\t&='
        tex +=sym.latex(unit[i])
        if i!=0:tex+=r'\\'
    tex = r'\begin{align*}'+'\n\t'+tex+'\n\t'+r'\end{align*}'
    if p!=0: print_latex(tex);return tex
    else:           copy(tex);return tex

# 計算式をそのままLaTeX出力
def func_to_latex(func,sym_all=[],val_all=[],rm_all=None,
                  sym_ans='%%',dig_ans=3,rm_ans='%%',p=0):
    if type(sym_ans)is not str:
        sym_ans = sym.latex(sym_ans)
    def func_sym_to_val(func,sym_all,val_all,rm_all):
        if  rm_all is None:
            rm_all=['',]*len(sym_all)
        sym_str = [];
        for i in sym_all:
            sym_str.append(sym.Symbol('%'+sym.latex(i)+'%'));
        ### print(0,func);print(0.1,sym_all);print(0.2,sym_str)
        func_str = ep.subs(func,sym_all,sym_str)                ;### print(1,func_str)###
        func_str = sym.latex(func_str)                          ;### print(2,func_str)###
        for i,j in zip(['0','1','2','3','4','5','6','7','8','9'],['0%','1%','2%','3%','4%','5%','6%','7%','8%','9%']):
            func_str = func_str.replace(i,j)
        ### print(0,func);print(0.1,sym_all);print(0.2,sym_str)
        ### func_str = func_str.replace(' ','')                 ;### print(3,func_str)
        func_str = func_str.replace('%%',r'\times ')            ;### print(4,func_str)
        for i in range(len(sym_all)):
            func_str=func_str.replace(
                str(sym.latex(sym_str[i])),
                str(round(val_all[i],3))+r'\mathrm{'+rm_all[i]+'}'
            )
        func_str=func_str.replace('%','')                       ;### print(5,func_str)
        print(6,func_str)
        return func_str
    def func_to_ans(func,sym_all,val_all,dig_ans,rm_ans):
        ans = ep.subs(func,sym_all,val_all);
        ans = np.round(float(ans),int(dig_ans+dig_ans))
        ans = str(ans)+rm_ans#[:len(ans)-dig_ans]+r'\hbox{\sout{'+ans[:dig_ans]+'}'+rm_ans
        return ans
    def func_to_rslt(func,sym_all,val_all,dig_ans,rm_ans):
        ans = ep.subs(func,sym_all,val_all)
        ans = ep.to_sgnf_fig(float(ans), dig_ans)+rm_ans
        return ans

    latex_text = ep.align_asta_latex([
        sym_ans,func,
        func_sym_to_val(func,sym_all,val_all,rm_all),
        func_to_ans(func,sym_all,val_all,dig_ans,rm_ans),
        func_to_rslt(func,sym_all,val_all,dig_ans,rm_ans),
    ],0)

    if p!=0: print_latex(latex_text);return latex_text
    else:           copy(latex_text);return latex_text

#分数型
def frac_to_latex(denom,numer, answer=0, x='%%', rm='%%',p=0,label=''):
    return to_latex(r'\frac{'+denom+'}{'+numer+'}', answer, x,rm,p,label)
#平均
def mean_to_latex(data, x='%%', rm='%%',p=0,label=''):
    denom =  ''
    for i in range(len(data)):
        if i != 0:denom=denom+'+'
        denom += str(data[i])+rm
    #LaTeX作成
    return frac_to_latex(denom,str(len(data)), np.mean(data), x, rm,p,label)
#不確かさ
def uncrt_to_latex(data, x='%%', rm='%%',p=0,label=''):
    N=len(data);m=np.mean(data);u=uncrt(data)
    #LaTeX作成
    s = '\\sqrt{\\frac{1}{'+str(N)+'\\cdot'+str(N-1)+'}\\sum_{i=1}^'+str(N)+'('+x+'_i-'+str(m)+')^2}'
    return to_latex(s, uncrt(data), 'Δ'+x,rm,p,label)
#重平均
def mean_sq_to_latex(data, x='%%', rm='%%',p=0,label=''):
    denom =  ''
    for i in range(len(data)):
        if i != 0:denom=denom+'+'
        denom+= '('+str(data[i])+')^{2}'
    #LaTeX作成
    return to_latex(r'\sqrt{'+denom+'}', mean_sq(data), x, rm,p,label)
#  合成標準不確かさ（非推奨）
def syn_uncrt_to_latex(func=sym.Symbol('f'),
                       uncrt_sym=[],
                       uncrt_all=[],
                       sym_all=[sym.Symbol('f')],
                       uncrt_unit_all=[0],
                       rm_all =[],
                       x='%%',rm='%%',p=0,label=''):
    ans,partial_all,all_sym_to_val,uncrt_unit_all = syn_uncrt(func,uncrt_sym,uncrt_all,
                                                              sym_all,uncrt_unit_all,rm_all,1)
    print([partial_all,'<<<>>>',all_sym_to_val,'<<<>>>',uncrt_unit_all])
    func1 = ''#各偏微分しそうな二乗和平均
    func2 = ''#各偏微分した二乗和平均
    func3 = ''#各変数を代入した二乗和平均
    func4 = ''#各計算したInt二乗和平均
    for i in range(len(uncrt_all)):
        if i!=0:func1=func1+'+';func2=func2+'+';func3=func3+'+';func4=func4+'+'
        diff_denom=sym.Symbol(r'\partial '+x)
        diff_numor=sym.Symbol(r'\partial '+str(uncrt_sym[i]))
        func1 = func1 + '('+sym.latex(diff_denom/diff_numor)+')^{2}'+r'\Delta '+str(uncrt_sym[i])+'^2'
        func2 = func2 + partial_all[i]
        func3 = func3 + all_sym_to_val[i]
        func4 = func4 + '('+str(uncrt_unit_all[i])+')^{2}'
    else:
        func1 = r'\sqrt{'+func1+'}'
        func2 = r'\sqrt{'+func2+'}'
        func3 = r'\sqrt{'+func3+'}'
        func4 = r'\sqrt{'+func4+'}'
    #for i in range(len(uncrt_unit_all)):
    return to_latex(func1+'\n\t&='+func2+'\n\t&='+func3+'\n\t&='+func4,ans,r'\Delta '+x,rm,p,label)
#  合成標準不確かさ（新型）
def syn_to_latex(func,sym_all=[],val_all=[],uncrt_all=[],rm_all=[],
                  sym_ans='%%',dig_ans=3,rm_ans='%%',p=0):
    if type(sym_ans)is not str:
        sym_ans = sym.latex(sym_ans)
    def func_sym_to_val(func,sym_all,val_all,rm_all):
        if  rm_all is None:
            rm_all=['',]*len(sym_all)
        sym_str = [];
        for i in sym_all:
            sym_str.append(sym.Symbol('%'+sym.latex(i)+'%'));
        ### print(0,func);print(0.1,sym_all);print(0.2,sym_str)
        func_str = ep.subs(func,sym_all,sym_str)                ;### print(1,func_str)###
        func_str = sym.latex(func_str)                          ;### print(2,func_str)###
        for i,j in zip(['0','1','2','3','4','5','6','7','8','9'],['0%','1%','2%','3%','4%','5%','6%','7%','8%','9%']):
            func_str = func_str.replace(i,j)
        ### print(0,func);print(0.1,sym_all);print(0.2,sym_str)
        ### func_str = func_str.replace(' ','')                 ;### print(3,func_str)
        func_str = func_str.replace('%%',r'\times ')            ;### print(4,func_str)
        for i in range(len(sym_all)):
            func_str=func_str.replace(
                str(sym.latex(sym_str[i])),
                str(round(val_all[i],3))+r'\mathrm{'+rm_all[i]+'}'
            )
        func_str=func_str.replace('%','')                       ;### print(5,func_str)
        print(6,func_str)
        return func_str

    def func_to_ans(funct,sym_all,val_all,dig_ans):
        ans = ep.subs(func,sym_all,val_all)              ;### print(1,ans)
        ans = ep.subs(ans,sym_all,val_all)               ;### print(2,ans)
        ans = np.round(float(ans),int(dig_ans+dig_ans))  ;### print(3,ans)
        return ans
    def func_to_uncrt(func,sym_all,val_all,dig_ans,rm_ans):
        ans = ep.subs(func,sym_all,val_all);print(ans)   ;### print(1,ans)
        ans = np.round(float(ans),int(dig_ans+dig_ans))  ;### print(2,ans)
        ans = str(ans)                                   ;### print(3,ans)
        ans = ans+rm_ans                                 ;### print(4,ans)
        return ans
    def func_to_rslt(func,sym_all,val_all,dig_ans,rm_ans):
        ans = ep.subs(func,sym_all,val_all)
        ans = ep.to_sgnf_fig(float(ans), dig_ans)+rm_ans
        return ans
    func_todiff=0
    func_diffed=0
    todiff     =[]  ### 偏微分前
    diffed     =[]  ### 偏微分後
    sym_uncrt  =[]
    for s in sym_all:
        todiff.append(sym.Symbol('\partial '+sym_ans)/sym.Symbol('\partial '+sym.latex(s)))
        diffed.append(diff(func,s))
        sym_uncrt.append(sym.Symbol('Δ'+sym.latex(s)))
        func_todiff=func_todiff+(sym.Symbol('\partial '+sym_ans)**2/sym.Symbol('\partial '+sym.latex(s))**2)*(sym.Symbol('Δ'+sym.latex(s))**2)
        func_diffed=func_diffed+(diff(func,s)**2)*(sym.Symbol('Δ'+sym.latex(s))**2)
    syms = to_list(sym_all)+sym_uncrt
    syms.append(sym.Symbol(sym_ans))                             ;### display(1,syms)
    vals = to_list(val_all)+to_list(uncrt_all)
    vals.append(float(func_to_ans(func,sym_all,val_all,dig_ans)));### display(2,vals)
    rms  = rm_all + rm_all
    rms.append(rm_ans)                                           ;### display(3,rms)
    func_todiff = sym.Symbol(sym_ans)*sqrt(func_todiff)
    func_diffed = sym.Symbol(sym_ans)*sqrt(func_diffed)

    latex_text = ep.align_asta_latex([
        'Δ'+sym_ans,
        func_todiff,                                          ### 偏微分前
        func_diffed,                                          ### 偏微分後
        func_sym_to_val(func_diffed,syms,vals,rms),           ### 値代入後
        func_to_uncrt(  func_diffed,syms,vals,dig_ans,rm_ans),### 答え
        func_to_rslt(   func_diffed,syms,vals,dig_ans,rm_ans),### Round
    ],0)

    if p!=0: print_latex(latex_text);return latex_text
    else:           copy(latex_text);return latex_text

def weighted_mean_to_latex(mean_all, uncrt_all, x='%%', rm='%%',p=0,label=''):
    denom = ''#分子
    numer = ''#分母
    for i in range(len(mean_all)):
        denom += '\\frac{'+str(mean_all[i])+'}{('+str(uncrt_all[i])+')^2}'
        numer += '\\frac{1}{('+str(uncrt_all[i])+')^2}'
        if i != len(mean_all)-1:
            denom += '+'
            numer += '+'
    #LaTeX作成
    return frac_to_latex(denom,numer,weighted_mean(mean_all,uncrt_all)[0],x,rm,p,label)

def weighted_uncrt_to_latex(mean_all, uncrt_all,x='%%', rm='%%',p=0,label=''):
    numer = '\\sqrt{'#分母
    for i in range(len(mean_all)):
        numer += '\\frac{1}{('+str(uncrt_all[i])+')^2}'
        if i != len(mean_all)-1:
            numer += '+'
        if i == len(mean_all)-1:
            numer += '}'#sqrt
    #LaTeX作成
    return frac_to_latex('1',numer,weighted_mean(mean_all,uncrt_all)[1],x,rm,p,label)

#表出力
def df_to_latex(df,label='%%%%',c=None,i=False,p=0):
    txt_bgn = '\\begin{table}[htb]\\label{'+label+'}\n\t\\centering\n\t\\caption{'+label+'}\n'
    txt_end = '\t\\end{table}\n'
    latex = df.to_latex(index=i,columns=c,escape=False)
    if p!=0:print( txt_bgn + latex + txt_end )
    else:    copy( txt_bgn + latex + txt_end )
def alnm():
    txt=paste();s='';pi=''
    for i in txt:
        if not pi.isalnum() and     i.isalnum():s=s+'$'+i
        if     pi.isalnum() and not i.isalnum():s=s+ i +'$'
        if not isinstance(i, unicode):s=s
        if i==' ' :s=s
        if i=='．':s=s
        if i=='，':s=s
        if i=='。':s=s+'.'
        if i=='、':s=s+','
        else:s=s+i
        pi=i
