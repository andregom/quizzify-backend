import sys, os
import wget
import tarfile
import sense2vec

url = 'https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz'
filename = wget.download(url, out = 'sense2vec_weights/')
print(filename)

# dirname = os.path.realpath('.')

# filename = 's2v_reddit_2015_md.tar.gz'

# filepath = os.path.join(dirname, filename)

# tar = tarfile.open(filename, "r:gz")
# tar.extractall()
# tar.close()
