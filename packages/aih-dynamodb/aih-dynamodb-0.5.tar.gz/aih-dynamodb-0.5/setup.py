from setuptools import setup

setup(name='aih-dynamodb',
      version='0.5',
      description='Aih Dynamodb',
      url='https://github.com/quyencao/aih-dynamodb',
      author='aih',
      author_email='quyen.cm@example.com',
      license='MIT',
      packages=['aih_dynamodb'],
      install_requires=[
          'boto3',
          'dynamodb-json'
      ],
      zip_safe=False,
      include_package_data=True,
      python_requires='>=3.6')