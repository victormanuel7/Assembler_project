import sys
import argparse

# Function to validate data to print or put in a file
def validate(data, bits=3):
    if (data in registers and bits == 3):
        return registers[data]
    elif (data in registers and bits == 8):
        data = data.split("x")[1]
        return bin(int(data, 16))[2:].zfill(bits)
    elif ("0x" in data):
        data = data.split("0x")[1]
        return bin(int(data, 16))[2:].zfill(bits)
    elif ("-" in data): # complement 2
        return bin(int(data) % (1 << bits))[2:]
    else:
        return bin(int(data, 16))[2:].zfill(bits)


# Function that will return line in which word is present (tags)
def findline(word, text, act_line):
    #print(word)
    counter = 1

    lines = text.split("\n")
    for line in lines:
        if word in line and counter != act_line:
            #print(counter)
            return counter
        counter += 1

parser = argparse.ArgumentParser(description='Process an input file to transform data into binary code.')
parser.add_argument('infile', type=argparse.FileType('r'))
args = parser.parse_args()

# dictionary of Nemonic
nemonics = {
    "add": "0000",
    "addi": "0001",
    "and": "0010",
    "andi": "0011",
    "beq": "0100",
    "bne": "0101",
    "j": "0110",
    "jal": "0111",
    "jr": "1010",
    "lb": "1011",
    "or": "1100",
    "sb": "1101",
    "sll": "1110",
    "srl": "1111",
}

registers = {
    "x0": "000",
    "x1": "001",
    "x2": "010",
    "x3": "011",
    "x4": "100",
    "x5": "101",
    "x6": "110",
    "x7": "111",
}

# Creating the output file
f = open("tmp.txt", "w")

# temp string 
temp = open(sys.argv[1], 'r')
temp_data = temp.read()
temp.close()

#print(temp_data)

counter_line = 1

# Reading the file
with open(sys.argv[1], 'r', encoding='UTF-8') as file:
    while (line := file.readline().rstrip()):
        # clean the line of tabs and empty spaces
        line = line.replace('\t', '').replace(' ', '')

        # clean the line of tags and split by ','
        if(":" in line):
            line = line.split(':')[1].split(',')
        else:
            line = line.split(',')
        
        # process each instruction if is a valid nemonic
        if(line[0] in nemonics):
            #print(nemonics[line[0]])
            #print(findline("INC", temp_data))

            if(line[0] == "add"):
                f.write(nemonics[line[0]] + validate(line[2]) + validate(line[3]) + validate(line[1], 8) + "\n")
                print(nemonics[line[0]] + validate(line[2]) + validate(line[3]) + validate(line[1], 8))
            elif(line[0] == "addi"):
                f.write(nemonics[line[0]] + validate(line[2]) + validate(line[1]) + validate(line[3], 8) + "\n")
                print(nemonics[line[0]] + validate(line[2]) + validate(line[1]) + validate(line[3], 8))
            elif(line[0] == "and"):
                f.write(nemonics[line[0]] + validate(line[2]) + validate(line[3]) + validate(line[1], 8) + "\n")
                print(nemonics[line[0]] + validate(line[2]) + validate(line[3]) + validate(line[1], 8))
            elif(line[0] == "andi"):
                f.write(nemonics[line[0]] + validate(line[2]) + validate(line[1]) + validate(line[3], 8) + "\n")
                print(nemonics[line[0]] + validate(line[2]) + validate(line[1]) + validate(line[3], 8))
            elif(line[0] == "beq"):
                #if(line[1] == line[2]):
                offset = findline(line[3], temp_data, counter_line) - counter_line
                f.write(nemonics[line[0]] + validate(line[1]) + validate(line[2]) + str(validate(str(offset), 8)) + "\n")
                print(nemonics[line[0]] + validate(line[1]) + validate(line[2]) + str(validate(str(offset), 8)))
            elif(line[0] == "bne"):
                #if(line[1] != line[2]):
                offset = findline(line[3], temp_data, counter_line) - counter_line
                f.write(nemonics[line[0]] + validate(line[1]) + validate(line[2]) + str(validate(str(offset), 8)) + "\n")
                print(nemonics[line[0]] + validate(line[1]) + validate(line[2]) + str(validate(str(offset), 8)))
            elif(line[0] == "j"):
                offset = findline(line[1], temp_data, counter_line)
                f.write(nemonics[line[0]] + str(validate(str(offset), 14)) + "\n")
                print(nemonics[line[0]] + str(validate(str(offset), 14)))
            elif(line[0] == "jal"):
                offset = findline(line[1], temp_data, counter_line)
                f.write(nemonics[line[0]] + str(validate(str(offset), 14)) + "\n")
                print(nemonics[line[0]] + str(validate(str(offset), 14)))
            elif(line[0] == "jr"):
                f.write(nemonics[line[0]] + validate(line[1]) + validate("0x0", 11) + "\n" ) 
                print(nemonics[line[0]] + validate(line[1]) + validate("0x0", 11))
            elif(line[0] == "lb"):
                f.write(nemonics[line[0]] + validate(line[3]) + validate(line[1]) + validate(line[2], 8) + "\n" ) 
                print(nemonics[line[0]] + validate(line[3]) + validate(line[1]) + validate(line[2], 8))
            elif(line[0] == "or"):
                f.write(nemonics[line[0]] + validate(line[2]) + validate(line[3]) + validate(line[1]) + validate("0x0", 5) + "\n" ) 
                print(nemonics[line[0]] + validate(line[2]) + validate(line[3]) + validate(line[1]) + validate("0x0", 5))
            elif(line[0] == "sb"):
                f.write(nemonics[line[0]] + validate(line[3]) + validate(line[1]) + validate(line[2], 8) + "\n" ) 
                print(nemonics[line[0]] + validate(line[3]) + validate(line[1]) + validate(line[2], 8))
            elif(line[0] == "sll"):
                f.write(nemonics[line[0]] + validate(line[3]) + validate(line[2]) + validate(line[1]) + validate("0x0", 5) + "\n" ) 
                print(nemonics[line[0]] + validate(line[3]) + validate(line[2]) + validate(line[1]) + validate("0x0", 5))
            elif(line[0] == "srl"):
                f.write(nemonics[line[0]] + validate(line[3]) + validate(line[2]) + validate(line[1]) + validate("0x0", 5) + "\n" ) 
                print(nemonics[line[0]] + validate(line[3]) + validate(line[2]) + validate(line[1]) + validate("0x0", 5))

        else:
            print("ERROR: The ", line[0], " is not defined.")
            break
        
        counter_line += 1

# closing the output file
f.close()
