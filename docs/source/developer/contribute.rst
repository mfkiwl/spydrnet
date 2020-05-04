.. include:: ../../../CONTRIBUTING.rst

Update History
Version 1.4 Dallin Skouson

contributing
============

We want to thank you for your interest in contributing to SpyDrNet, and we wish you a rewarding experience as you contribute to this open source project. 

This document outlines some of the helpful tips I have come up with as I have worked on developing SpyDrNet.

Get your environment setup
--------------------------

*Operating system*

SpyDrNet is written in pure python 3 and we welcome contributers using any operating system as a development platform. As of the release of version 1.4 all of the contributors have used Windows (10) or Linux (Ubuntu) for their contributions. However we have no reason to believe any other opterating system that supports python 3.5 and greater would present a problem. If it does maybe you could help us solve it!

*The Python Interpreter*

SpyDrNet is tested on Python 3.5 and up. We suggest that one of the tested version of Python 3 be used to develop with SpyDrNet, perferably the latest stable release. These are the supported platforms for release and it makes the most sense for the developers to run the release platforms.

Pip is a useful tool for installing python packages. It is useful to help install needed packages for the tests and building the documentation. Not all developers have experience with python. Useful information about installing and using pyhton as well as language documentation can be found at https://docs.python.org/3/ . This, is a great reference for getting aquainted with pyhton.

*Code Editing*

There are some great code editors. Do a google search, find one you like and use it. It doesn't much matter what you use as long as it gets the job done.


Writing Code
------------

We try to write good working code. going back through complex code segments and thinking about other ways of acomplishing the same task has been very useful. Sometimes two pairs of eyes on a segement of code can help see a way to simplify it as well.

When commiting the code the the git repository using a new branch with a related name is useful. In general we have merged all our task branches into a release branch before merging with master. Merges with master need a review which is useful to help see if there are any issues.

Additionally when making a pull request the branch will be run against the tests on several build systems this gives an additional sanity check when building. Sometimes a strange error on one test environment can reveal a deeper issue that just happened to pass on the other tests.

Tests should be written with the code.

Writing Tests
-------------

When writing tests there are a few things that are useful to lookout for.

make sure the code works the way it was expected to work. For example the flattening test makes sure the design is actually flat when done.

Take a look at how to break the test. for example make sure assertions are thrown if the expected entry criteria doesn't hold up. If there is a way to make sure the error message makes some sense that could be really helpful down the line too.

Find other strange but good use cases, and potential abuses and find a way to set up those circumstances to see if the code still holds up.

Try to write code that ensures as many possible good results as possible. For example the tests on cloneing should ideally ensure that all connected components are still connected when the clone comes out.

Creating Documentation 
----------------------