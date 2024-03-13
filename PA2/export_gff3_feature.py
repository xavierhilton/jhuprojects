#!usr/bin/python3
import re
import sys

# validargs is a list that keeps track of the required command line argument parameters
validargs = ['--source_gff', '--type', '--attribute', '--value']
# query_values is a dictionary that keeps the values that keeps the input sorted in case the input arguments aren't "in-order"
query_values = {'type': "", 'attribute': "", 'value': ""}
# path stores the path of the gff3 input file as a string
path = ""
# proceed allows for the code to process down to the search block if true
proceed = True


# finding_seq is a function I wrote to break down the gff result (gff3_line) to find the correct sequence and print it
def finding_seq(gff3_line, res_string):
    # chromosome looks for the correct chromosome number (ie chrI, chrV, etc)
    chromosome = re.match(r"^chr\w*", gff3_line).group()
    # range looks for the exact base pair coordinates that the sequence is located in
    range = re.split(r"\t", re.search("\d+\t\d+", gff3_line).group())
    # direction looks for the way to read the chromosome, whether it be forward(+) or reverse(-)
    direction = re.split(r'\t', re.search(r'\d\t.\t.\t.\t\w', gff3_line).group())[2]
    # fasta searches and grabs the chromosome sequence
    fasta = re.search(r">" + "%s" % chromosome + "([^>]*)", input_reader).group()
    # sequence breaks down the FASTA-formatted sequence, takes away the heading ">...", and converts the sequence into one string
    sequence = re.split(r"\n", fasta)
    sequence.remove(">" + chromosome)
    sequence = "".join(sequence)
    # result stores the resulting string of DNA derived from the factors grabbed above
    result = ""
    # this if case is for if the provided direction is in a forward direction
    if direction == "+":
        # the for loop cycles through the sequence, tracking the index of the char in the string and the char itself(base)
        for index, base in enumerate(sequence):
            # if the index is within the range, then it's added to the result string
            if int(range[0]) <= index <= int(range[1]):
                result += base
    # this if case is for if the direction provided is in a reverse direction
    elif direction == "-":
        # in this case, the sequence is read in reverse, so I reverse the sequence
        sequence = sequence[::-1]
        # same loop as above, as the sequence is reversed already
        for index, base in enumerate(sequence):
            if int(range[0]) <= index <= int(range[1]):
                result += base
    # this else statement is in cases where there is no forward/reverse direction indicated
    else:
        # for convenience, I assume that the output should be read in a forward direction
        print('No strand direction found. Forward sequence will be printed.')
        for index, base in enumerate(sequence):
            if int(range[0]) <= index <= int(range[1]):
                result += base
    # segments stores the broken result sequence, up to 60 bases per indexed string
    segments = []
    # increment keeps track of how far I am on the result sequence
    increment = 0
    # the for loop is similar to the other loops, except it is on the result sequence
    for number, letter in enumerate(result):
        # since the index starts at 60, I felt that it was fair to do the index(number) + 1 to make sure that I was selecting multiples of 60
        if ((number + 1) % 60 == 0 and (number + 1) / 60 > 0) or number == len(result) - 1:
            segments.append(result[increment * 60:number])
            increment += 1
    # the res_string represents the heading of the results, which I print it here
    print(res_string)
    # for the final result, I loop through the segments list and print it in order
    for segment in segments:
        print(segment)


# cmdargs is the resulting list derived from sys.argv
cmdargs = sys.argv
# since the first argument is the program name itself, I take it out since it's ultimately useless in the query
del cmdargs[0]
# this checks for if there is the correct number of remaining arguments
if len(cmdargs) != 4:
    print(
        "Invalid command line prompt - this program must have 4 arguments: the path of the gff3 file, the type of sequence and the type and value of an attribute. Please try again.")
    proceed = False
else:
    # since cmdargs is a list, I use this for loop to cycle through it
    for args in cmdargs:
        # this if statement looks for the valid argument format, which is "--something="
        if re.search(r"--.*=", args):
            # if it is, value captures the value of the argument parameter
            value = re.split(r"=", args)[1]
            # then, it looks if the argument parameter is valid as in outlined above
            if re.split(r'=', args)[0] in validargs:
                # if there is a path argument, then path is derived here
                if re.search(r"--source_gff", args):
                    path = value
                # if type is provided, then the type value in the dictionary is grabbed
                if re.search(r"--type", args):
                    query_values['type'] = value
                # if attribute is provided, then the attribute value in the dictionary is grabbed
                if re.search(r"--attribute", args):
                    query_values['attribute'] = value + "="
                # if value is provided, then the value value in the dictionary is grabbed
                if re.search(r"--value", args):
                    query_values['value'] = value
            # if the argument parameter is not seen in validargs, then this else statement is triggered
            else:
                print(
                    args + ' is an invalid argument for this program. Please use the arguments --source_gff, --type, --attribute, and --value.')
                proceed = False
        # if the formatting for the command line argument is incorrect, then this else statement is triggered
        else:
            print(
                "Invalid format used for command line arguments - only use --source_gff, --type, --attribute, and --value. Please try again.")
            proceed = False
            break

# if all information is derived, then we can move onto the search code block
if proceed:
    # result_string stores the correct values and formatting for the result header
    result_string = ""
    # query_parameters stores the formatted search statement used for the search
    query_parameters = ""
    # this if statement checks if there is a file path provided or if the file path provided points to a gff file
    if path == "" or re.search(r'\.gff$', path) == None:
        print('Source path is invalid. Please try again.')
    else:
        # input and input_reader allow me to open and read the file
        input = open(path)
        input_reader = input.read()
        # query_values is cycled through to build the query_parameters and result_string strings
        for key in query_values:
            query_parameters += ".*" + query_values.get(key)
            if result_string == "":
                result_string += ">" + query_values.get(key)
            else:
                result_string += ":" + query_values.get(key)
        # query stores the list derived from the findall command
        query = re.findall(r"%s" % query_parameters + "[\W]", input_reader)
        # this if statement is triggered if there are multiple matches for the search parameters found
        if len(query) > 1:
            print("Multiple matches have been detected. The program will print out every result.")
            # for convenience, I made sure to print out every sequence that matched the initial parameters
            for result in query:
                finding_seq(result, result_string)
        # since findall outputs a list, I grabbed the only value out of the list if the query returns exactly 1 result
        elif len(query) == 1:
            finding_seq(query[0], result_string)
        # this if statement is for if there is nothing found that matches the parameters
        elif len(query) == 0:
            print("No results were found for these argument parameters. Please try again.")
