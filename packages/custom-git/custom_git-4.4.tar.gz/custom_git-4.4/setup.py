import setuptools

setuptools.setup(
     name='custom_git',  
     version='4.4',
     author="voziq",
     author_email="mgoli@voziq.com",
     description="A Docker and AWS utility package",
     url="https://github.com/voziq/custom-git",
     packages=setuptools.find_packages(),
     scripts=['jupyterlab_git/execute.sh'],
     install_requires=[
        'notebook',
        'nbdime >= 1.1.0'
    ],
     package_data={'custom_git': ['*']},
 )
