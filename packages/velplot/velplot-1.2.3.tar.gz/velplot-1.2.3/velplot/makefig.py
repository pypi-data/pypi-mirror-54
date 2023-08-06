import os,sys,numpy,shutil
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from .atominfo import atom_list
from .fortread import read_fort13,read_fort26
from .getdv import get_dv
from .checkshift import check_shift
from .plotfit import plot_fit
from .vpfitrun import make_setup,fit_fort,create_chunks

def make_figure(fortfile,atomdir='./atom.dat',details=False,dispersion=0.01,dv=None,error=False,
                extra=None,fit=False,getwave=False,header=None,illcond=False,nores=False,
                output=(datetime.now()).strftime('%y%m%d-%H%M%S'),save2pdf=None,unscale=False,
                vpfit='vpfit',vpsetup='./vp_setup.dat',zmid=None,cont=False,ncols=None,nrows=None,
                pubstyle=False,seaborn=False,posidx=None):
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
    dv : float
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
    save2pdf : bool
      Save figure to PDF file
    unscale : bool
      Don't correct the data and distort the models
    vpfit : str
      Path to a custom vpfit executable
    vpsetup : str
      Path to a custom vp_setup.dat
    zmid : float
      Central redshift to plot transitions

    Examples
    --------
    As executables:

    >>> velplot fort.13 --output turbulent --vpfit vpfit10 --header header.dat

    As Python script:

    >>> import velplot
    >>> velplot.make_figure(fortfile='fort.13',header='header.dat',details=True,getwave=True)
    '''
    # Extract custom transition position if available
    if type(posidx)==str:
        posidx = numpy.loadtxt(posidx)
    if type(posidx)==list:
        posidx = numpy.array(posidx)
    # Get full path to VPFIT dependencies
    if atomdir!='./atom.dat': atomdir = os.path.abspath(atomdir)
    if vpsetup!='./vp_setup.dat': vpsetup = os.path.abspath(vpsetup)
    vpfit = os.path.abspath(vpfit) if os.path.exists(vpfit) else shutil.which(vpfit)
    # Move for fort file location
    current_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(fortfile)))
    fortfile = fortfile.split('/')[-1]
    # Prepare setup files
    atom,pcvals,lastchtied,daoaun = make_setup(atomdir,vpsetup)
    # Perform fitting is requested
    if fit or error or illcond:
        fit_fort(fortfile,fit,error,illcond,pcvals,vpfit)
        os.system('mv fort.18 '+fortfile.replace('.13','.18'))
        os.system('mv fort.26 '+fortfile.replace('.13','.26'))
    # Extract model details
    if fortfile.split('.')[-1]=='13' or fortfile.split('.')[0]=='f13':
        header,comment,table1,table2 = read_fort13(fortfile,lastchtied,atom,header)
    if fortfile.split('.')[-1]=='26' or fortfile.split('.')[0]=='f26':
        header,comment,table1,table2 = read_fort26(fortfile,lastchtied,atom,header)
    dvmin,dvmax,zmid = get_dv(header,table1,comment,dv,zmid)
    header = create_chunks(fortfile,table1,header,pcvals,vpfit,cont)
    # Use seaborn style if requested
    if seaborn: plt.style.use('seaborn')
    # Select standard or publishing style
    if pubstyle:
        plt.rc('font',   size=10, family='sans-serif')
        plt.rc('axes',   labelsize=10, linewidth=0.2)
        plt.rc('legend', fontsize=10, handlelength=5)
        plt.rc('xtick',  labelsize=8)
        plt.rc('ytick',  labelsize=8)
        plt.rc('lines',  lw=0.2, mew=0.2)
    else:
        plt.rc('font', size=2, family='serif')
        plt.rc('axes', labelsize=2, linewidth=0.2)
        plt.rc('legend', fontsize=2, handlelength=10)
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('lines', lw=0.2, mew=0.2)
        plt.rc('grid', linewidth=0.2)
    if save2pdf==1:
        pdf_pages = PdfPages(current_dir+'/'+output+'.pdf')
        i=0
        while (i<len(table1)):
            f   = 1
            ref = i + 6          # position in table1 to define where to create new plotting page
            fig = plt.figure(figsize=(8.27, 11.69))
            plt.axis('off')
            plt.subplots_adjust(left=0.1, right=0.9, bottom=0.06, top=0.96, wspace=0, hspace=0)
            while i<len(table1) and i<ref:
                ax = fig.add_subplot(6,1,f,xlim=[dvmin,dvmax],ylim=[-0.6,2.1])
                ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
                if extra!=None:
                    for extrav in extra.split(':'):
                        ax.axvline(float(extrav),color='0.5',ls='dotted',lw=0.8)
                ax.text(dvmin,1.6,r'$-1\sigma$ ',ha='right',va='center',size=8)
                ax.text(dvmin,1.8,r'$+1\sigma$ ',ha='right',va='center',size=8)
                if f==1: plt.title(os.path.abspath(fortfile),fontsize=7)
                if i+1!=ref and i+1!=len(table1): plt.setp(ax.get_xticklabels(), visible=False)
                else: ax.set_xlabel('Velocity relative to $z_{abs}=%.6f$ (km/s)'%zmid,fontsize=10)
                print(header[i,0],header[i,1],table1[i][0],'chunks/vpfit_chunk'+'%03d'%(i+1))
                shift,cont,slope,z,zero = check_shift(i,dvmin,dvmax,table1,table2,header,comment)
                plot_fit(i,table1,table2,header,atom,comment,             # Output of read_fort13 or read_fort26
                         shift,cont,slope,z,zero,                         # Output of check_shift
                         dvmin,dvmax,zmid,                                # Output of get_dv
                         dispersion,daoaun,nores,unscale,getwave,details  # User-defined, have default values
                         )
                i = i + 1
                f = f + 1
            pdf_pages.savefig(fig)
        pdf_pages.close()
    else:
        if ncols!=None:
            fraction = len(table1)/ncols
            nrows = int(fraction+1) if float(fraction)/int(fraction)>1 else int(fraction)
            figsize = (8.27,11.69/6*nrows)
        elif nrows!=None:
            fraction = len(table1)/nrows
            ncols = int(fraction+1) if float(fraction)/int(fraction)>1 else int(fraction)
            figsize = (8.27,11.69/6*nrows)
        else:
            figsize = (8.27,2*len(table1))
            nrows = len(table1)
            ncols = 1
        fig = plt.figure(figsize=figsize,frameon=False,dpi=150)
        #plt.subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.96, wspace=0, hspace=0)
        plt.subplots_adjust(left=0.07,right=0.97,bottom=0.07,top=0.98,wspace=0.05,hspace=0.05)
        for i in range(len(table1)):
            ylimit = [-0.35,1.9] if pubstyle else [-0.6,2.1]
            idx = i+1 if type(posidx)==type(None) else posidx[i]
            ax = fig.add_subplot(nrows,ncols,idx,xlim=[dvmin,dvmax],ylim=ylimit)
            if extra!=None:
                for extrav in extra.split(':'):
                    ax.axvline(float(extrav),color='0.5',ls='dotted',lw=0.8)
            ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
            if (idx-1)%ncols==0:
                if pubstyle==False:
                    ax.text(dvmin,1.6,r'$-1\sigma$  ',ha='right',va='center',size=8)
                    ax.text(dvmin,1.8,r'$+1\sigma$  ',ha='right',va='center',size=8)
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
            if idx<len(table1)-ncols:
                plt.setp(ax.get_xticklabels(), visible=False)
            print(header[i,0],header[i,1],table1[i][0],'chunks/vpfit_chunk'+'%03d'%(i+1))
            shift,cont,slope,z,zero = check_shift(i,dvmin,dvmax,table1,table2,header,comment,pubstyle)
            plot_fit(i,table1,table2,header,atom,comment,             # Output of read_fort13 or read_fort26
                     shift,cont,slope,z,zero,                         # Output of check_shift
                     dvmin,dvmax,zmid,                                # Output of get_dv
                     dispersion,daoaun,nores,unscale,getwave,details, # User-defined, have default values
                     pubstyle
            )
        fig.text(0.5, 0.02, 'Velocity relative to $z_{abs}=%.6f$ (km/s)'%zmid, ha='center',fontsize=10)
        if pubstyle:
            fig.text(0.02, 0.5, 'Normalized Flux', va='center', rotation='vertical',fontsize=10)
        if save2pdf==2:
            plt.savefig(current_dir+'/'+output+'.pdf')
        else:
            plt.show()
    os.system('rm -rf chunks/')
    os.chdir(current_dir)
