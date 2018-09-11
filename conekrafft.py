# ConeKrafft - Cone Angle extraction
#
# Written by Nadja Krafft, idea by Christoph Stuhl (Workgroup of Prof. Reiner Anwander, University of Tuebingen)
#
# Version 1.0
#
import sys
import os

# Header
info=["ConeKrafft - Cone Angle extraction","A Krafftful tool for preparing data", "http://uni-tuebingen.de/syncat-anwander"]

print("{:*^64}".format(""))

for line in info:
    print("{}{:^62}{}".format("*", line, "*"))

print("{}{:>63}".format("*","*"))
print("{:*^64}".format(""))
print("{}".format("\nGet MATHEMATICA PACKAGE: \nhttp://www.ccqc.uga.edu/references/software.php\n"))


create_matematica = input("Do you want to create a new Mathematica File?\n(Overwrite existing file named ComplexDataBase1.txt)\n[0] No\n[1] Yes\n")

file_list = []

for xyz in os.listdir('.'):
            if xyz.endswith(".xyz") == True:
                file_list.append(xyz)
if len(file_list) == 0:
    print("No valid input files found. Program exciting")
    sys.exit(0)

if create_matematica == "1":
    output=open("ComplexDataBase1.txt","w") 
    filecount=1
    

    
    while True:
        
        num_of_files=len(file_list)
        if num_of_files == 0:
            print("All xyz files were added. Program exiting.")
            break
        
        print("Found {} xyz files:\n".format(num_of_files))
        for (number, xyz) in enumerate(file_list):
            print("{}: {}".format(number, xyz))
            
        

        filenumber_to_use=int(input("\nWhich xyz file do you want to use? Enter the number:\n "))
        if filenumber_to_use < len(file_list):
            
            filename=file_list[filenumber_to_use]
            
            print("File to open: "+filename) 

            try:
               sourceFile=open(filename)

            except FileNotFoundError:
                print("Error: File not found!")

            except IOError:
                print("Error: File not readable!")

            else:
                #list of central atoms:
                elements=["Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Al","Ga","In","Tl","Ge","Sn","Pb","As","Sb","Bi","Sc","Y","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"]
                central_atoms=[]#found central atoms in ortep file
                other_atoms =[]#all other atoms in ortep file
                
                data=sourceFile.readlines()
                sourceFile.close()
                print("Header of file:\n"+data[0]+data[1])
                del data[0:2]
                print("Header deleted")

                #copy central and other atoms to corresponding list
                for line in data:
                    match = False
                    for element in elements:
                        if element in line:
                            central_atoms.append(line)
                            match = True
                            break
                    if not match:
                        other_atoms.append(line)

                num_of_central_atoms = len(central_atoms)
                print("Found {} central atoms".format(num_of_central_atoms))

                # if more than 1 match occures, user has to choose
                # if none is found, user has to enter new filename
                if num_of_central_atoms > 1:
                    for (number, line) in enumerate(central_atoms):
                        print("{}: {}".format(number, line))

                    while True:
                        first_atom_in_list=int(input("Choose central atom from the list:\n"))
                        if first_atom_in_list < 0 or first_atom_in_list >= num_of_central_atoms:
                            print("Invalid")
                        else:
                            other_atoms.insert(0, central_atoms[first_atom_in_list])
                            del central_atoms[first_atom_in_list]
                            other_atoms.extend(central_atoms)
                            break

                elif num_of_central_atoms == 0:
                    print("Error: no central atom found!")
                    continue
                else:
                    other_atoms.insert(0, central_atoms[0])

                output=open("ComplexDataBase1.txt","a")
                filename = filename[:-4]
                output.write("(X"+str(filecount)+") "+filename+"\n")

                for (number, line) in enumerate(other_atoms, 1):
                    output.write("\n{}\t{}".format(number, line))


                output.write(str(0)+"\n\n")           
                output.close()   
                filecount=filecount+1
                
                #delete file from file_list
                del file_list[filenumber_to_use]

                print("File closed.")
                add_next = input("Do you want to convert more .xyz files?\n[0] No\n[1] Yes\n" )
                if add_next != "1":
                    break

else:
    sys.exit(0)