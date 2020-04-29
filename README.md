## SER502-Spring2020-Team23
Project: Compiler and Virtual Machine for a Programming Language  

The team members are  

Divya Polineni
Prem Preeti Patnala
Rohith Varma Gaddam
Sree Pradeep kumar Relangi


The language developed is called "ACE" . The link to the youtube video is : https://www.youtube.com/watch?v=TzX2D-oW1Zw

The structure of the repository is as follows: 

data/ - consists the sample programs of ACE.

src/Compiler/ - consists of the compiler.py which we use to compile and execute programs written in ACE.

src/Runtime/ - is composed of the interpreter.py which is the main runtime environment of ACE Language.

doc/ - contains the documents.


## Installation

Requires Python 3.6 to be installed on the computer.

Requires the package PLY. Install using the following command

>> pip install ply

## Build & Run

To run the your code written in ACE,switch to the folder **src** and use the following command in a terminal or command prompt (Windows).  

The input file containing the source code written in ACE needs to be passed as an argument to the below command  

>>  python runtime/interpreter.py **input-file**

**input-file** should be placed in **data** folder

The output of the program will be displayed on the console/terminal window.  


