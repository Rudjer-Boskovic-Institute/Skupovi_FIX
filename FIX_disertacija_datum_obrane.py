import re
import csv

# List of patterns to match against
patterns = [
    r'(\d{1,2})\.(\d{1,2})\.',  # e.g. 30.6.
    r'(\d{1,2})\. (\d{1,2})\.',  # e.g. 30. 06.
    r'(\d{1,2})\. (\d{1,2})',  # e.g. 30. 6
    r'(\d{1,2})\.(\d{1,2})',  # e.g. 30.6
    r'(\d{1,2}) ([a-zA-Z]+)',  # e.g. 30 lipnja or 30. lipanj
    r'(\d{1,2})\. ([a-zA-Z]+)',  # e.g. 30 lipnja or 30. lipanj
    r'(\d{1,2})\.([a-zA-Z]+)',  # e.g. 30 lipnja or 30. lipanj
    r'(\d{1,2})\.(\d{1,2})\.\d{4}\.',  # e.g. 30.6.1977.
    r'(\d{1,2})\.(\d{1,2})\.\d{4}',  # e.g. 30.6.1977
    r'(\d{1,2})\.(\d{2})\.\d{4}',  # e.g. 30.06.1977
    r'(\d{1,2})\.(\d{1,2})\s\d{4}',  # e.g. 30.6 1977
]

pattern_ok = [
    r'(\d{1,2})\.(\d{1,2})\.'
]

# Dictionary of month name translations
month_translations = {
    'sijecnja': '01',
    'veljace': '02',
    'ozujka': '03',
    'travnja': '04',
    'svibnja': '05',
    'lipnja': '06',
    'srpnja': '07',
    'kolovoza': '08',
    'rujna': '09',
    'listopada': '10',
    'studenog': '11',
    'studenoga': '11',
    'prosinca': '12',
}

# Define a dictionary to map characters to their replacements
replacements = {
        'siječanj': '01.',
        'veljača': '02.',
        'ožujak': '03.',
        'travanj': '04.',
        'svibanj': '05.',
        'lipanj': '06.',
        'srpanj': '07.',
        'kolovoz': '08.',
        'rujan': '09.',
        'listopad': '10.',
        'studeni': '11.',
        'prosinac': '12.',
        'siječnja': '01.',
        'veljače': '02.',
        'ožujka': '03.',
        'travnja': '04.',
        'svibnja': '05.',
        'lipnja': '06.',
        'srpnja': '07.',
        'kolovoza': '08.',
        'rujana': '09.',
        'listopada': '10.',
        'studenog': '11.',
        'prosinca': '12.',
        ',': '.',
        '..': '.',
}


# Function to convert month name to month number
def translate_month_name(month_name, stri):
    for key, value in month_translations.items():
        if key.lower() in month_name.lower():
            return value
    return ''



# Function to normalize date format
def normalize_date(date_str):
    for pattern in patterns:
        match = re.match(pattern, date_str)

        #print (date_str)
        if match:
            day, month = match.groups()[:2]
            if month.isalpha():
                month = translate_month_name(month, date_str)
            if not month:
                month = day
                day = '01.'

            return f'{day.zfill(2)}.{month.zfill(2)}.'
    return date_str

# Input and output file paths
input_file = 'obrana.tsv'
output_file = 'output.tsv'

# Open input and output files
with open(input_file, 'r', newline='') as input_fp, \
        open(output_file, 'w', newline='') as output_fp:

    # Create CSV reader and writer objects
    reader = csv.reader(input_fp, delimiter='\t')
    writer = csv.writer(output_fp, delimiter='\t')

    # Write header row to output file
    header_row = next(reader)
    writer.writerow(header_row)

    # Iterate over rows in input file
    for row in reader:

        # Extract ID and DATE columns
        id_, date_str, year_str = row

        output_string = date_str
        for old, new in replacements.items():
            output_string = output_string.replace(old, new)

        output_string = date_str
        for old, new in replacements.items():
            output_string = output_string.replace(old, new)

        output_string = date_str
        for old, new in replacements.items():
            output_string = output_string.replace(old, new)

        #date_str = date_str.translate(str.maketrans(char_mapping)) 
        # Normalize date
        normalized_date = normalize_date(output_string)

        
        match_md = re.match(r'(^\d{1,2})\.$', normalized_date)
        if match_md:
            normalized_date = '01.' + normalized_date


        nd = normalized_date
        match_norm = re.match(r'(\d{1,2})\.(\d{1,2})\.', normalized_date)
        if not match_norm:
            normalized_date = 'nepoznato'
        elif not int(match_norm[1]) and not int(match_norm[2]):
            normalized_date = 'nepoznato'
        else:
            #print(match_norm[1] + ' -- ' + match_norm[2])
            if int(match_norm[1]) < 1 or int(match_norm[1]) > 31:
                normalized_date = 'nepoznato'
                print (nd + ' -- ' + 'NOT OK dd')
            if int(match_norm[2]) < 1 or int(match_norm[2]) > 12:
                normalized_date = 'nepoznato'
                print (nd + ' -- ' + 'NOT OK mm')

        # Write normalized row to output file
        writer.writerow([id_, date_str, normalized_date])
