Pyphage is a Convore chatbot. It's sitting in the python group, you can go
[check it out](https://convore.com/python/introducing-the-python-chatbot-gee-i-hope-this-works/)
if you'd like.

It depends on the [requests](http://kennethreitz.com/blog/introducing-requests/) library and python 2.7 (for importlib).

The "eval" plugin depends on [pysandbox](https://github.com/haypo/pysandbox).

The python chatbot currently implements these commands:  
/doc `<something>`: return python 2.7's documentation for `<something>`  
/eval `<expression>`: use a restricted python environment to return the result of `<expression>`  
/karma: who in the python group has the most karma?  
/rtd `<module>` `<function>`: return a link to readthedocs for `<module>` and/or `<function>`  
/zen:  
/help `<something>`: get help on a command, or a list of all commands if `<something>` is omitted  
