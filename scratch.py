
# scratch.py

# experiment with file creation date
import os
files   = [ 'github_repository_a.png',
            'beginning_python_cover_a.jpg' ]
ctimes  = []
for file in files:
    ctimes.append( os.path.getctime(file) )
print 'files: ', files
print 'sorted: ', sorted(files, key=os.path.getctime)

## try redirecting STDOUT to a file
#import sys
#sys.stdout = open('stdout.txt','wt')
#print 'print statement'
#print 'statement with trailing comma',
#print ' to see if it continues'


## better image filename processing
#import os
#directory   = os.getcwd()
#extensions = ['jpg', 'bmp', 'png', 'gif']
#image_file_names    = [ fn for fn in os.listdir(directory)    \
#                        if any(fn.endswith(ext) for ext in extensions)]
#line    = '   see github_repository_a.png'
#print any( [line.find(fn) != -1 for fn in image_file_names] )
#for fn in image_file_names:
#    if line.find(fn) != -1:
#        fnlink  = '<A TARGET="_BLANK" HREF="%s">%s</A>' % (fn, fn)
#        newline = line.replace( fn, fnlink )
#        print 'newline: ', newline

# method of obtaining list of image files
#import os
#directory   = os.getcwd()
#jpg_files   = []
#for filename in os.listdir(directory):
#    if filename.endswith(".jpg"):
#        # print(os.path.join(directory, filename))
#        jpg_files.append(filename)
#    else:
#        print 'non-jpg file: ' + filename
#nFiles  = len(jpg_files)

