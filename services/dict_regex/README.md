# `dict_regex`

A tiny web application exposing a `/match` endpoint that takes a regex in the
`p` query parameter and looks up English words matching that regex.

For example:
```
$ curl localhost:8080/v0/match/?p=.foo.
{"matches":["afoot"]}
```

## Organization

- Python server code is in `src/server`
- Rust match engine code is in `src/engine`
    - This builds via [`maturin`](https://github.com/PyO3/maturin) into a Python
      module

## Development

Slightly irritating development flow for the rust engine:

- From root directory, activate the virtual environment with `source
  .venv/bin/activate`
- `cd` into `src/engine`
- `maturin develop`/`maturin build`
- `poetry install` as usual in the root
