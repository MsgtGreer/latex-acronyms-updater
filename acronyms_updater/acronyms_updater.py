import os
import argparse
import glob
import re


def find_tex_files(dir: str):
    return glob.glob(f"{dir}/*.tex")

def find_acronyms_in_string(string: str):
    pat = re.compile(r'\\ac[sp]{0,1}\{([A-Za-z0-9]+)\}')
    acronyms = pat.findall(string)
    #return acronyms
    return list(set(acronyms))

def read_tex_file_and_get_acronyms(file):
    with open(file,"r") as f:
        text = f.read()
    return find_acronyms_in_string(text)

def read_acronyms_file_and_get_acronym_definitions(file):
    with open(file,"r") as f:
        text = f.read()
    pat = re.compile(r'\\begin\{acronym\}((?:.|\n)*?)\\end\{acronym\}')
    acronyms_definition = pat.findall(text)
    acronyms_list = get_acronyms_from_definitions(acronyms_definition[0])
    return acronyms_list

def get_acronyms_from_definitions(text):
    pat = re.compile(r'\\acro\{([A-Za-z0-9]+)\}')
    acronyms = pat.findall(text)
    return acronyms

def create_definition_prototype_from_acronym(acronym: str):
    return f"\t\\acro{{{acronym}}}[Not Defined]{{Not Defined}}\n"

def get_acronym_definition_lines(file):
    with open(file,"r") as f:
        lines = f.readlines()
    definition_lines=[line for line in lines if '\\acro' in line]
    return definition_lines

def update_acronym_definition_file(file,list_of_new_acronyms):
    definition_lines = get_acronym_definition_lines(file)
    # This is the dirty method, assuming the acronym definition file does not contain 
    for ac in list_of_new_acronyms:
        definition_lines += [create_definition_prototype_from_acronym(ac)]
    new_file_text = '\\begin{acronym}\n'
    for line in definition_lines:
        new_file_text += f'{line}'
    new_file_text += '\\end{acronym}\n'
    with open(file,"w") as f:
        f.writelines(new_file_text)
    
    



if __name__=='__main__':
    parser = argparse.ArgumentParser(
                    prog='acronyms_updater',
                    description='This little tool finds all acronyms you reference in your tex files and is capable of adding them to your acronzms environment.',
                    epilog='Programmed bz Florian Roessing')
    parser.add_argument('-d','--directory',help='Specify the directory where to look four your tex files are stored.')
    parser.add_argument('-a','--acronymsfile',help='Specify where your acronyms environment is defined.')
    parser.add_argument('-t','--test',action='store_true',help='If set, this runs the file finder, and the acronzm finder, showing files and acronzms in the terminal.')

    args = parser.parse_args()  
    
    if args.test:
        print("======= Files and their acronym references =========")
        files = find_tex_files(args.directory)
        acronym_references = []
        for file in files:
            print(file)
            acs =read_tex_file_and_get_acronyms(file)
            print(acs)
            acronym_references += acs

        print("======= Acronym Definitions =========")
        acronym_definitions = read_acronyms_file_and_get_acronym_definitions(args.acronymsfile)
        print(acronym_definitions)
        missing_acronyms = [acs for acs in acronym_references if not acs in acronym_definitions]
        print("======= Acronyms not yet defined =========")
        print(missing_acronyms)
    else:
        files = find_tex_files(args.directory)
        acronym_references = []
        for file in files:
            acs =read_tex_file_and_get_acronyms(file)
            acronym_references += acs
        acronym_definitions = read_acronyms_file_and_get_acronym_definitions(args.acronymsfile)
        missing_acronyms = [acs for acs in acronym_references if not acs in acronym_definitions]
        update_acronym_definition_file(args.acronymsfile,missing_acronyms)

        