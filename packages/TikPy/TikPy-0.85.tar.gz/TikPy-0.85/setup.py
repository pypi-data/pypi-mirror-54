from distutils.core import setup, Extension

with open('README.txt', encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'TikPy',         # How you named your package folder (MyLib)
  packages = ['TikPy'],   # Chose the same as "name"
  version = '0.85',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description_content_type='text/markdown',

  long_description=long_description,
#   long_description="""
# # TikTok API

# TikTok has no public API. TikPy is a **light weight API**, without the requirement of any browser sessions, to collect the public data available at [www.tiktok.com](https://www.tiktok.com). Collect trending posts, video metadata, user metadata, hashtags, music, related hashtags, related music and, download videos with the API. Everything is returned in a JSON object. 

# ## Instlling
# ```python
# pip install TikPy
# ```
# ## Quick Start
# ```python
# from TikPy import TikAPI

# api = TikAPI.API()
# api.get_user_info('leenabhushan')
# ```

# ### Documentation [here](www.github.com/precog-recr/TikPy)
#   """,

# long_description_content_type='text/markdown',
   # Give a short description about your library
  author = 'Vishwesh Kumar',                   # Type in your name
  author_email = 'vishwesh18119@iiitd.ac.in',      # Type in your E-Mail
  url = 'https://github.com/precog-recr/TikPy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/precog-recr/TikPy/archive/1.0.tar.gz',    # I explain this later on
  keywords = ['TikTok', 'API'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'bs4',
          'newspaper3k'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    # 'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    # 'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)