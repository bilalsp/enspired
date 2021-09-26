# Enspired GmbH Coding Task

<!-- Describe your project in brief -->
Compute chairs statistics based on floor plan of apartment.

# Table of contents
- [Description](#Description)
- [Pseudo Code](#Pseudo-Code)
- [Usage](#Usage)

## Description
Coding task description is available in [task_en.txt](task_en.txt).

## Pseudo Code
```
Step1: Read input file (e.g. 'rooms.txt') as a `plan_matrix`
Step2: Create an `Apartment` class object with empty rooms (i.e., without chairs)
    Step2.1: Find a closed boundary in `plan_matrix` 
    Step2.2: Each closed boundary in `plan_matrix` represents an apartment's room.
             So, create a `Room` class object with closed boundary.
    Step2.3: Add created room to the apartment
    Step2.4: Jump to Step2.1 until closed boundaries exist in `plan_matrix`
Step3: Furnish appartment's rooms with chairs 
    Step3.1: Traverse over each cell of `plan_matrix`.
            If chair found then add it to correct room 
            If room name found then add it to correct room
Step4: Sort the rooms in an apartment by room name.
Step5: Display the result on console and save it into ouput file.
```
Time Complexity: O(r*l) where r and l are number of rows and columns in `plan_matrix` respectively.

## Usage
Run an appropriate command inside the project folder. 

To run the program without installing `enspired-tool` cli tool.
```
python enspired/main.py -i rooms.txt --verbose
```
To install `enspired-tool` cli tool.
```
pip install --use-feature=in-tree-build . 
```
To run  `enspired-tool` cli tool
```
enspired-tool -i rooms.txt --verbose
```