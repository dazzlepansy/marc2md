# marc2md

## What is this?

marc2md is a script to convert bibliographic MARC records into Markdown files
for use in a static website. The result is a "static catalogue" that can be
used to make library holdings findable to others.

MARC is a standard data format used by professional cataloguers to represent
books, DVDs, archival collections, realia, and anything else that a library or
archive might have in its collection.

## Doesn't LibraryThing do this?

Not to my satisfaction. LibraryThing is great when it comes to books, but it's
terrible when it comes to archival collections or anything else that's not a
book because it strips out notes and subject headings from imported MARC
records. In order to allow users to maintain control over their collections,
it is important to let them describe holdings in their own terms.

## Doesn't Koha do this?

Koha, Evergreen, and any number of other online public-access catalogues
(OPACs) or integrated library systems (ILSes) are great platforms for
libraries to make their collections findable. They also manage patrons,
circulation, reporting, etc. While I use these platforms professionally, they
are overkill for my needs. I run a statically-generated website and really all
I need to make my collection accessible is a statically-generated catalogue. I
have no use for the other bells and whistles, and being able to control the
record templates lets me do what I want without a complex system getting in
the way.

## How can users search the catalogue?

marc2md outputs two things: one file for each MARC record, and one index file
that links to all the record files. If you link to your index file anywhere on
your website, search engines will crawl your whole catalogue and make the
records discoverable. Personally I use a search widget from DuckDuckGo that
lets me restrict searches to the path of the catalogue records, thus creating
a text-based search that will match anything in the catalogue. It's not as
sophisticated as a proper OPAC/ILS, but the point here is minimalism.

## How can I run this?

	python3 marc2md.py '/home/user/records.mrc' '/home/user/catalogue/'

The script will read records from the first argument and output the index file
to the output directory. The output directory is expected to have a "records"
subdirectory into which the individual records will be output.
