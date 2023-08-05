# Rabbit MQ Clients

A set of client of objects to use in any service that needs to send or receive RabbitMQ messages.

### Installation

From pip

```bash
$ pip install rabbit-clients
```

From source

```python
python setup.py install
```

### Features

```Rabbit-Clients``` is an opinionated set of decorators for services or solutions
that need to exist as part of a queue oriented ecosystem.  They are opinionated in
that you can only ever have one consumer per service.  This ties services
to queues intentionally as to ensure the services purpose remains
narrow and focused.  Services can publish as much as desired.  See the
examples below for usage.

*NOTE:* ```Rabbit-Clients``` looks for an environment variable called ```RABBIT_URL```.
If this is not found then ```localhost``` will be used.

### Usage Example

You may only have one consumer per module/service.  A user can publish as much as desired.

```python
from typing import TypeVar
from rabbit_clients import consume_message, publish_message

RabbitMQMessage = TypeVar('RabbitMQMessage')


@publish_message(queue='younguns')
def publish_to_younguns(message):
    return message


@publish_message(queue='aaron_detect')
def check_for_aaron(consumed_message):
    return_message = {'name': consumed_message['name'], 'isAaron': False}
    if return_message['name']  == 'Aaron':
        return_message['isAaron'] = True
    return return_message


@consume_message(consume_queue='oldfolks')
def remove_forty_and_up(message_dict):
    people = message_dict['people']
    not_protected_class = [younger for younger in people if younger['age'] < 40]
    message_dict['people'] = not_protected_class
    
    check_for_aaron(message_dict)
    publish_to_younguns(message_dict)


if __name__ == '__main__':
    remove_forty_and_up()  # Listening for messages

```

### Documentation

README.md

### How to run unit tests

Unit testing is done with ```pytest``` and is
orchestrated by a single shell script that runs a 
RabbitMQ instance in Docker

```bash
./test.sh
```

### Contributing

```Rabbit-Clients``` will follow a GitFlow guideline.  Users wishing to contribute
should fork the repo to your account.  Feature branches should be created
from the current development branch and open pull requests against the original repo.