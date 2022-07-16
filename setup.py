from setuptools import setup

setup(
      name='Spring_Generator',
      version='1.0.0',
      description="Spring Boot CLI",
      long_description='generate Spring Project and code',
      author='EL BSSITA Fouad',
      author_email='Fouadelbssita@gmail.com',
      #license='MIT', # or any license you think is relevant
      packages=['script'],
      #zip_safe=False,
      install_requires=[
          'click',
          'questionary'
      ],
      entry_points="""
      [console_scripts]
      sg = script.SpringCodeGeneratore:main
      """,
)
