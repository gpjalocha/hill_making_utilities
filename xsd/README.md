# XML schema definition for DSJ hills (v1.10)

This XSD file allows you to check your hill XML schema correctnes.

* XSD validator checks for duplicated tags in elements ( elements defined like `<pillar refx1="inrun" refx1="dhill" ...` will fail the validation)
* If unknown element under parent is used, XSD will fail
* If unknown attribute under element is used XSD will fail
* If type/format of the attribute is incorrect, XSD will fail(this includes checking if material and textures are avaliable)

## How to check?

This XSD is in version 1.0 since many of the IDE plugins use 1.0 version(1.1 version allows for much more complex validation conditions). You can google it or use this simple script provided:

You need library to use the script

`pip install xmlschema`

and run the following to check the schema

`python validate_xml.py <schema_path> <hill_path>`
