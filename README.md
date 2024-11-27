[![PyPI](https://img.shields.io/pypi/v/bytewax-lever.svg?style=flat-square)](https://pypi.org/project/bytewax-lever/)

# Bytewax Lever

[Lever](https://lever.co) connectors for [Bytewax](https://bytewax.io).

This connector offers 1 source:

* `LeverPostingSource` - Supplies created & updated Lever Postings

## Installation

This package is available via [PyPi](https://pypi.org/project/bytewax-lever) as
`bytewax-lever` and can be installed via your package manager of choice.

## Usage

```python
import os

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.connectors.stdio import StdOutSink

from bytewax_lever import PostingSource

LEVER_API_KEY = os.environ["LEVER_API_KEY"]

flow = Dataflow("lever_example")
flow_input = op.input("input", flow, PostingSource(api_key=LEVER_API_KEY))

op.output("output", flow_input, StdOutSink())
```

## License

Licensed under the [MIT License](./LICENSE).
