from distutils.core import setup

setup(
    name='gui-ssh-client',
    packages=['src', 'data'],
    version='0.0.0.4',
    license='gpl-3.0',
    description='Simple GUI SSH client implementation with Paramiko and Tkinter',
    long_description="Simple implementation of GUI for SSH Client for educational purposes.",
    author='quantagonista',
    author_email='quantagonista@gmail.com',
    url='https://gitlab.com/quantagonista/gui-ssh-client',
    download_url='https://gitlab.com/quantagonista/gui-ssh-client/-/archive/master/gui-ssh-client-master.tar.gz',
    keywords=['ssh', 'tkinter', 'paramiko', 'ssh-client'],
    python_requires='>=3',
    install_requires=[
        'paramiko==2.6.0',
        'Pillow==6.2.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'gui-ssh-client=main:main',
        ],
        'gui_scripts': [
            'gui-ssh-client=main:main',
        ]
    },
    data_files=[
        ('data', ['data/enve.png', 'data/pc-3.png'])
    ],
    py_modules=["main"],
)
