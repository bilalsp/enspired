"""
Entry point script for `enpired-tool` command line tool.
"""
import argparse
from enspired.apartment import Apartment


def main():
    parser = argparse.ArgumentParser(description='enspired-cli-tool')
    parser.add_argument("-i", "--inputfile", required=True, 
                        help='input file path')
    parser.add_argument("-o", "--outputfile", default='./out.txt', 
                        help='input file path')
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="print output on console")
    
    args = parser.parse_args()
      
    # read input file
    with open(args.inputfile, 'r') as file:
        plan = file.read()
        plan_matrix = list(map(list, plan.split('\n')))
      
    # create apartment with empty rooms `without chairs`
    apartment = Apartment.from_plan_matrix(plan_matrix)

    # furnish appartment's rooms with chairs 
    apartment.furnish(plan_matrix)

    # in rare situation there might be duplicate rooms in apartment.
    apartment.clean()

    # sort the rooms in an apartment by `room name` 
    apartment.sort() 

    # write result to the output file
    with open(args.outputfile, 'w') as file:
        output = "total:\n"
        output += ", ".join(
            ['{}: {}'.format(k, v) for k, v in apartment.info.items()]) + '\n'
        for room in apartment:
            output += '{}: \n'.format(room.name)
            output += ", ".join(
                ['{}: {}'.format(k, v) for k, v in room.info.items()]) + '\n'
        output = output[:-1]
        file.write(output)

    # display the result on console
    if args.verbose:
        print(output)


if __name__ == '__main__':
    main()
