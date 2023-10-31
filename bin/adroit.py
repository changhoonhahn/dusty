'''

python script to deploy jobs on della-gpu


'''
import os, sys 

def sed(igal, iang, nmcmc=1000, keep=False, dust=True, z=True): 
    '''
    '''
    script = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J sed%s%s.%i.%i" % (['.noz', ''][z], ['.nodust', ''][dust], igal, iang),
        "#SBATCH --nodes=1", 
        "#SBATCH --time=00:59:59",
        "#SBATCH --export=ALL", 
        "#SBATCH --output=o/sed%s%s.%i.%i" % (['.noz', ''][z], ['.nodust', ''][dust], igal, iang), 
        "#SBATCH --mail-type=all",
        "#SBATCH --mail-user=chhahn@princeton.edu",
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate torch-env", 
        "",
        "python sed%s%s.py %i %i %i %s" % (['_noz', ''][z], ['_nodust', ''][dust], igal, iang, nmcmc, str(keep)), 
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



for igal in [64]: #range(55, 60): 
    sed(igal, 0, nmcmc=2000, keep=True, dust=True, z=True)
    sed(igal, 0, nmcmc=2000, keep=True, dust=False, z=True)
    sed(igal, 0, nmcmc=2000, keep=True, dust=True, z=False)
    sed(igal, 0, nmcmc=2000, keep=True, dust=False, z=False)
