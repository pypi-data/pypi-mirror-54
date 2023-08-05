import os,sys,numpy
import matplotlib.pyplot as plt
from matplotlib import rc
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from .atominfo import atom_list
from .fitfort import fit_fort
from .fortread import read_fort13,read_fort26
from .getdv import get_dv
from .createchunks import create_chunks
from .checkshift import check_shift
from .plotfit import plot_fit

def make_figure(fortfile,atomdir='./atom.dat',details=False,dispersion=0.01,dvplot=None,error=False,
                extra=None,fit=False,getwave=False,header=None,illcond=False,nores=False,
                output=(datetime.now()).strftime('%y%m%d-%H%M%S'),show=False,unscale=False,
                version='vpfit',vpsetup='./vp_setup.dat',zmid=None,cont=False):
    '''
    Main function to create velocity plot.

    Parameters
    ----------
    fortfile : str
      fort.13 file to be read
    atomdir : str
      Path to a custom atom.dat
    details : bool
      Plot individual Voigt profiles
    dispersion : float
      Spectral velocity dispersion for high-resolution individual Voigt profiles
    dvplot : float
      Custom velocity range for plotting
    error : bool
      Run VPFIT only once to get error estimates
    extra : str
      Add vertical line to identify specific region. Multiple velocities
      can be specified by using the colon symbol (:) to separate the values.
    fit : bool
      Run VPFIT and embed final results in fort.13
    getwave : bool
      Get wavelength array from the spectrum
    header : str
      List of transition IDs of each fitting region
    illcond : bool
      Run VPFIT with ill-conditioning
    nores : bool
      Do no plot the residuals
    output : str
      Give custom output filename
    show : bool
      Flag whether the figure is shown using Python interface.
    unscale : bool
      Don't correct the data and distort the models
    version : str
      Path to a custom vpfit executable
    vpsetup : str
      Path to a custom vp_setup.dat
    zmid : float
      Central redshift to plot transitions

    Examples
    --------
    As executables:

    >>> velplot fort.13 --output turbulent --version vpfit10 --header header.dat

    As Python script:

    >>> import velplot
    >>> velplot.make_figure(fortfile='fort.13',header='header.dat',show=True,details=True,getwave=True)
    '''
    # Move for fort file location
    current_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(fortfile)))
    fortfile = fortfile.split('/')[-1]
    # Set up atomic transition list
    os.environ['ATOMDIR'] = atomdir
    if os.path.exists(atomdir):
        atom = atom_list(atomdir)
    else:
        print('ERROR: atom.dat not found...')
        quit()
    # Set up VPFIT settings
    os.environ['VPFSETUP'] = vpsetup
    if os.path.exists(vpsetup)==True:
        pcvals,lastchtied,daoaun = False,'z',1
        for line in numpy.loadtxt(vpsetup,dtype='str',delimiter='\n'):
            if 'pcvals' in line and line.split()[0][0]!='!':
                pcvals = True
            if 'lastchtied' in line and line.split()[0][0]!='!':
                lastchtied = line.split()[1].lower()
            if 'daoaun' in line and line.split()[0][0]!='!':
                daoaun = float(line.split()[1])
    else:
        print('ERROR: vp_setup.dat not found...')
        quit()
    # Remove previously created chunks
    if os.path.exists('./chunks/')==True:
        os.system('rm -rf chunks/')
    if fit or error or illcond:
        fit_fort(fortfile,fit,error,illcond,pcvals,version)
        os.system('mv fort.18 '+fortfile.replace('.13','.18'))
        os.system('mv fort.26 '+fortfile.replace('.13','.26'))
    if fortfile.split('.')[-1]=='13' or fortfile.split('.')[0]=='f13':
        header,comment,table1,table2 = read_fort13(fortfile,header,lastchtied,atom)
    if fortfile.split('.')[-1]=='26' or fortfile.split('.')[0]=='f26':
        header,comment,table1,table2 = read_fort26(fortfile,header,lastchtied,atom)
    dv,zmid = get_dv(dvplot,zmid,header,table1,comment)
    header = create_chunks(fortfile,table1,header,pcvals,version,cont)
    rc('font', size=2, family='serif')
    rc('axes', labelsize=2, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=8)
    rc('ytick', labelsize=8)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    if show:
        fig = plt.figure(figsize=(9,2*len(table1)),frameon=False,dpi=200)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.96, wspace=0, hspace=0)
        for i in range(len(table1)):
            ax = fig.add_subplot(len(table1),1,i+1,xlim=[-dv,dv],ylim=[-0.6,2.1])
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
            if extra!=None:
                for extrav in extra.split(':'):
                    ax.axvline(float(extrav),color='0.5',ls='dotted',lw=0.8)
            ax.text(-dv,1.6,r'$-1\sigma$  ',ha='right',va='center',size=8)
            ax.text(-dv,1.8,r'$+1\sigma$  ',ha='right',va='center',size=8)
            if i==0: plt.title(os.path.abspath(fortfile),fontsize=7)
            if i+1<len(table1): plt.setp(ax.get_xticklabels(), visible=False)
            else: ax.set_xlabel('Velocity relative to $z_{abs}=%.6f$ (km/s)'%zmid,fontsize=10)
            print(header[i,0],header[i,1],table1[i][0],'chunks/vpfit_chunk'+'%03d'%(i+1))
            shift,cont,slope,z,zero = check_shift(i,dv,table1,table2,header,comment)
            plot_fit(i,daoaun,nores,unscale,getwave,details,table1,table2,header,
                     atom,comment,shift,cont,slope,z,zero,dv,dispersion,zmid)
        plt.show()
    else:
        pdf_pages = PdfPages(output+'.pdf')
        i=0
        while (i<len(table1)):
            f   = 1             
            ref = i + 6          # position in table1 to define where to create new plotting page
            fig = plt.figure(figsize=(8.27, 11.69))
            plt.axis('off')
            plt.subplots_adjust(left=0.1, right=0.9, bottom=0.06, top=0.96, wspace=0, hspace=0)
            while i<len(table1) and i<ref:
                ax = fig.add_subplot(6,1,f,xlim=[-dv,dv],ylim=[-0.6,2.1])
                ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
                if extra!=None:
                    for extrav in extra.split(':'):
                        ax.axvline(float(extrav),color='0.5',ls='dotted',lw=0.8)
                ax.text(-dv,1.6,r'$-1\sigma$ ',ha='right',va='center',size=8)
                ax.text(-dv,1.8,r'$+1\sigma$ ',ha='right',va='center',size=8)
                if f==1: plt.title(os.path.abspath(fortfile),fontsize=7)
                if i+1!=ref and i+1!=len(table1): plt.setp(ax.get_xticklabels(), visible=False)
                else: ax.set_xlabel('Velocity relative to $z_{abs}=%.6f$ (km/s)'%zmid,fontsize=10)
                print(header[i,0],header[i,1],table1[i][0],'chunks/vpfit_chunk'+'%03d'%(i+1))
                shift,cont,slope,z,zero = check_shift(i,dv,table1,table2,header,comment)
                plot_fit(i,daoaun,nores,unscale,getwave,details,table1,table2,header,
                         atom,comment,shift,cont,slope,z,zero,dv,dispersion,zmid)
                i = i + 1
                f = f + 1
            pdf_pages.savefig(fig)
        pdf_pages.close()
    os.system('rm -rf chunks/')
    os.chdir(current_dir)
