from setuptools import setup

setup(
    name='daily',
    version='0.2.1',
    license='MIT',
    description='Simple CLI tool to write on the #daily slack channel and its corresponding timesheet.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Antonio Molner Domenech',
    author_email='antonio.molner@strivelabs.io',
    url='https://github.com/antoniomdk/daily-celtiberian',
    py_modules=['daily'],
    entry_points='''
        [console_scripts]
        daily=daily:cli
    ''',
    keywords=['daily', 'cli', 'timesheet'],
    data_files=[('daily', ['client_sheets.json', 'template.txt'])],
    install_requires=[
        'slackclient==2.2.1',
        'arrow==0.15.2',
        'Click==7.0',
        'halo==0.0.28',
        'gspread==3.1.0',
        'python-dateutil==2.8.0',
        'google-api-python-client==1.7.11',
        'google-auth-httplib2==0.0.3',
        'google-auth-oauthlib==0.4.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development ',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
