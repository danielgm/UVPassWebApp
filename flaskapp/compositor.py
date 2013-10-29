#!/usr/bin/python

import itertools
from math import floor
import numpy
import os
from PIL import Image, ImageChops
import png
import sys
import time



def compositeMoonMeme(backgroundFilename, distortedFilename, diffuseFilename, outputFilename):
	distorted = Image.open(distortedFilename)
	diffuse = Image.open(diffuseFilename)
	background = Image.open(backgroundFilename)

	box = (650, 605, 650 + distorted.size[0], 605 + distorted.size[1])
	diffused = ImageChops.multiply(distorted, diffuse)
	background.paste(diffused, box, diffused)
	background.save(outputFilename)


def uvpass(textureFilename, uvpassFilename, outputFilename):
	r = png.Reader(open(textureFilename, 'rb'))
	texcols, texrows, texdata, texmeta = r.read()
	assert texmeta['planes'] == 4

	# This is faster with uint16 than with uint8
	tex2d = numpy.vstack(itertools.imap(numpy.uint16, texdata))
	tex3d = numpy.reshape(tex2d, (texrows, texcols, texmeta['planes']))

	r = png.Reader(open(uvpassFilename, 'rb'))
	cols, rows, uvdata, uvmeta = r.read()
	assert uvmeta['planes'] == 4

	outdata = []
	row = 0
	for uvrowdata in uvdata:
		outrowdata = []
		for col in range(cols):
			if uvrowdata[col * 4 + 3] == 0:
				outrowdata.extend([0, 0, 0, 0])
			else:
				texrow = int(texrows - uvrowdata[col * 4 + 1] / 65536.0 * texrows - 1)
				texcol = int(uvrowdata[col * 4] / 65536.0 * texcols)
				outrowdata.extend(tex3d[texrow][texcol])
		outdata.append(outrowdata)
		row += 1

	f = open(outputFilename, 'wb')
	w = png.Writer(cols, rows, bitdepth=8, alpha=True)
	w.write(f, outdata)
	f.close()


if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Usage:\n\tpython " + sys.argv[0] + " texture.png uvpass.png output.png"
		exit()

	uvpass(sys.argv[1], sys.argv[2], sys.argv[3])

