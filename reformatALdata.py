

def reformat(raw_filename, output_filename):

    with open(raw_filename, 'r') as f:

        with open(output_filename, 'w') as f_out:

            for line in f:
                columns  = line.split(' ', 1)

                modified_line = columns[0] + ' ' + columns[1].replace(' ', '\t')
                f_out.write(modified_line)

    print("Done!")
            
reformat('./data003.al', './tm003_AL_reformatted.txt')