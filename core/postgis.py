from sqlalchemy.types import UserDefinedType
from sqlalchemy.sql import expression
from sqlalchemy import event, func, select, Table
import binascii

# Python datatypes
class GisElement(object):
    """ Represents a geometry value.
    """

    def __str__(self):
        return self.desc

    def __repr__(self):
        return "<%s at 0x%x; %r>" % (self.__class__.__name__,
                                    id(self), self.desc)

class BinaryGisElement(GisElement, expression.Function):
    """ Represents a Geometry value expressed as binary.
    """

    def __init__(self, data):
        self.data = data
        expression.Function.__init__(self, "ST_GeomFromEWKB", data,
                                    type_=Geometry(coerce_="binary"))

    @property
    def desc(self):
        return self.as_hex

    @property
    def as_hex(self):
        return binascii.hexlify(self.data)

class TextualGisElement(GisElement, expression.Function):
    """ Represents a Geometry value expressed as text.
    """

    def __init__(self, desc, srid=-1):
        self.desc = desc
        expression.Function.__init__(self, "ST_GeomFromText", desc, srid,
                                    type_=Geometry)


# SQL datatypes.
class Geometry(UserDefinedType):
    """ Base PostGIS Geometry column type.
    """

    name = "GEOMETRY"

    def __init__(self, dimension=None, srid=-1,
                coerce_="text"):
        self.dimension = dimension
        self.srid = srid
        self.coerce = coerce_

    class comparator_factory(UserDefinedType.Comparator):
        """ Define custom operations for geometry types.
        """

        # override the __eq__() operator
        def __eq__(self, other):
            return self.op('~=')(other)

        # add a custom operator
        def intersects(self, other):
            return self.op('&&')(other)

        # any number of GIS operators can be overridden/added here using the techniques above.

    def _coerce_compared_value(self, op, value):
        return self

    def get_col_spec(self):
        return self.name

    def bind_expression(self, bindvalue):
        if self.coerce == "text":
            return TextualGisElement(bindvalue)
        elif self.coerce == "binary":
            return BinaryGisElement(bindvalue)
        else:
            assert False

    def column_expression(self, col):
        if self.coerce == "text":
            return func.ST_AsText(col, type_=self)
        elif self.coerce == "binary":
            return func.ST_AsBinary(col, type_=self)
        else:
            assert False

    def bind_processor(self, dialect):
        def process(value):
            if isinstance(value, GisElement):
                return value.desc
            else:
                return value
        return process

    def result_processor(self, dialect, coltype):
        if self.coerce == "text":
            fac = TextualGisElement
        elif self.coerce == "binary":
            fac = BinaryGisElement
        else:
            assert False
        def process(value):
            if value is not None:
                return fac(value)
            else:
                return value
        return process

    def adapt(self, impltype):
        return impltype(dimension=self.dimension,
                srid=self.srid, coerce_=self.coerce)

# other datatypes can be added as needed.

class Point(Geometry):
    name = 'POINT'

class Curve(Geometry):
    name = 'CURVE'

class LineString(Curve):
    name = 'LINESTRING'

# ... etc.


# DDL integration
# PostGIS historically has required AddGeometryColumn/DropGeometryColumn
# and other management methods in order to create PostGIS columns.  Newer
# versions don't appear to require these special steps anymore.  However,
# here we illustrate how to set up these features in any case.

def setup_ddl_events():
    @event.listens_for(Table, "before_create")
    def before_create(target, connection, **kw):
        dispatch("before-create", target, connection)

    @event.listens_for(Table, "after_create")
    def after_create(target, connection, **kw):
        dispatch("after-create", target, connection)

    @event.listens_for(Table, "before_drop")
    def before_drop(target, connection, **kw):
        dispatch("before-drop", target, connection)

    @event.listens_for(Table, "after_drop")
    def after_drop(target, connection, **kw):
        dispatch("after-drop", target, connection)

    def dispatch(event, table, bind):
        if event in ('before-create', 'before-drop'):
            regular_cols = [c for c in table.c if not
                                    isinstance(c.type, Geometry)]
            gis_cols = set(table.c).difference(regular_cols)
            table.info["_saved_columns"] = table.c

            # temporarily patch a set of columns not including the
            # Geometry columns
            table.columns = expression.ColumnCollection(*regular_cols)

            if event == 'before-drop':
                for c in gis_cols:
                    bind.execute(
                            select([
                                func.DropGeometryColumn(
                                    'public', table.name, c.name)],
                                    autocommit=True)
                            )

        elif event == 'after-create':
            table.columns = table.info.pop('_saved_columns')
            for c in table.c:
                if isinstance(c.type, Geometry):
                    bind.execute(
                            select([
                                    func.AddGeometryColumn(
                                        table.name, c.name,
                                        c.type.srid,
                                        c.type.name,
                                        c.type.dimension)],
                                autocommit=True)
                        )
        elif event == 'after-drop':
            table.columns = table.info.pop('_saved_columns')
setup_ddl_events()