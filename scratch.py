
# scratch.py

# image filename processing
import os
directory   = os.getcwd()
extensions = ['jpg', 'bmp', 'png', 'gif']
image_file_names    = [ fn for fn in os.listdir(directory)    \
                        if any(fn.endswith(ext) for ext in extensions)]
line    = '   see github_repository_a.png'
print any( [line.find(fn) != -1 for fn in image_file_names] )
for fn in image_file_names:
    if line.find(fn) != -1:
        fnlink  = '<A TARGET="_BLANK" HREF="%s">%s</A>' % (fn, fn)
        newline = line.replace( fn, fnlink )
        print 'newline: ', newline


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

