import pkg_resources

# List of dependencies copied from requirements.txt
dependencies = \
    [
        'matplotlib>=3.1.1',
        'netCDF4>=1.5.1.2',
        'numpy>=1.17.0',
        'PyQt5>=5.13.0',
    ]

# Throw exception if correct dependencies are not met
pkg_resources.require(dependencies)
