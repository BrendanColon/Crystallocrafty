import math

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

###input pdb file name
pdb_code = "1LYS" ### edit this in quotes for the name of your .pdb file!
pdb_filename = pdb_code + '.pdb'

with open('secondary_structures.tmp2') as fp:
    for name, seq in read_fasta(fp):
        if pdb_code in name[1:5]:
            if 'sequence' in name:
                sequence = seq
            elif 'secstr' in name:
                secstr = seq

lengths_of_structures = []
structures_to_crochet = []
length = 0

#########################################
#generating instructions
for r in range(len(secstr)):
    res = secstr[r]
    ### recording length, will have to anticipate the length of the structure
    if res =='H' or res =='G' or res =='I':
        length = length + 1
        structures_to_crochet.append( 'Helix' )
    elif res =='E':
        length = length + 2.5
        structures_to_crochet.append( 'Beta-Sheet' )
    elif res =='S' or res =='T' or res =='X' or res =='B':
        length = length + 2.5
        structures_to_crochet.append( 'Unordered' )
    lengths_of_structures.append( length )
    length = 0

structures_flattened = []
stitch_multiplier = []
flattened_length = []

count = 1 # these steps compress the instructions as to not have repeats
for i in range(len(structures_to_crochet)-1):
    if structures_to_crochet[i] == structures_to_crochet[i+1]:
        count = count + 1
    else:
        structures_flattened.append(structures_to_crochet[i])
        stitch_multiplier.append(count)
        flattened_length.append(lengths_of_structures[i])
        count = 1

reverse_structures_to_crochet = structures_to_crochet.reverse()
reverse_lengths_of_structures = lengths_of_structures[::-1]
reverse_structures_flattened = []
reverse_stitch_multiplier = []
reverse_flattened_length = []

count = 1
for i in range(len(structures_to_crochet)-1):
    if structures_to_crochet[i] == structures_to_crochet[i+1]:
        count = count + 1
    else:
        reverse_structures_flattened.append(structures_to_crochet[i])
        reverse_stitch_multiplier.append(count)
        reverse_flattened_length.append(reverse_lengths_of_structures[i])
        count = 1

structures_flattened.append(reverse_structures_flattened[0])
stitch_multiplier.append(reverse_stitch_multiplier[0])
flattened_length.append(reverse_flattened_length[0])

flattened_stitch_count = []

for i in range(len(structures_flattened)):
    if structures_flattened[i] == 'Unordered':
        flattened_stitch_count.append( int(math.ceil(2.5*stitch_multiplier[i])) )
    elif structures_flattened[i] == 'Beta-Sheet':
        flattened_stitch_count.append( int(math.ceil(2.5*stitch_multiplier[i])) )
    elif structures_flattened[i] == 'Helix':
        flattened_stitch_count.append( int(math.ceil(1*stitch_multiplier[i])) )
#########################################

output_filename = pdb_code + '_crochet_output.txt'
output = open(output_filename, 'w')

output.write('This project will require ' + str(sum(flattened_stitch_count)) + ' stitches.\n')

for instruction in range(len(structures_flattened)):
    output.write('Step %s: %s for %s stitches. \n' % ((instruction+1), structures_flattened[instruction],
                                                      flattened_stitch_count[instruction]))
output.close()