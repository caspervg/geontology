from geontology import GeoOntology

ont = GeoOntology("tests/geo_ontology.ttl", frmt='n3')

ont.add_geo_column("work", "data", "http://linkedgeodata.org/ontology/OilPlatform", name="location", field1="lat",
                   field2="lon", type='PointFeature', desc="Oil platforms")

ont.add_info_column("work", "data", "http://linkedgeodata.org/ontology/maxspeed", name="speed", field="speed", type="integer",
                    desc="Maximum allowed speed")

serialized = ont.serialize()
assert """<http://move.ugent.be/geodata/ontology/work/data/column/location> a :DuoGeoColumn ;
    :defines <http://linkedgeodata.org/ontology/OilPlatform> ;
    :description "Oil platforms" ;
    :field "location" ;
    :field1 "lat" ;
    :field2 "lon" ;
    :type "http://move.ugent.be/geodata/ontology/PointFeature" .""" in serialized
assert """<http://move.ugent.be/geodata/ontology/work/data/column/speed> a :InfoColumn ;
    :defines <http://linkedgeodata.org/ontology/maxspeed> ;
    :description "Maximum allowed speed" ;
    :field "speed" ;
    :name "speed" ;
    :type "integer" .""" in serialized

ont.add_info_column("work1", "data1", "http://linkedgeodata.org/ontology/maxspeed", name="speed", field="speed1", type="integer",
                    desc="Maximum allowed speed 2", unit="http://purl.obolibrary.org/obo/UO_0000094")

serialized = ont.serialize()

assert """<http://move.ugent.be/geodata/ontology/work1/data1/column/speed> a :InfoColumn ;
    :defines <http://linkedgeodata.org/ontology/maxspeed> ;
    :description "Maximum allowed speed 2" ;
    :field "speed1" ;
    :name "speed" ;
    :type "integer" ;
    :unit [ a <http://purl.obolibrary.org/obo/UO_0000094> ] .""" in serialized

ont.set_fields('Accuracy', field='my_acc_field')

serialized = ont.serialize()

assert """col:Accuracy a :AccuracyColumn ;
    prop:defines <http://sensorml.com/ont/swe/property/PositionalAccuracy> ;
    prop:description "Accuracy of the measurement at this point" ;
    prop:field "my_acc_field" ;
    prop:name "accuracy" ;
    prop:type "real" .""" in serialized