# conway

A demo webpage implementing Conway's game of life, based on the rust wasm
tutorial.

- The rust code in `wasm` defines a backend implementing the game
- The typescript code in `client` implements a frontend for this
- The Dockerfile uses vanilla nginx to serve out the resulting page
