from rpio.transformations.transformations import swc2code_py,message2code_py
from rpio.metamodels.aadl2_IL.examples.example1 import example


#---------------example AADL model---------------------
system = example()
x=1

#---------------Run AADL 2 python code---------------------
try:
    message2code_py(system=system, path="output/generated/messages")
    swc2code_py(system=system,path="output/generated")
except:
    print("Failed to generate")