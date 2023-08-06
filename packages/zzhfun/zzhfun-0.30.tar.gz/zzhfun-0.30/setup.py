import setuptools
setuptools.setup(name='zzhfun',
      version='0.30',
      description='zzh model function and data function',
      url='https://github.com/FlashSnail/zzhfun',
      author='Zzh',
      author_email='zzh_0729@foxmail.com',
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 2",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      install_requires=[
        'pandas>=0.24.2',
        'numpy>=1.16.2',
        'xgboost>=0.82', # depency on scipy, however, 1.2.2 is the last version support py2
        #'keras>=2.2.4',
        'scikit-learn<=0.20.3', #0.20 is the last version support for py2
        #'file==0.2.0'
      ]      
      )
