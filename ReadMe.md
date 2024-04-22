When I write tex, I often write up my acronyms on the go without properly adding them to my acronyms definition. This script should help me out. 

This script helps me solve the issue. 
It scrapes all tex files in a given location, extracts the referenced acronyms, compares them against the acronym definitions in a provided acronyms file and adds all definitions that are missing, with a short and longform that says undefined.

You can instal it as a local python package using pip.
Then you can run:
```
py <path_to_file>\acronyms_updater.py -h
```
for help, or
```
py <path_to_file>\acronyms_updater.py -d <path_with_tex_files_to_be_checked> -a <tex_file_with_acronym_definitions>
```
to use the tool.
!!! Warning at the moment the tool overrites your <tex_file_with_acronym_definitions>, so make sure it only contains the acronym environment.
