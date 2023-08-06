import os
import sys
import subprocess

from tqdm import tqdm
from nbconvert import nbconvertapp, RSTExporter

# my created
from options import nbc_options
from data.load_data import DataLoader

opt = nbc_options.Options().parse()
app = nbconvertapp.NbConvertApp()
loader   = DataLoader()

class Converter:
    def __init__(self):
        # for setting env
        self.os       = opt.os
        self.cwd      = os.getcwd()
        self.dir      = os.path.abspath(os.path.dirname(__file__))
        self.expy     = os.path.join( os.environ['USERPROFILE'] , '.expy')
        self.home     = os.environ['USERPROFILE']
        # for setting args
        self.input    = self.init_input()  #return list of file path as C:\U...
        self.output   = self.init_output()
        self.template = self.init_template()
        self.path     = self.init_path()
        # self.exporter = RSTExporter()

    def init_input(self):
        # no option:[], if no args:None, if args:['name',...]
        all_file= [os.path.join(self.cwd,f) for f in opt.input] if opt.input else []
        if opt.input == opt.all: opt.no_convert=True
        if opt.input:all_dir=[os.path.join(self.cwd,d) for d in opt.input if os.path.isdir(os.path.join(self.cwd,d))]
        elif opt.all:all_dir=[os.path.join(self.cwd,d) for d in opt.all   if os.path.isdir(os.path.join(self.cwd,d))]
        else        :all_dir=[self.cwd] if opt.all==[] else []
        for d in     all_dir:all_file +=[os.path.join(d,f) for f in os.listdir(d)]
        return [f for f in all_file if f[-6:]=='.ipynb' and os.path.isfile(f)]

    def init_output(self):#return format as pdf, html...
        if   opt.to    :return opt.to
        elif opt.output:return opt.output
        else: return 'pdf'

    def init_template(self): #return template
        loader()
        if opt.template:
            if os.path.isfile(os.path.join(self.cwd, opt.template[0])):
                return os.path.join(self.cwd, opt.template[0])
            raise ValueError('No such file\t%s.'%os.path.join(self.cwd, opt.template[0]))
        if   opt.template==[]   : return None
        elif self.output=="pdf" : return loader.latex_temp
        elif self.output=="html": return loader.html_temp
        else:return None

    def init_path(self):
        path = opt.path if opt.path else self.cwd
        return None if opt.path is None else path
    #---------------------------------------------------------------------------
    def __call__(self):
        # action
        if opt.install_tex    :self.install_tex()
        if opt.install_pandoc :self.install_pandoc()
        if opt.reset_template :loader.nofile_list=loader.file_list;loader()
        if opt.debug : self.debug();
        if type(opt.rm)==type([]):self.remove_file()
        if not opt.no_convert :
            self.convert()
            print('Finished')

    def convert(self):
        input  = self.input
        output = opt.output if opt.output else '%s.%s'%(opt.input,self.output)
        for filename in (input if opt.hide_bar else tqdm(input)):
            args = [filename,
                    '--to=%s'%self.output,]
            if opt.no_input : args.append('--no-input')
            if self.template: args.append('--template=%s'  %self.template)
            if self.path    : args.append('--output-dir=%s'%self.path)
            app.initialize(args)
            app.start()
    # another
    def debug(self):
        print('test:\t',opt.test, '\ntype:\t',type(opt.test))

    def install_tex(self):
        if opt.os in ['posix','Debian','Ubuntu']:
            subprocess.run('sudo apt install texlive-xetex texlive-fonts-recommended texlive-generic-recommended')
        if opt.os in ['Windows','nt']: print('\n\tPlease install [MikTex](http://www.miktex.org/)\n')
        if opt.os in ['Mac','Darwin']: print('\n\tPlease install [MacTex](http://tug.org/mactex/)\n')

    def install_pandoc(self):
        if opt.os=='posix'or'Debian'or'Ubuntu':
            subprocess.run('sudo apt install pandoc')
        else : print('\n\tPlease install [Pandoc](https://pandoc.org/installing.html)\n')

    def remove_file(self):
        opt.no_convert=True
        all_file= [os.path.join(self.cwd,f) for f in opt.rm] if opt.rm else []
        if  opt.all:all_dir=[os.path.join(self.cwd,d) for d in opt.all if os.path.isdir(os.path.join(self.cwd,d))]
        elif opt.rm:all_dir=[os.path.join(self.cwd,d) for d in opt.rm  if os.path.isdir(os.path.join(self.cwd,d))]
        else       :all_dir=[self.cwd] if opt.all==[] else []
        for d in    all_dir:all_file +=[os.path.join(d,f) for f in os.listdir(d)]
        all_file= [f for f in all_file if f[-len(self.output):]==self.output and os.path.isfile(f)]

        for f in all_file: print('\t%s'%f)
        print('already delete this file ?\t[y/n]')
        val = input()
        if val in ['y','yes']:
            try:
                for f in tqdm(all_file): os.remove(f)
            except:
                pass
        print('Finished.')

def main():
    conv = Converter()
    conv()

if __name__ == '__main__':
    main()
