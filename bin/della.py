'''

python script to deploy jobs on della-gpu


'''
import os, sys 

def sed(igal, iang): 
    '''
    '''
    script = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J sed.%i.%i" % (igal, iang),
        "#SBATCH --nodes=1", 
        "#SBATCH --time=00:59:59",
        "#SBATCH --export=ALL", 
        "#SBATCH --output=o/sed.%i.%i" % (igal, iang), 
        "#SBATCH --mail-type=all",
        "#SBATCH --mail-user=chhahn@princeton.edu",
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate gqp", 
        "",
        "python sed.py %i %i" % (igal, iang), 
        "",
        'now=$(date +"%T")', 
        'echo "end time ... $now"', 
        ""]) 

    # create the script.sh file, execute it and remove it
    f = open('script.slurm','w')
    f.write(script)
    f.close()
    os.system('sbatch script.slurm')
    os.system('rm script.slurm')
    return None


def sed_nodust(igal, iang): 
    '''
    '''
    script = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J sed.nodust.%i.%i" % (igal, iang),
        "#SBATCH --nodes=1", 
        "#SBATCH --time=00:59:59",
        "#SBATCH --export=ALL", 
        "#SBATCH --output=o/sed.nodust.%i.%i" % (igal, iang), 
        "#SBATCH --mail-type=all",
        "#SBATCH --mail-user=chhahn@princeton.edu",
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate gqp", 
        "",
        "python sed_nodust.py %i %i" % (igal, iang), 
        "",
        'now=$(date +"%T")', 
        'echo "end time ... $now"', 
        ""]) 

    # create the script.sh file, execute it and remove it
    f = open('script.slurm','w')
    f.write(script)
    f.close()
    os.system('sbatch script.slurm')
    os.system('rm script.slurm')
    return None


def sed_noz(igal, iang): 
    '''
    '''
    script = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J sed.noz.%i.%i" % (igal, iang),
        "#SBATCH --nodes=1", 
        "#SBATCH --time=00:59:59",
        "#SBATCH --export=ALL", 
        "#SBATCH --output=o/sed.noz.%i.%i" % (igal, iang), 
        "#SBATCH --mail-type=all",
        "#SBATCH --mail-user=chhahn@princeton.edu",
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate gqp", 
        "",
        "python sed_noz.py %i %i" % (igal, iang), 
        "",
        'now=$(date +"%T")', 
        'echo "end time ... $now"', 
        ""]) 

    # create the script.sh file, execute it and remove it
    f = open('script.slurm','w')
    f.write(script)
    f.close()
    os.system('sbatch script.slurm')
    os.system('rm script.slurm')
    return None


def sed_noz_nodust(igal, iang): 
    '''
    '''
    script = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J sed.noz.nodust.%i.%i" % (igal, iang),
        "#SBATCH --nodes=1", 
        "#SBATCH --time=00:59:59",
        "#SBATCH --export=ALL", 
        "#SBATCH --output=o/sed.noz.nodust.%i.%i" % (igal, iang), 
        "#SBATCH --mail-type=all",
        "#SBATCH --mail-user=chhahn@princeton.edu",
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate gqp", 
        "",
        "python sed_noz_nodust.py %i %i" % (igal, iang), 
        "",
        'now=$(date +"%T")', 
        'echo "end time ... $now"', 
        ""]) 

    # create the script.sh file, execute it and remove it
    f = open('script.slurm','w')
    f.write(script)
    f.close()
    os.system('sbatch script.slurm')
    os.system('rm script.slurm')
    return None


for igal in [60]: 
    #sed(igal, 0)
    #sed_nodust(igal, 0)
    sed_noz(igal, 0)
    sed_noz_nodust(igal 0)
