import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from pymarc import Record, Field, Subfield, MARCReader, MARCWriter

def parse_arguments():
    parser = argparse.ArgumentParser(
            prog='Marc2MD',
            description='Decompile MARC records to Markdown',
            )
    parser.add_argument('filename')
    parser.add_argument('output')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Load the Jinja templates.
    env = Environment(
            loader = FileSystemLoader("templates"),
            autoescape=select_autoescape()
            )
    record_template = env.get_template("record.md")
    catalogue_template = env.get_template("catalogue.md")

    # Load the MARC language term dicts.
    with open('languages.json') as f:
        language_data = f.read()
    languages = json.loads(language_data)

    listing = {}

    with open(args.filename, 'rb') as fh:
        reader = MARCReader(fh)
        for record in reader:
            values = {}

            f008 = record.get('008').value()

            f245 = record.get('245')
            values['title'] = f245.format_field()

            # Try to determine the "type" of the record (book, collection, etc.)
            # This will not be shown in the record if it's an unsupported type.
            ldr_type = record.leader[6:7]
            ldr_level = record.leader[7:8]
            if ldr_type == 'p' and (ldr_level == 'c' or ldr_level == 'd'):
                values['type'] = 'Collection'
            elif ldr_type == 'a':
                if ldr_level == 'm':
                    values['type'] = 'Book'
                elif ldr_level == 's':
                    values['type'] = 'Serial'
            elif ldr_type == 'r':
                values['type'] = 'Realia'

            # Get the author.
            author = record.get_fields('100', '110', '111')
            if author:
                # Delete any links or ID numbers.
                author[0].delete_subfield('0')
                author[0].delete_subfield('1')

                values['author'] = author[0].format_field()

            # Uniform title.
            if f240 := record.get('240'):
                values['uniform_title'] = f240.format_field()

            # Process 7xx fields into contributors and analytical entries.
            values['contributors'] = []
            values['analytics'] = []
            for f7xx in record.get_fields('700', '710', '711'):
                # Delete any links or ID numbers.
                f7xx.delete_subfield('0')
                f7xx.delete_subfield('1')

                if f7xx.indicator2 == '2':
                    values['analytics'].append(f7xx.format_field())
                else:
                    values['contributors'].append(f7xx.format_field())

            # Get a list of languages, combining the 008 language with anything
            # listed in 041. Keep a separate list of original languages from 041 $h.
            values['languages'] = [languages[f008[35:38]]]
            values['original_languages'] = []
            if f041 := record.get('041'):
                for language_code in f041.get_subfields('a'):
                    if languages[language_code] not in values['languages']:
                        values['languages'].append(languages[language_code])
                for language_code in f041.get_subfields('h'):
                    values['original_languages'].append(languages[language_code])

            # Edition.
            if f250 := record.get('250'):
                values['edition'] = f250.format_field()

            # Get the publication and copyright information from the 264s.
            for f264 in record.get_fields('264'):
                if f264.indicator2 == '1':
                    values['publication'] = f264.format_field()
                elif f264.indicator2 == '4':
                    values['copyright'] = f264.get('c')
            # If there isn't a 264, try to fall back to 260.
            if 'publication' not in values:
                if f260 := record.get('260'):
                    values['publication'] = f260.format_field()

            # Physical description.
            if f300 := record.get('300'):
                values['physical_description'] = f300.format_field()

            # ISBNs.
            values['isbns'] = []
            for f020 in record.get_fields('020'):
                # Currently we're only getting valid ISBNs.
                if f020.get('a'):
                    values['isbns'].append(f020.format_field())

            # Subjects.
            values['subjects'] = []
            for subject in record.subjects:
                # Delete the vocabulary code.
                subject.delete_subfield('2')
                values['subjects'].append(subject.format_field())

            # Notes.
            for f541 in record.get_fields('541'):
                # Delete any acquisition data deemed to be private.
                if f541.indicator1 == '0':
                    record.remove_field(f541)
            # Currently notes fields are not differentiated.
            # Possible future feature to come back and separate these out,
            # e.g. summary, scope and content, etc.
            values['notes'] = [note.format_field() for note in record.notes]

            values['holdings'] = [holding.format_field() for holding in record.get_fields('852', '863')]

            # Get the control number and add the record to a master dict
            # mapping control numbers to titles.
            # This will be used for the index page.
            control = record.get('001').value()
            listing[control] = values['title']

            # Write each individual catalogue record to its own file.
            with open(args.output + '/records/' + control + '.md', 'w') as out:
                out.write(record_template.render(values))

        # Write a master index of all the catalogue entries.
        # This is not particularly browsable by humans but is intended to allow
        # search engines to crawl and index the whole catalogue.
        with open(args.output + '/catalogue.md', 'w') as out:
            out.write(catalogue_template.render(listing=listing))

