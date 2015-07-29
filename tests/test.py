from geontology import GeoOntology

ont = GeoOntology("tests/geo_ontology.ttl", frmt='n3')

ont.add_geo_column("http://linkedgeodata.org/ontology/OilPlatform", name="OilPlatformLocation", field1="lat",
                   field2="lon", type='PointFeature', desc="Oil platforms")

ont.add_info_column("http://linkedgeodata.org/ontology/maxspeed", name="MaxSpeed", field="speed", type="integer",
                    desc="Maximum allowed speed")

serialized =  ont.serialize()
assert """col:OilPlatformLocation a :DuoGeoColumn ;
    prop:defines <http://linkedgeodata.org/ontology/OilPlatform> ;
    prop:description "Oil platforms" ;
    prop:field1 "lat" ;
    prop:field2 "lon" ;
    prop:name "oilplatformlocation" ;
    prop:type "http://move.ugent.be/geodata/ontology/PointFeature" .""" in serialized
assert """col:MaxSpeed a :InfoColumn ;
    prop:defines <http://linkedgeodata.org/ontology/maxspeed> ;
    prop:description "Maximum allowed speed" ;
    prop:field "speed" ;
    prop:name "maxspeed" ;
    prop:type "integer" .""" in serialized

ont.add_info_column("http://linkedgeodata.org/ontology/maxspeed", name="MaxSpeed2", field="speed1", type="integer",
                    desc="Maximum allowed speed 2", unit="http://purl.obolibrary.org/obo/UO_0000094")

serialized = ont.serialize()

assert """col:MaxSpeed2 a :InfoColumn ;
    prop:defines <http://linkedgeodata.org/ontology/maxspeed> ;
    prop:description "Maximum allowed speed 2" ;
    prop:field "speed1" ;
    prop:name "maxspeed2" ;
    prop:type "integer" ;
    prop:unit [ a <http://purl.obolibrary.org/obo/UO_0000094> ] .""" in serialized

ont.set_fields('Accuracy', field='my_acc_field')

serialized = ont.serialize()

assert """col:Accuracy a :AccuracyColumn ;
    prop:defines <http://sensorml.com/ont/swe/property/PositionalAccuracy> ;
    prop:description "Accuracy of the measurement at this point" ;
    prop:field "my_acc_field" ;
    prop:name "accuracy" ;
    prop:type "real" .""" in serialized