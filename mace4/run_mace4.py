import os
import subprocess

mace4_directory_path = os.path.dirname(os.path.realpath(__file__))
sensors_file_path = os.path.join(mace4_directory_path, 'sensors.in')
background_knowledge_file_path = os.path.join(mace4_directory_path, 'background_knowledge.in')
expression_file_path = os.path.join(mace4_directory_path, 'expression.in')
output_file_path = os.path.join(mace4_directory_path, 'result.out')

mace4_command = ['mace4', '-f', sensors_file_path, background_knowledge_file_path, expression_file_path]

mace4_process = subprocess.Popen(mace4_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

with open(output_file_path, 'w') as f:
    f.write(mace4_process.communicate()[0].decode())
