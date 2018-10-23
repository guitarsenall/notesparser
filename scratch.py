
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

import os
directory   = os.getcwd()
extensions = ['jpg', 'bmp', 'png', 'gif']
file_names = [fn for fn in os.listdir(directory)    \
              if any(fn.endswith(ext) for ext in extensions)]
