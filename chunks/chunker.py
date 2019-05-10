#!/usr/bin/env python3
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#

from zipfile import ZipFile
import os

from bs4 import BeautifulSoup as bs
import lxml

CHUNK = 200
FILE = '../at_centerline.kmz'

assert FILE.endswith('.kmz'), "KMZ file required"
name = os.path.splitext(os.path.basename(FILE))[0]
print("decompressing file ...")
with ZipFile(FILE) as myzip:
    with myzip.open('doc.kml') as myfile:
        data = myfile.read()
print("loading file ...")
soup = bs(data, 'xml')
places = soup.find_all('Placemark')
print(len(places), "Placemarks found")
chunks = len(places) // CHUNK
chunks += bool(len(places) % CHUNK)
print(f"I will create {chunks} files from it, each with {CHUNK} Placemarks or less")
print()

for i in range(chunks):
    print("working on chunk ...", i+1)
    soup = bs(data, 'xml')
    places = soup.find_all('Placemark')

    for place in places[:i*CHUNK]:
        place.extract()
    for place in places[i*CHUNK+CHUNK:]:
        place.extract()
    with ZipFile(f"Chunk_{i+1}_{name}.kmz", "w") as f:
        f.writestr('doc.kml', soup.prettify())

print("done")
