import os
import json
from collections import Counter
from collections import OrderedDict

class Convertor():

    def __init__(self, doc_path):
        
        # Init Class member variablse
        self.doc_path = doc_path
        self.doc_content = None
        self.conversion_dict = {
            '!': '"',
            '"': '#',
            '#': '!',
            '$': '&',
            '%': '$',
            '&': ')',
            "'": '%',
            '(': '(',
            ')': "'"
        }
        self.character_shift = 7
        self.number_shift = 5
        self.output_string = ''
        self.top_10_words = None
        self.untranslated_letters = {}


    # Method to perform encode operation
    def encode(self):
        
        # Read the doc if doc content is None
        if not self.doc_content:
            with open(self.doc_path, 'r') as fp:
                self.doc_content = fp.read().replace('\n', ' ')
                fp.close()

        # Iterate on each character of the doc content
        for char in self.doc_content:

            # Check if the character is alphabet
            if char.isalpha():

                # Set upper and lower bounds for lower and upper case letters
                lower_start = 97
                lower_end = lower_start + 26
                upper_start = 65
                upper_end = upper_start + 26
                # Get aascii of character
                ord_char = ord(char)

                # If the character is upper
                if char.isupper():

                    # Handle overflow shifting for upper case letter
                    if ord_char + self.character_shift >= upper_end:
                        self.output_string += chr(ord_char + self.character_shift - upper_end + upper_start)
                    else:
                        self.output_string += chr(ord_char + self.character_shift)
                else:

                    # Handle overflow shifting for lower case letters
                    if ord_char + self.character_shift >= lower_end:
                        self.output_string += chr(ord_char + self.character_shift - lower_end + lower_start)
                    else:
                        self.output_string += chr(ord_char + self.character_shift)

            # If the character is numeric
            elif char.isdigit():
                self.output_string += str((int(char) + 5) % 10)

            # If the character is in our special character dict then replace it with it's value
            elif char in list(self.conversion_dict.keys()):
                self.output_string += self.conversion_dict[char]

            # Else set it in untranslated letters
            else:
                if char in list(self.untranslated_letters.keys()):
                    self.untranslated_letters[char] += 1
                else:
                    self.untranslated_letters[char] = 1
                self.output_string += char

        # Get the dir name from full path
        dir_path = os.path.dirname(self.doc_path)
        # Get filename and it's extension as list
        filenames = os.path.splitext(os.path.basename(self.doc_path))
        # Generate new output file name
        output_path = dir_path + filenames[0] + '-output' + filenames[1]

        # Write encoded output to the file
        with open(output_path, 'w') as wp:
            wp.write(self.output_string)
            wp.close()

        # Split whole text into words
        words_set = self.doc_content.split()
        counter = Counter(words_set)
        # Get top 10 words
        self.top_10_words = counter.most_common(10)

        # Sort the dictionary of untranslated words by their frequency in doc content
        sorted_dictionary = OrderedDict(sorted(self.untranslated_letters.items(), key=lambda v: v, reverse=True))
        
        # Set the json content
        sec_content = {
            'top_10_words': self.top_10_words,
            'untranslated_letters': dict(sorted_dictionary)
        }

        # Output path for output-sec file
        sec_output_path = dir_path + filenames[0] + '-output-sec' + filenames[1]

        # Write to file
        json.dump(sec_content, open(sec_output_path, 'w'))


    # Method to handle decode operation
    def decode(self):


        # Read the doc content if None
        if not self.doc_content:
            with open(self.doc_path, 'r') as fp:
                self.doc_content = fp.read().replace('\n', ' ')

        # Iterate on each character of the doc
        for char in self.doc_content:

            # Decode alphabet
            if char.isalpha():
                lower_start = 97
                lower_end = lower_start + 26
                upper_start = 65
                upper_end = upper_start + 26
                ord_char = ord(char)

                if char.isupper():
                    if ord_char - self.character_shift < upper_start:
                        self.output_string += chr(upper_end - (upper_start - (ord_char - self.character_shift)))
                    else:
                        self.output_string += chr(ord_char - self.character_shift)
                else:
                    if ord_char - self.character_shift < lower_start:
                        self.output_string += chr(lower_end - (lower_start - (ord_char - self.character_shift)))
                    else:
                        self.output_string += chr(ord_char - self.character_shift)
            
            # Decode numeric values
            elif char.isdigit():
                self.output_string += str((10 + int(char) - 5) % 10)

            # Decode special symbol values from our conversion dict
            elif char in list(self.conversion_dict.keys()):
                self.output_string += list(self.conversion_dict.keys())[list(self.conversion_dict.values()).index(char)]

            else:
                self.output_string += char

        # Preapre output file name
        dir_path = os.path.dirname(self.doc_path)
        filenames = os.path.splitext(os.path.basename(self.doc_path))
        output_path = dir_path + filenames[0] + '-output-decoded' + filenames[1]

        # Write output to the file
        with open(output_path, 'w') as wp:
            wp.write(self.output_string)
            wp.close()
