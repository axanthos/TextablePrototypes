from setuptools import setup

setup(
    name="MyWidgets",
    version='0.0.1',
    packages=["MyOrangeWidgets"],
    entry_points={"orange.widgets": "MyWidgets = MyOrangeWidgets"},
    install_requires=[
        'Orange-Textable>=1.5.2',
    ],
    author="University of Lausanne",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2 :: only',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],    
)
