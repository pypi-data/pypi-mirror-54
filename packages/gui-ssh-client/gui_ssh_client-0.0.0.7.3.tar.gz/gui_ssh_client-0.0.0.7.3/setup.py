from distutils.core import setup

from setuptools import find_packages

setup(
    name='gui_ssh_client',
    packages=find_packages(),
    version='0.0.0.7.3',
    license='gpl-3.0',
    description='Simple GUI SSH client implementation with Paramiko and Tkinter',
    long_description="Simple implementation of GUI for SSH Client for educational purposes.",
    author='quantagonista',
    author_email='quantagonista@gmail.com',
    url='https://gitlab.com/quantagonista/gui_ssh_client',
    download_url='https://gitlab.com/quantagonista/gui_ssh_client/-/archive/master/gui_ssh_client-master.tar.gz',
    keywords=['ssh', 'tkinter', 'paramiko', 'ssh-client'],
    python_requires='>=3',
    install_requires=[
        'paramiko==2.6.0',
        'Pillow==6.2.0',
        'scp==0.13.2'
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
            'gui-ssh-client=gui_ssh_client.main:main',
        ],
        'gui_scripts': [
            'gui-ssh-client=gui_ssh_client.main:main',
        ]
    },
    include_package_data=True
)
