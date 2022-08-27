# TODO

The macro system is not efficient. The macro class should search for the syntax of every macro and only call it when it's used.
For now the macro runs before every file, even when the macro is not used in the file

- [ ] Cache html version until changes in md file  
- [x] Optional auth to protect files against changes by unauthorized users
- [ ] Drawio integration
- [ ] use better search mechanism, using [whoosh](https://whoosh.readthedocs.io/en/latest/intro.html)
