<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

[![Build Status](https://travis-ci.org/kountable/sanic-to-json.svg?branch=master)](https://travis-ci.org/kountable/sanic-to-json)

# sanic-to-json
Generate a Postman [JSON](http://json.org) file from a [Sanic app](https://sanic.readthedocs.io/en/latest/index.html#). The JSON file can directly uploaded into the [Postman client](https://www.getpostman.com) or through their [API](https://docs.api.getpostman.com/?version=latest#3190c896-4216-a0a3-aa38-a041d0c2eb72).  

Using the postman [schema](https://schema.getpostman.com/json/collection/v2.1.0/collection.json) we can build Postman Collections using python endpoints from Sanic (Flask apps need testing). The script parses the Sanic app. It searches for blueprints. The blueprints, through routes, provide docs strings data. The doc string data is used to populate a Postman formatted JSON file. The JSON file can then be uploaded to Postman as a collection. 

Once we have Postman formatted JSON we can create API documentation through the Postman [API](https://docs.api.getpostman.com/?version=latest#3190c896-4216-a0a3-aa38-a041d0c2eb72)

## How to use

- to execute an example run `python -m examples.example_script`
which executes
```python
from sanic_to_json import generate_sanic_json
from examples.app import app

generate_sanic_json("Test API", app, filename="postman_collection.json")
```
The above code formats the Postman collection with 'Test API' and doc strings from Sanic app, `app`, and yields [postman_collection.json](https://github.com/kountable/sanic-to-json/blob/master/postman_collection.json)

### To add `body` and `header` elements to Postman JSON 
Placing `INI` in doc string will cause the text below to be loaded into a python config object, which then get converted to the appropiate headers and JSON body in Posttman. 

For example, as found in [endpoint-three](https://github.com/kountable/sanic-to-json/blob/master/examples/blueprint_1.py)
```
    INI
    [request]
    headers = {"Content-Type": "application/json"}
    body = {"username": "{{username}}", "password": "{{password}}"}
```

### To add query parameters
Similar to above placing sections under INI that are prefixed will start a example request. 
For example, as found in [endpoint-one](https://github.com/kountable/sanic-to-json/blob/master/examples/blueprint_1.py)
```
    """Return text from request.
       
    INI
    [request]
    headers = {"Content-Type": "application/json","x-amz-sns-message-type": "Notification"}
    query = ?day=1&temp=F
    """
```

## How to document Sanic app and Blueprints
- As the example shows, the Sanic app should have a `.doc` attribute. This doc string will serve as the introduction to the API in Postman docs, e.g., `app.__doc__ = "This API does stuff."`

- Blueprints should also include a doc string, this will serve as the description to each collection folder in Postman. Again see `examples` folder
`bp1.__doc__ = "This is the doc string for blueprint1."`

- Note: You can't send a JSON body with GET method. 

## How to install 
`pip install sanic-to-json`


## Contributors
See the [GitHub contributor page](https://github.com/kountable/sanic-to-json/graphs/contributors)


## License
sanic-to-json is open source software [licensed as MIT](https://github.com/kountable/sanic-to-json/blob/master/LICENSE).



