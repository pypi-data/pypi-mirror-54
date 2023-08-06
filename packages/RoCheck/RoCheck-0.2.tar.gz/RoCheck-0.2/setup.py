from setuptools import setup

setup(
    name='RoCheck',
    version='0.2',
    packages=['RoCheck'],
    install_requires=[    # 依赖列表
        'requests'
    ],
    author_email = 'kwok6140@outlook.com',
    author = "Kwok6140",
    license='MIT',
    long_description='''
# RoCheck
[Link to our github](https://github.com/Kwok6140)
This is a modules ported from grilme99's RoCheck which is written in node.js

[Link to his github](https://github.com/grilme99/RoCheck)

# How to install

pip install RoCheck

# Get started

import RoCheck as Roblox

Checks = Roblox.RoCheck("ur cookie")

print(Checks.check('place_id', 'job_id'))

> Output: 128.116.6.27 (Different depend on the server the game is running on)

# Support

> If you would like support with this module then message me on Discord (Kwok6140#2416)

> -Kwok6140



(check grilme99 or jacob out he's cool
''',
    long_description_content_type='text/markdown'
)
