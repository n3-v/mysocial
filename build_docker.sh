#!/bin/bash
docker build --tag=social .
docker run -p 1337:1337 --rm --name=social -it social