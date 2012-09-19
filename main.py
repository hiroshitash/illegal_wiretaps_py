# Main for Illegal Wiretaps

import sys
import getopt
from wiretaps import Wiretaps

__all__ = []

def get_names_from_file(file_name):
    list_victim_names = []
    infile = file(file_name, "r")

    for line in infile.readlines():
        line = line.lower()
        new_line = ""
        for letter in line:
            if letter.isalpha():
                new_line += letter

        if len(new_line) > 0: 
            list_victim_names.append(new_line)
    return list_victim_names

    
if __name__ == '__main__':
    cmdline_params = sys.argv[1:]
    opts, args = getopt.gnu_getopt(cmdline_params, '', [])

    if len(args) != 1:
        print("The following command not supported: \n\t%s" % sys.argv)
        print("The name of input file unknown.")

    input_file_name = args[0]
    list_vname = get_names_from_file(input_file_name)
    #print(list_vname)
    
    wire_prob = Wiretaps()
    wire_prob.solve_problem(list_vname)
    #wire_prob.print_cost_table()
    wire_prob.print_solution()

    

                                   
