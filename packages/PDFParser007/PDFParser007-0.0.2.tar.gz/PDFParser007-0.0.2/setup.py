#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
   name="PDFParser007",
   version="0.0.2",
   author="Ankit Srivastava 007",
   author_email="ankits.7733@gmail.com",
   description="Get Text,heading ,Para and Sentences from pdf.",
   long_description=README,
   long_description_content_type="text/markdown",
   #url="https://github.com/pypa/sampleproject",
   packages=find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
)

install_requires = [
    'pdfminer.six',
    'nltk'
]
if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
