'''

python script to deploy jobs on della-gpu


'''
import os, sys 

def sed_noz_pocomc(igal,  dust=True): 
    script = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J sed_noz.lsst%s.poco.%i" % (['.nodust', ''][dust], igal),
        "#SBATCH --nodes=1", 
        "#SBATCH --time=05:59:59",
        "#SBATCH --export=ALL", 
        "#SBATCH --output=o/sed_noz.lsst%s.poco.%i" % (['.nodust', ''][dust], igal), 
        "#SBATCH --mail-type=all",
        "#SBATCH --mail-user=chhahn@princeton.edu",
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate gqp", 
        "",
        "python sed_noz%s.py %i" % (['_nodust', ''][dust], igal), 
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

sed_noz_pocomc(0,  dust=True)
sed_noz_pocomc(0,  dust=False)
