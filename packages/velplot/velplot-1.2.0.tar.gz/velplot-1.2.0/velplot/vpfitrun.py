import os,numpy
from .atominfo import atom_list

def make_setup(atomdir='./atom.dat',vpsetup='./vp_setup.dat'):
    # Check if both atom.dat and vp_setup.dat are found
    assert os.path.exists(os.path.abspath(atomdir)), 'atom.dat not found at %s'%os.path.abspath(atomdir)
    assert os.path.exists(os.path.abspath(vpsetup)), 'atom.dat not found at %s'%os.path.abspath(vpsetup)
    # Set up atomic transition list
    atom = atom_list(atomdir)
    os.environ['ATOMDIR'] = os.path.abspath(atomdir)
    # Set up VPFIT settings
    os.environ['VPFSETUP'] = os.path.abspath(vpsetup)
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
    return atom,pcvals,lastchtied,daoaun

def create_chunks(fortfile,table1,header,pcvals,version,cont=False):
    '''
    Generate data chunk for each fitted region.

    Parameters
    ----------
    fortfile : str
      Path to input fort.13 or fort.26 file.
    pcvals : bool
      Flag to check if pcvals command in vp_setup.dat
    version : str
      VPFIT executable filename
    '''
    opfile = open('fitcommands','w')
    opfile.write('d\n')                 # Run display command + enter
    if pcvals:                          # If development tools called...
        opfile.write('\n')              # ...used default setup -> enter only
    opfile.write('\n')                  # Used default selfeter (logN) -> enter only
    opfile.write(fortfile+'\n')         # Insert fort file name + enter
    for line in table1:
        if cont and '.fits' in line[0]:
            opfile.write('\n')
    opfile.write('\n')                  # Plot the fitting region (default is yes) -> enter only
    if len(table1)>1:           # If more than one transitions...
        opfile.write('\n')              # ...select first transition to start with (default)
    opfile.write('as\n\n\n')
    for line in table1:
        opfile.write('\n\n\n\n')
    #if len(table1)>1:           # If more than one transitions...
    #    opfile.write('\n')              # ...select first transition to start with (default)
    opfile.write('n\n\n')
    opfile.close()
    try:
        os_cmd = version+' < fitcommands > termout'
        if os.system(os_cmd) != 0:
            raise Exception('%s does not exist'%version)
    except:
        if 'Zero wavelength range' in open('termout').read():
            print('\n\tERROR: A fitting region has no available data! Check your spectrum and/or model.\n')
        else:
            print("""\n\tThere is a problem creating the chunks. Try the following --cont argument and check that the path to data files in header is valid.\n""")
        quit()
    output = numpy.loadtxt('termout',dtype='str',delimiter='\n')
    for i in range(len(output)):
        if 'Statistics for each region :' in output[i]:
            i,k = i+2,0
            while 'Plot?' not in output[i]:
                header[k,-4] = 'n/a' if '*' in output[i].split()[2] else '%.4f'%(float(output[i].split()[2]))
                header[k,-3] = 'n/a' if '*' in output[i].split()[2] else '%.4f'%(float(output[i].split()[2])/float(output[i].split()[4]))
                header[k,-2] = output[i].split()[3]
                header[k,-1] = output[i].split()[4]
                k = k + 1
                i = i + 2
    if os.path.exists('chunks')==False:
        os.system('mkdir chunks')
        
    os.system('mv vpfit_chunk* chunks/')
    os.system('rm fitcommands termout')

    return header

def fit_fort(fortfile,fit,error,illcond,pcvals,version):
    '''
    Do Voigt fitting and update model.
    '''
    opfile = open('fitcommands','w')
    if error:
        opfile.write('e\n')             # Run fit command + enter
    else:
        opfile.write('f\n')             # Run fit command + enter
    if pcvals:                          # If development tools called...
        if illcond:
            opfile.write('il\n')
        opfile.write('\n')              # ...used default setup -> enter only
    opfile.write('\n')                  # Used default parameter (logN) -> enter only
    opfile.write(fortfile+'\n')   # Insert fort file name + enter
    opfile.write('n\n')                 # Do not plot the region + enter
    opfile.write('\n')                  # Do not fit more line and exit VPFIT -> enter only
    opfile.close()

    os.system(version+' < fitcommands')

    if fit or illcond:
    
        ''' Read fort.13 and store header and first guesses '''
    
        i,flag,header,guesses = 0,0,[],[]
        line13 = [line.replace('\n','') for line in open(fortfile,'r')]
        while i < len(line13):
            if '*' in line13[i]:
                flag = flag+1
            if '*' not in line13[i] and flag==1:
                header.append(line13[i]+'\n')
            if '*' not in line13[i] and flag==2:            
                guesses.append(line13[i]+'\n')
            i = i + 1
    
        ''' Take results from fort.18 '''
    
        i,results = 0,[]
        line18 = numpy.loadtxt('fort.18',dtype='str',delimiter='\n')
        for i in range(len(line18)-1,0,-1):
            if 'chi-squared' in line18[i]:
                a = i + 2
                break
        for i in range(a,len(line18)):
            results.append(line18[i]+'\n')
            if len(line18[i])==1:
                break
                
        ''' Update fort.13 and embed results from fort.18 '''
    
        fort = open(fortfile,'w')
        for line in ['*\n']+header+['*\n']+results+guesses:
            fort.write(line)
        fort.close()
        
