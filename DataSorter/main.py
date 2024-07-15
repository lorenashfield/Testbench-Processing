from collections import defaultdict

def read_lines_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Process any number of files
lines = (read_lines_from_file('uart_data1.txt')
         + read_lines_from_file('uart_data2.txt'))

# Initialize counts dictionary
counts = defaultdict(lambda: {'DE': 0, 'OK': 0, 'WD': 0})

# Process each line
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith('IN:'):
        # Parse the bit and reg, ensuring the line is complete
        parts = line.split(',')
        if len(parts) == 2:
            try:
                bit_part = parts[0].split()[2]
                reg_part = parts[1].split()[1]

                bit = int(bit_part)
                reg = int(reg_part[1:-1])

                if 0 <= bit <= 31 and (0 <= reg <= 12 or reg == 14):
                    # Form the key for the dictionary
                    key = (bit, reg)

                    # Check the next line if it exists
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line.startswith('DE:'):
                            counts[key]['DE'] += 1
                        elif next_line.startswith('OK:'):
                            counts[key]['OK'] += 1
                        elif next_line.startswith('WD:'):
                            counts[key]['WD'] += 1
            except (ValueError, IndexError) as e:
                # Skip invalid lines and print debug info
                print(f"Skipping line {i}: {line} due to error: {e}")

    # Move to the next line
    i += 1

# Print the counts for each bit/reg combination
if counts:
    sorted_keys = sorted(counts.keys(), key=lambda x: (x[1], x[0]))
    for key in sorted_keys:
        value = counts[key]
        print(f'Reg {key[1]}, Bit {key[0]}: (DE: {value["DE"]}, OK: {value["OK"]}, WD: {value["WD"]})')
else:
    print("No valid data found.")
