import xmlschema
import sys

schema=sys.argv[1]
hill_xml=sys.argv[2]

print(schema)
print(hill_xml)

my_schema = xmlschema.XMLSchema(schema)
my_schema.validate(hill_xml)
