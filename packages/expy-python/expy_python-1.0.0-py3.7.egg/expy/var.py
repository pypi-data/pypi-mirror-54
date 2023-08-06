import sympy as sym

from sympy import symbols as ss
from sympy import sqrt,sin,cos,tan,exp,log,diff

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
def diff_(up,down): return ss(r'\frac{d%s}{d%s}'  %(sym.latex(de_),sym.latex(up) ))
def part_(up,down): return ss(r'\frac{%s}{%s}'    %(partial_(pa_),partial_(up) ))
def para_(var,any): return ss(r'%s(%s)' % (var, any))

version= '1.0.0'
### グローバル変数定義
DATAPATH    = './data'
LATEXPATH   = './data/LaTeX'
LATEXDATAPATHconst= './data/LaTeX/data'

### 実験定数
c    = 2.99792458 *10**8
g    = 9.80665
g_0  = 9.7978872
G    = 6.67384    *10**-1
m_e  = 9.10938291 *10**-31
m_p  = 1.672621777*10**-27
m_u  = 1.660538921*10**-27
e    = 1.602176565*10**-19
h    = 6.62606957 *10**-34
k    = 1.3806488  *10**-23
N_A  = 6.02214129 *10**-23
R    = 8.3144621
mu_0 = 1.256637061*10**-6
ep_0 = 8.854187817*10**-12

### 環境変数
temperature= 0.0### 温度
pressure   = 0.0### 気圧
humidity   = 0.0### 湿度
weather    = 'hare'### 天気

### 標準器の誤差
n_cm  = 0.005   ### ノギス
n_mm  = 0.05    ### ノギス
k_cm   = 0.005  ### 金尺
k_mm   = 0.05   ### 金尺
p_s    = 0.0001 ### パルス
t_s    = 0.005  ### タイマー
h_s    = 1.0    ### タイマー

greek_char    = 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau upsilon phi chi psi omega \\partial'
Greek_char    = 'Gamma Lambda Sigma Psi Delta Xi Upsilon Omega Theta Pi Phi sum prod'
alphabet_char = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
Alphabet_char = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'

greek_var = 'al_ be_ ga_ de_ ep_ ze_ et_ th_ io_ ka_ la_ mu_ nu_ xi_ pi_ rh_ si_ ta_ up_ ph_ ch_ ps_ om_ pa_'
Greek_var = 'Ga_ La_ Si_ Ps_ De_ Xi_ Up_ Om_ Th_ Pi_ Ph_ su_ pr_'
alphabet_var = 'a_ b_ c_ d_ e_ f_ g_ h_ i_ j_ k_ l_ m_ n_ o_ p_ q_ r_ s_ t_ u_ v_ w_ x_ y_ z_'
Alphabet_var = 'A_ B_ C_ D_ E_ F_ G_ H_ I_ J_ K_ L_ M_ N_ O_ P_ Q_ R_ S_ T_ U_ V_ W_ X_ Y_ Z_'

global a_,b_,c_,d_,e_,f_,g_,h_,i_,j_,k_,l_,m_,n_,o_,p_,q_,r_,s_,t_,u_,v_,w_,x_,y_,z_

(a_,b_,c_,d_,e_,f_,g_,h_,i_,j_,k_,l_,m_,n_,o_,p_,q_,r_,s_,t_,u_,v_,w_,x_,y_,z_
) = sym.symbols(alphabet_char)
(A_,B_,C_,D_,E_,F_,G_,H_,I_,J_,K_,L_,M_,N_,O_,P_,Q_,R_,S_,T_,U_,V_,W_,X_,Y_,Z_
) = sym.symbols(Alphabet_char)
(al_,be_,ga_,de_,ep_,ze_,et_,th_,io_,ka_,la_,mu_,nu_,xi_,
pi_,rh_,si_,ta_,up_, ph_,ch_,ps_,om_,pa_
)=sym.symbols(greek_char)
(Ga_,La_,Si_,Ps_,De_,Xi_,Up_,Om_,Th_,Pi_,Ph_,su_,pr_
)=sym.symbols(Greek_char)
def alphabet():
    return [a_,b_,c_,d_,e_,f_,g_,h_,i_,j_,k_,l_,m_,n_,o_,p_,q_,r_,s_,t_,u_,v_,w_,x_,y_,z_,
            A_,B_,C_,D_,E_,F_,G_,H_,I_,J_,K_,L_,M_,N_,O_,P_,Q_,R_,S_,T_,U_,V_,W_,X_,Y_,Z_]
def greek():
    return [al_,be_,ga_,de_,ep_,ze_,et_,th_,io_,ka_,la_,mu_,nu_,xi_,
            pi_,rh_,si_,ta_,up_, ph_,ch_,ps_,om_,pa_,
            Ga_,La_,Si_,Ps_,De_,Xi_,Up_,Om_,Th_,Pi_,Ph_,su_,pr_]
def math():
    return [ss,sub,sup,sub_0,sub_1,sub_2,sub_i,sub_k,sub_m,sub_n,
    _dash,Delta_,delta_,partial_,bar_,frac_,diff_,part_,para_]
