import setuptools

setuptools.setup(
        name='emx',
        version='0.0.1',
        url='https://docs.emx.com/',
        license='GNU General Public License',
        author='Pasha Petukhov',
        author_email='support@emx.com',
        description='EMX python library',
        packages=setuptools.find_packages(),
        long_description=open('README.md').read(),
        zip_safe=False,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
    )
