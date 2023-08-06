import setuptools

setup = \
    {
        'name': "tfv",
        'version': '0.0.1',
        'description': "Post processing tools for TUFLOW FV results",
        'url': "https://gitlab.com/JonahC/tfv",

        'author':
            [
                "Toby Devlin",
                "Jonah Chorley"
            ],

        'author_email': "support@tuflow.com",

        'packages': setuptools.find_packages(),

        'classifiers':
            [
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],

        'python_requires': '>=3.6',
        'install_requires':
            [
                'numpy>=1.17.0',
                'matplotlib>=3.1.1',
                'netCDF4>=1.5.1.2',
                'PyQt5>=5.13.0',
            ]
    }

setuptools.setup(**setup)
