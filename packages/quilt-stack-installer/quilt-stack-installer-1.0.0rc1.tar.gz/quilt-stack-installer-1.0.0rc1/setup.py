from pathlib import Path

from setuptools import setup, find_packages

VERSION = Path(Path(__file__).parent, "quilt_stack_installer", "VERSION").read_text()

def readme():
    readme_short = """
    Command-line tool for installing Quilt as a CloudFormation stack.
    """
    return readme_short



setup(
    name="quilt-stack-installer",
    version=VERSION,
    packages=find_packages(),
    description='Quilt Data installation tool',
    long_description=readme(),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    author='quiltdata',
    author_email='contact@quiltdata.io',
    license='LICENSE',
    url='https://github.com/quiltdata/quilt',
    install_requires=[
        'appdirs>=1.4.0',
        'aws-requests-auth>=0.4.2',
        'boto3>=1.8.0',
        'requests>=2.12.4',
        'pyyaml',
        'click',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': ['quilt-stack-installer=quilt_stack_installer.cli:cli'],
    }
)
