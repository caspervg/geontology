import json
from rdflib import Graph, Namespace, URIRef, RDF, Literal, RDFS, BNode
from collections import defaultdict

_GEO_NAMESPACE = 'http://move.ugent.be/geodata/ontology/'


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


def setpath(d, p, k):
    if len(p) == 1:
        d[p[0]] = k
    else:
        setpath(d[p[0]], p[1:], k)


class GeoOntology:
    """
    Sets up the GeoData Ontology.
    See the `RDFLib documentation <rdflib.readthedocs.org/en/latest/index.html>`_ for
    more information.
    """

    def __init__(self, path, namespace=_GEO_NAMESPACE, frmt='turtle'):
        """
        Initializes the GeoData Ontology and backing graph
        :param path: Path to the base ontology. Can be a file, or an url.
        :param namespace: Namespace to use. Defaults to 'http://move.ugent.be/geodata/ontology/'
        :param frmt: Format of the base ontology. Defaults to 'turtle'
        :return:
        """
        self.graph = Graph()
        self.graph.parse(path, format=frmt)
        self.frmt = frmt
        self.namespace = Namespace(namespace)
        self.column_ns = Namespace(namespace + 'column/')
        self.property_ns = Namespace(namespace + 'property/')

        self.featureTypes = {
            'LineFeature': self.namespace.LineFeature,
            'PointFeature': self.namespace.PointFeature,
            'PolygonFeature': self.namespace.PolygonFeature
        }

    def add_info_column(self, defines, name='column', field='column',
                        type='string', desc='No description', unit=None):
        """
        Adds an InfoColumn to the graph
        :param defines: URI to the (type of) entity that is defined by this column.
        :param name: Name of the column.
        :param type: Type of the column. Check the ontology for the list of possibilities
        :param desc: Description of the column.
        :param unit: Unit of the column.
        :return:
        """
        col = URIRef(self.column_ns + name)

        self.graph.add((col, RDF.type, self.namespace.InfoColumn))
        self.graph.add((col, self.property_ns.name, Literal(name.lower())))
        self.graph.add((col, self.property_ns.field, Literal(field)))
        self.graph.add((col, self.property_ns.defines, URIRef(defines)))
        self.graph.add((col, self.property_ns.description, Literal(desc)))
        self.graph.add((col, self.property_ns.type, Literal(type)))
        if unit:
            self.graph.add((col, self.property_ns.unit, Literal(unit)))

    def add_geo_column(self, defines, name='column', field1=None, field2=None,
                       type='LineFeature', desc='No description'):
        """
        Adds a GeoColumn to the graph
        :param defines: URI to the (type of) entity that is defined by this column.
        :param name: Name of the column.
        :param field1: For DuoGeoColumns, the name of the first field.
        :param field2: For DuoGeoColumns, the name of the second field.
        :param type: Type of the column. Can be 'LineFeature' or 'PointFeature'.
        :param desc: Description of the column.
        :return:
        """
        col = URIRef(self.column_ns + name)

        if field1 is None or field2 is None:
            # It's a column backed by only one field
            self.graph.add((col, RDF.type, self.namespace.UniGeoColumn))
            self.graph.add((col, self.property_ns.field, Literal(name)))
        else:
            self.graph.add((col, RDF.type, self.namespace.DuoGeoColumn))
            self.graph.add((col, self.property_ns.field1, Literal(field1)))
            self.graph.add((col, self.property_ns.field2, Literal(field2)))

        self.graph.add((col, self.property_ns.name, Literal(name.lower())))
        self.graph.add((col, self.property_ns.defines, URIRef(defines)))
        self.graph.add((col, self.property_ns.description, Literal(desc)))
        self.graph.add((col, self.property_ns.type, Literal(self.featureTypes[type])))

    def serialize(self, frmt=None):
        """
        Serializes the current graph to a string
        :param frmt: Format to use for serialization. If left empty, uses the
        format set in the class constructor.
        :return:
        """
        if frmt is None:
            return self.graph.serialize(format=self.frmt)
        else:
            return self.graph.serialize(format=frmt)

    def get_columns(self, info=True, geo=True):
        result = recursive_defaultdict()

        if info:
            for s, p, o in self.graph.triples((None, RDFS.subClassOf, URIRef(_GEO_NAMESPACE + 'InfoColumn'))):
                for _s, _p, _o in self.graph.triples((None, RDF.type, s)):
                    for __s, __p, __o in self.graph.triples((_s, None, None)):
                        result['info'][_s][__p] = __o
        if geo:
            for s, p, o in self.graph.triples((None, RDFS.subClassOf, URIRef(_GEO_NAMESPACE + 'GeoColumn'))):
                for _s, _p, _o in self.graph.triples((None, RDF.type, s)):
                    for __s, __p, __o in self.graph.triples((_s, None, None)):
                        result['geo'][_s][__p] = __o

        return result

    def set_fields(self, column, field=None, field1=None, field2=None, unit=None):
        if column.startswith(_GEO_NAMESPACE):
            # Name space is already included in the name
            col_ref = URIRef(column)
        else:
            col_ref = URIRef(_GEO_NAMESPACE + "column#" + column)

        if field is not None:
            self.graph.add((col_ref, self.property_ns.field, Literal(field)))
            if unit:
                self.graph.add((col_ref, self.property_ns.unit, Literal(unit)))
        elif field1 is not None and field2 is not None:
            self.graph.add((col_ref, self.property_ns.field1, Literal(field1)))
            self.graph.add((col_ref, self.property_ns.field2, Literal(field2)))
            if unit:
                self.graph.add((col_ref, self.property_ns.unit, Literal(unit)))
        else:
            raise AssertionError("If field is none, field1 and field2 should not be none")
