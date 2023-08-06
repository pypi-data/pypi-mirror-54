import os
import argparse

FORMAT = ['asciidoc','custom','html','html_ch','html_embed',
          'html_toc','html_with_lenvs','html_with_toclenvs',
          'latex','latex_with_lenvs','markdown','notebook',
          'pdf','python','rst','script', 'selectLanguage',
          'slides', 'slides_with_lenvs']

class Options():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        #self.save = True
        self.initialized = False

    def initialize(self):
        # for setting input
        self.parser.add_argument('-a', '--all'   ,type=str ,nargs='*',default=None,help='Convert all file of dir')
        self.parser.add_argument('-i', '--input' ,type=str ,nargs='*',default=None,help='Input file to convert')

        # for setting output
        self.parser.add_argument('-p', '--path'  ,type=str ,nargs='*',default=None,help='Specify conved output path')
        self.parser.add_argument('-o', '--output',type=str ,default=None,help='Format detail..`$nbc -o -h`')
        self.parser.add_argument('--to'          ,type=str ,default=None,help='Format detail..`$nbc -o -h`(-p is equal --to)')
        #self.parser.add_argument('--max-size'    ,type=bool,default='True',help='??:int')

        # for setting converter
        self.parser.add_argument('-t','--template',type=str ,nargs='*',default=None,help='user template file')
        self.parser.add_argument('--no-input'     ,action='store_false',help='Hide input cells')
        #self.parser.add_argument('-l','--latex'   ,type=str, default='' ,help='')
        #self.parser.add_argument('--addtofile'    ,action='store_false' ,help='Set new dir and add pdf to this')

        # for action
        self.parser.add_argument('-r','--rm'        ,type=str,nargs="*",default=None,help='Remove file')
        self.parser.add_argument('-n','--no-convert',action='store_true',help='Stop convert to pdf')
        self.parser.add_argument('--install-tex'    ,action='store_true',help='Install tex    for Linux')
        self.parser.add_argument('--install-pandoc' ,action='store_true',help='Install pandoc for Linux')
        self.parser.add_argument('--reset-template' ,action='store_true',help='Delete and recreate ~/.expy')

        # for env
        self.parser.add_argument('-d','--debug',action='store_true',help='Set log level to DEBUG')
        self.parser.add_argument('-e','--error',action='store_true',help='Set log level to ERROR')
        self.parser.add_argument('--os'        ,type=str,default=os.name,help='Choose OS of your pc')
        self.parser.add_argument('--hide-bar'  ,action='store_true',help='Hide the wget progress bar')
        #self.parser.add_argument('--hidewarn'  ,action='store_true',help='Hide Warnings. ')

    def parse(self, save=True):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt
