#!/bin/bash
for name in `find . -name "*.pyc"`; do echo $name; rm -f $name; done;
for name in `find . -name "*~"`; do echo $name; rm -f $name; done;
