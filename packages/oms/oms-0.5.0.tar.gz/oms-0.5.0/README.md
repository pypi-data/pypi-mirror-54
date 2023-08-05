# oms.py

A micro-framework for the excellent **[Open Microservices Specification](https://microservices.guide/)**, for suppportive code written in Python 3.6+.

**Note**: this is pre-release software, and is subject to improvement. Contributions are welcome! This framework is being developed for [other languages](https://github.com/microservices?utf8=%E2%9C%93&q=oms.*&type=&language=), as well. If you'd like to help, [let us know](support@storyscript.io)!

# Intended / Example Usage

```shell
$ cat service.py
```
```python
import oms
from uuid import uuid4

service = oms.Microservice(name='uuid')

@service.register()
def new(prefix: str) -> str:
    """Generates a UUID, with a given prefix."""
    return f'{prefix}{uuid4().hex}'

if __name__ == '__main__':
    service.serve()
```

`register` takes some optional arguments: `name` and `path`. You can also call `service.add(f=new)`, instead.

Next, run the command `$ oms-generate` `oms.yml` files will automatically be generated, for your application:

```shell
$ oms-generate service:service
…
'oms.yml' written to disk!
```

```yaml
$ cat oms.yml
actions:
  new:
    help: Generates a UUID, with a given prefix.
    arguments:
      prefix:
        in: query
        required: true
        type: string
    http:
      method: get
      path: /new
      port: 8080
    output:
      type: string
lifecycle:
  startup:
    command:
    - python3
    - /app/service.py
oms: 1

```

```shell
$ cat Dockerfile
FROM kennethreitz/pipenv
COPY . /app
CMD ["python3", "service.py"]
```

Now, run your microservice!

```shell
$ python service.py
2019-05-09 14:45:39,342 - micro - DEBUG - Initiating 'uuid' service.
2019-05-09 14:45:39,344 - micro - DEBUG - Registering Flask endpoint: '/new'
2019-05-09 14:45:39,344 - micro - DEBUG - Dockerfile './Dockerfile' already exists!
2019-05-09 14:45:39,345 - micro - DEBUG - Microservice Manifest './oms.yml' already exists!
2019-05-09 14:45:39,346 - micro - INFO - Serving on: '*:8080'
```

This will spawn a Flask application (using the production-ready [waitress web server](https://docs.pylonsproject.org/projects/waitress/en/stable/)), preconfigured to serve the masses!

Or, use the [oms](https://github.com/microservices/oms) CLI:

```shell
$ oms run new -a prefix='user-'
…
```

## Installation

```shell
$ pip install
```

**P.S.** Do provide feedback, if you desire! :)

✨ 🍰 ✨
