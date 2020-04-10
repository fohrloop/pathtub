import setuptools
setuptools.setup(
    name='pathtub',
    version='1.0.0',
    url='https://github.com/np-8/pathtub',
    author='Niko Pasanen',
    description='Reading and editing Windows PATH.',
    author_email='niko@pasanen.me',
    license='MIT',
    packages=setuptools.find_packages(),
    keywords=['PATH', 'Windows', 'winpath', 'powershell'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Topic :: System :: Shells',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
