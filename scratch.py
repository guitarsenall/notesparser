
# scratch.py

# Build list of all files but .html files
import os, pprint
os.chdir(r'D:\Users\Owner\Documents\OneDrive\2018\notesparser\notesparser\sampledata')
directory   = os.getcwd()
extensions = [ 'htm', 'html' ]
image_file_names    = os.listdir(directory)
old_file_names      = image_file_names[:]
for fn in old_file_names:
    if any( fn.endswith(ext) for ext in extensions):
        image_file_names.remove(fn)
image_file_names.sort(key=os.path.getctime)
for fn in image_file_names:
    print '%s, %s' % ( fn, os.path.getctime(fn) )
#pprint.pprint( image_file_names )

## experiment with file creation date
#import os
#files   = [ 'github_repository_a.png',
#            'beginning_python_cover_a.jpg' ]
#ctimes  = []
#for file in files:
#    ctimes.append( os.path.getctime(file) )
#print 'files: ', files
#print 'ctime sorted: ', sorted(files, key=os.path.getctime)
#print 'alphabetical sorted: ', sorted(files)

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

