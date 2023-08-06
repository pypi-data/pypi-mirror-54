#IOT:1

My custom protocol for communication between devices at home. 
It uses UPD and broadcast. 
Messages are json strings.

## Message body:

.. code-block::

    {
        "protocol": "iot:1",
        "node": "Rpi-lcd-1",
        "chip_id": "RpiB",
        "event": "lcd.content",
        "parameters: [
            "content": "-(=^.^)"
        ],
        "response": '',
        "targets": [
            "nodemcu-lcd-40x4"
        ]
    }

    
- protocol: defines name, currently iot:1
- node: friendly node name like light-room-big or screen-one-kitchen
- chip_id: a unique device id
- event: event name like light.on or display
- parameters: array of parameters. like rows to display
- response: used when responding to request, ie returning toilet state
- targets: message targets node with this names. special keyword ALL for all nodes in network

## set node name or/and chip_id

.. code-block::

    Message.chip_id = 'miau'
    Message.node_name = 'miau_too'

### Message()

Create new instance. It is automatically filled with chip_id and node_name if not set

### Message(string_message)

Creates message and fills with received data

.. code-block::

    input = """{"protocol": "iot:1", "node": "node_name", "chip_id": "aaa", "event": "channel.on", "parameters": {"channel": 0}, "response": "", "targets": ["node-north"]}"""
    msg = factory.MessageFactory.create(input)
        
## functions

### set(dictionary)

.. code-block::

    msg = message.Message()
    msg.set({
        'event': 'event.test',
        'parameters': {
            'is_x': '1'
        }
    })

Fills message with params.

### send message

.. code-block::

    s.sendto(bytes(msg), address)

### get value

.. code-block::

    msg = message.Message()
    msg.set({
        'event': 'event.test',
        'parameters': {
            'is_x': '1'
        }
    })

    print(msg['event'])


### AES encryptor


Uses AES-CBC with hmac signing.
require: pip install pycryptodome

Cryptor takes four parameters:

.. code-block::

    def __init__(self, staticiv, ivkey, datakey, passphrase):
        self.staticiv = staticiv
        self.ivkey = ivkey
        self.datakey = datakey
        self.passphrase = passphrase

Usage:

.. code-block::

    from iot_message.cryptor.aes_sha1 import Cryptor as AES

    Message.add_decoder(AES(
        'abcdef2345678901', '2345678901abcdef', '0123456789abcdef', 'mypassphrase'
    ))