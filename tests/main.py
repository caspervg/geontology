from rdflib import URIRef
from rdflib.namespace import DC, RDF, OWL, RDFS

from geontology import GeoOntology


ont = GeoOntology("geo_ontology.ttl", frmt='n3')
# print ont.serialize()

graph = ont.graph

print "InfoColumns"
for s, p, o in graph.triples(
        (None, RDFS.subClassOf, URIRef('http://move.ugent.be/geodata/ontology/InfoColumn'))):
    print "[%s, %s, %s]" % (s, p, o)

    for _s, _p, _o in graph.triples(
            (None, RDF.type, s)):
        print "   [%s, %s, %s]" % (_s, _p, _o)

        for __s, __p, __o in graph.triples(
                (_s, None, None)):
            print "      [%s, %s, %s]" % (__s, __p, __o)


print "\n\nGeoColumns"
for s, p, o in graph.triples(
        (None, RDFS.subClassOf, URIRef('http://move.ugent.be/geodata/ontology/GeoColumn'))):
    print "[%s, %s, %s]" % (s, p, o)

    for _s, _p, _o in graph.triples(
            (None, RDF.type, s)):
        print "   [%s, %s, %s]" % (_s, _p, _o)

        for __s, __p, __o in graph.triples(
                (_s, None, None)):
            print "      [%s, %s, %s]" % (__s, __p, __o)


if (None, URIRef('http://move.ugent.be/geodata/ontology/defines'), DC.date) in graph:
    print "some defines"