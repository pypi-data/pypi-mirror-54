from setuptools import setup


setup(
    name='sanic-redis',
    version='0.2.0',
    description='Adds redis support to sanic .',
    long_description='sanic-redis is a sanic framework extension which adds support for the redis.',
    url='https://github.com/strahe/sanic-redis',
    author='strahe',
    author_email="www@strahe.com",
    license='MIT',
    packages=['sanic_redis'],
    install_requires=('sanic', 'aioredis'),
    zip_safe=False,
    keywords=['sanic', 'redis', 'aioredis'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ],
)
