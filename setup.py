from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'YouBike API for Python'
LONG_DESCRIPTION = 'YouBike API for Python'

# Setting up
setup(
        name="youbike", 
        version=VERSION,
        author="AvianJay",
        author_email="avianjayusb@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'youbike'],
        classifiers= [
        ]
)