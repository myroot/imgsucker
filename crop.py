#!/usr/bin/python

import Image
import glob
import math
import os
MAXRES = 3800000


for filename in glob.glob("*.jpg") :
	print filename
	ext = filename.split('.');
	name = '.'.join(ext[:-1])
	ext = ext[-1]
	im = Image.open(filename);
	res = im.size[0] * im.size[1]
	if res > MAXRES :
		print im.size
		print 'hit'
		fragCount = math.ceil(float(res)/MAXRES)
		subHeight = int(im.size[1] / fragCount)
		for i in range(0,int(fragCount)) :
			box = (0,i*subHeight, im.size[0], i*subHeight+subHeight)
			try:
				region = im.crop(box)
				region.save('%s_%d.%s'%(name,i,ext))
			except:
				print 'error'
		os.unlink(filename)

		
		


