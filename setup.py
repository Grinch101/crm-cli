from setuptools import setup


setup(
        name='cli-crm',
        version='1.0',
        py_modules=['cli'],
        install_requirs=[
                'Click',
        ],
        entry_points='''
                [console_scripts]
                cli=cli:main
        '''
)