from setuptools import setup

setup(name='motion_control',
      version='0.1',
      description="Python library to generate Spring Project and code",
      long_description='sg to call the script',
      classifiers=[],
      keywords='python Spring',
      author='EL BSSITA Fouad',
      author_email='Fouadelbssita@gmail.com',
      #url='ANY URL YOU THINK IS RELEVANT',
      #license='MIT', # or any license you think is relevant
      packages=['script'],
      zip_safe=False,
      install_requires=[
          #'pycurl',
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      sg = script.SpringCodeGeneratore:main
      """,
)
