import re
from .dataformat import DATA, HEADERKEYS,MULTILINECOMPONENTS

def read_case(filename):
    case34 = {key: [] for key in DATA.keys()}
    key = None

    with open(filename, encoding="latin-1") as f:
        for line in f:

            # Get type of data
            type_data = get_type_of_data(line)
            if type_data == "END":
                break # End of file

            if type_data == "COMMENT":
                continue # Skip comment

            if type_data == "HEADER":
                parts = get_parts(line.split("/")[0], HEADERKEYS)
                case34["HEADER"] = parts
                continue

            if type_data: # Header of block data
                key = type_data
                continue

            # Populate dict if is in data block
            if key:
                if key not in MULTILINECOMPONENTS:
                    # Get parts and pad with None missing info
                    parts = get_parts(line, DATA[key])

                    # Add to the case
                    case34[key].append(parts)

                elif key == "TRANSFORMER":
                    components = []
                    for j, sublist in enumerate(DATA[key]):
                        parts = get_parts(line, sublist)
                        components.append(parts)
                        if j < 3:
                            line = next(f)
                        elif j == 3:
                            line = next(f) if components[0]["K"] != '0' else ""
                    # Append to case
                    case34[key].append(components)
                else:
                    components = []
                    for j, sublist in enumerate(DATA[key]):
                        parts = get_parts(line, sublist)
                        components.append(parts)
                        if j < len(DATA[key]) - 1:
                            line = next(f)
                    # Append to case
                    case34[key].append(components)
    return case34

def get_type_of_data(line):
    match_end = re.search(r"^Q", line)
    if match_end:
        return "END"

    match_comment = re.search(r"^@!", line)
    if match_comment:
        return "COMMENT"
    
    match_header = re.search(f"^0([^,]*,)([^,]*,)\s*34", line)
    if match_header:
        return "HEADER"

    match_data_type = re.search(r"(?<=BEGIN\s).*(?=\sDATA)", line)
    if match_data_type:
        return match_data_type.group()

    return None

def get_parts(line, data: list):
    parts = [part.strip() for part in line.split(",")]
    parts.extend([None] * (len(data) - len(parts)))
    component = {key: part for key, part in zip(data, parts)}
    return component
