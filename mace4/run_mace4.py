import os
import subprocess

mace4_directory_path = os.path.dirname(os.path.realpath(__file__))
sensors_file_path = os.path.join(mace4_directory_path, 'sensors.in')
background_knowledge_file_path = os.path.join(mace4_directory_path, 'background_knowledge.in')
expression_file_path = os.path.join(mace4_directory_path, 'expression.in')
output_file_path = os.path.join(mace4_directory_path, 'result.out')

mace4_command = ['mace4', '-f', sensors_file_path, background_knowledge_file_path, expression_file_path]
interpformat_command = ['interpformat', 'standard']
isofilter_command = ['isofilter']
interpformat_portable_command = ['interpformat', 'portable']

# run the shell commands and pipe the output
mace4_process = subprocess.Popen(mace4_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
interpformat_process = subprocess.Popen(interpformat_command, stdin=mace4_process.stdout, stdout=subprocess.PIPE)
isofilter_process = subprocess.Popen(isofilter_command, stdin=interpformat_process.stdout, stdout=subprocess.PIPE)
interpformat_portable_process = subprocess.Popen(interpformat_portable_command, stdin=isofilter_process.stdout,
                                                 stdout=subprocess.PIPE)

# capture the output and write it to the output file
with open(output_file_path, 'w') as f:
    f.write(interpformat_portable_process.communicate()[0].decode())
