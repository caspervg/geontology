from rdflib import Graph, Namespace, URIRef, RDF, Literal, RDFS, BNode
from rdflib.plugins.sparql import prepareQuery

_GEO_NAMESPACE = 'http://move.ugent.be/geodata/ontology/'


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

        self.featureTypes = {
            'LineFeature': self.namespace.LineFeature,
            'PointFeature': self.namespace.PointFeature,
            'PolygonFeature': self.namespace.PolygonFeature
        }

    def add_info_column(self, workspace, data, defines, name='column', type='string', desc='No description', unit=None):
        """
        Adds an InfoColumn to the graph
        :param workspace: Name of the workspace of the column (for namespacing)
        :param data: Name of the datafile of the column (for namespacing)
        :param defines: URI to the (type of) entity that is defined by this column.
        :param name: Name of the column.
        :param type: Type of the column. Check the ontology for the list of possibilities
        :param desc: Description of the column.
        :return:
        """
        col = URIRef(_GEO_NAMESPACE + workspace + "/" + data + "/column/" + name)

        self.graph.add((col, RDF.type, self.namespace.InfoColumn))
        self.graph.add((col, self.namespace.name, Literal(name)))
        self.graph.add((col, self.namespace.defines, URIRef(defines)))
        self.graph.add((col, self.namespace.description, Literal(desc)))
        self.graph.add((col, self.namespace.type, Literal(type)))

        if unit is not None:
            unit_instance = BNode()
            self.graph.add((unit_instance, RDF.type, URIRef(unit)))
            self.graph.add((col, self.namespace.unit, unit_instance))

    def add_geo_column(self, workspace, data, defines, name='column', field1=None, field2=None,
                       type='LineFeature', desc='No description'):
        """
        Adds a GeoColumn to the graph
        :param workspace: Name of the workspace of the column (for namespacing)
        :param data: Name of the datafile of the column (for namespacing)
        :param defines: URI to the (type of) entity that is defined by this column.
        :param name: Name of the column.
        :param field1: For DuoGeoColumns, the name of the first field.
        :param field2: For DuoGeoColumns, the name of the second field.
        :param type: Type of the column. Can be 'LineFeature' or 'PointFeature'.
        :param desc: Description of the column.
        :return:
        """
        col = URIRef(_GEO_NAMESPACE + workspace + "/" + data + "/column/" + name)

        if field1 is None or field2 is None:
            # It's a column backed by only one field
            self.graph.add((col, RDF.type, self.namespace.UniGeoColumn))
            self.graph.add((col, self.namespace.name, Literal(name)))
        else:
            self.graph.add((col, RDF.type, self.namespace.DuoGeoColumn))
            self.graph.add((col, self.namespace.name, Literal(name)))
            self.graph.add((col, self.namespace.name1, Literal(field1)))
            self.graph.add((col, self.namespace.name2, Literal(field2)))

        self.graph.add((col, self.namespace.defines, URIRef(defines)))
        self.graph.add((col, self.namespace.description, Literal(desc)))
        self.graph.add((col, self.namespace.type, Literal(self.featureTypes[type])))

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

    def get_columns(self, workspace=None, data=None):
        """
        Uses a SPARQL query to retrieve all columns in given workspace and dataset.
        If both workspace and data are left empty, all columns in the graph will be returned
        :param workspace: Name of the workspace
        :param data: Name of the dataset
        :return:
        """
        ns = self.namespace

        if workspace is not None:
            ns = ns + workspace
            if data is not None:
                ns = ns + "/" + data

        qry = prepareQuery("""
        SELECT DISTINCT ?entity
        WHERE {
            ?entity rdf:type ?type .
            ?type rdfs:subClassOf* :Column .
            FILTER(STRSTARTS(STR(?entity), \"""" + ns + """")) .
        }""", initNs={"rdf": RDF, "rdfs": RDFS, "": self.namespace})

        return self.graph.query(qry)