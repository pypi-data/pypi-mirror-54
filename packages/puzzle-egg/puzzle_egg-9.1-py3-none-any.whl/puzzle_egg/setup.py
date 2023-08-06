from setuptools import setup

setup(
    name='puzzle_egg',
    packages=['puzzle_egg'],
    description='Puzzle for something nice',
    version='9.1',
    package_data={'puzzle_egg': ['data/bomb-icon.png','data/kitties.txt','data/kitties2.txt','data/letter_1.png', 'data/letter_2.png', 'data/letter_3.png', 'data/letter_4.png','data/letter_5.png', 'data/letter_6.png', 'data/letter_7.png', 'data/letter_8.png', 'data/letter_9.png', 'data/letter_10.png']},
    url='',
    author='Alice Bom',
    author_email='alice.bom@avanade.com',
    keywords=['puzzle','main','configuration'],
    install_requires=[
    ]
)
