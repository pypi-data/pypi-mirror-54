from setuptools import setup

setup(
    name='rabbit-clients',
    version='0.9.5',
    packages=['tests', 'rabbit_clients', 'rabbit_clients.clients'],
    url='https://github.com/awburgess/rabbit-clients',
    license='MIT License',
    author='Aaron Burgess',
    author_email='geoburge@gmail.com',
    description='Provides decorators for basic RabbitMQ support with respect to publishing and consuming messages.',
    long_description='Provides decorators for basic RabbitMQ support with respect to publishing and consuming messages.',
    keywords='rabbitmq',
    install_requires=[
        'pika'
    ],
    extra_require=[
        'pytest',
        'pylint'
        'coverage',
        'pytest-cov'
    ]
)
