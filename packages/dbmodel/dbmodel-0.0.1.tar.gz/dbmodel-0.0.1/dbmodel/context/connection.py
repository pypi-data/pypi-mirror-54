# -*- coding: utf-8 -*-

import sys
import re

from dbmodel.utils.inflector import Inflector, Portugues
from dbmodel.context.database import DataBase
from dbmodel.entity.datatype import ListType
from dbmodel.entity.entity import EntityStatus

sql_operators = [ '!=', '>=','>','<=','<','=', ' IS NULL ', ' NOT IS ', ' IS ', ' NOT LIKE ', ' LIKE ', ' ']
relational_types = ["Object" , "ObjectList"]

class Connection():

    def __init__(self, db_user=None, db_password=None, db_host=None, db_port=None, db_database=None, db_ssl=False, db_ssl_ca=None, db_ssl_cert=None, db_ssl_key=None):
        try:
            self._inflector = Inflector(Portugues)
            self._db = DataBase(db_user, db_password, db_host, db_port, db_database, db_ssl,db_ssl_ca, db_ssl_cert, db_ssl_key)
            self.__commit__ = []
        except Exception as e:
            raise e

    def close(self):
        self._db.close()

    #VERIFICA SE O ATRIBUTO INFORMADO É UM METODO EXISTENTE SE NÃO FOR TRATA PARA VERIFICAR SE É UMA TABELA
    def __getattr__(self, name):
        try:
            if not name in self.__dir__():
                self._table = name
                self._distinct = None
                self._select = None
                self._where = None
                self._having = None
                self._orhaving = None
                self._orwhere = None
                self._orderby = None
                self._groupby = None
                self._limit = None
                self._join = None
                self._include = None
                classname =  self._inflector.classify(name)
                self._class = getattr(__import__('model.{0}'.format(classname.lower()), fromlist=[classname]), classname)
                self._klass = self._class()
            else:
                return None
            return self
        except Exception as e:
            raise  e

    # VERIFICAÇÃO SE HÁ OPERADOR NO CAMPO
    def __operator_check(self, field):
        exists_operator = [operator in field for operator in sql_operators]
        if any(exists_operator):
            field = field.strip().split(sql_operators[exists_operator.index(True)])
            field[0] = field[0].strip()
            field.insert(1, sql_operators[exists_operator.index(True)])
        return field

    def __valid_table(self):
        if not "_table" in self.__dir__():
            raise Exception("table not selected")


    def __validate_field(self, field):
        field = field.strip()
        if not "." in field and field in self._class.__dict__:
            return "{}.{}".format(self._table, field)
        elif field.split(".")[0] == self._table and field.split(".")[1] == "*":
            return field
        elif field.split(".")[0] == self._table and field.split(".")[1].strip() in self._class.__dict__:
            return field
        elif field.split(".")[0] in self._class.__dict__:
            return field
        # TODO VALIDADE FIELD WITH FUNCTION
        return field

    def __valid_field(self, field):
        if isinstance(field, str):
            field = self.__validate_field(field)
        elif isinstance(field, list):
            field[0] = self.__validate_field(field[0])
        return field

    def __valid_relational_table(self, table):
        try:
            table = table.strip()
            if getattr(self._class, table).__class__.__name__ in relational_types:
                return table
            raise Exception("{} table does not exist in relational list".format(table))
        except Exception as e:
            raise Exception("{} table does not exist in relational list".format(table))

    # VALIDAÇÃO DE CAMPOS
    def __check_fields(self, *fields, check_operator=False):
        self.__valid_table()
        list_fields = []
        for field in fields:
            if len(re.findall(r"(([a-z]|[A-Z]|[0-9]|\'|\*){1},{1}\ )", field))>0:
                for item_field in field.split(","):
                    if check_operator:
                        item_field = self.__operator_check(item_field)
                    list_fields.append(self.__valid_field(item_field))
            else:
                if check_operator:
                    field = self.__operator_check(field)
                list_fields.append(self.__valid_field(field))
        return list_fields

    def __check_tables(self, *tables):
        self.__valid_table()
        list_tables = []
        for table in tables:
            if len(re.findall(r"(([a-z]|[A-Z]|[0-9]|\'|\*){1},{1}\ )", table))>0:
                for item_table in table.split(","):
                    list_tables.append(self.__valid_relational_table(item_table))
            else:
                list_tables.append(self.__valid_relational_table(table))
        return list_tables


    def distinct(self, *fields):
        try:
            self._distinct = self.__check_fields(*fields)
            return self
        except Exception as e:
            raise e

    def select(self, *fields):
        try:
            self._select = self.__check_fields(*fields)
            return self
        except Exception as e:
            raise e

    def where(self, *fields):
        try:
            self._where = self.__check_fields(*fields, check_operator=True)
            return self
        except Exception as e:
            raise e

    def orwhere(self, *fields):
        try:
            if not self._where  or len(self._where) == 0:
                raise Exception("To use ORWHERE required use before WHERE clause")
            self._orwhere = self.__check_fields(*fields, check_operator=True)
            return self
        except Exception as e:
            raise e

    def having(self, *fields):
        try:
            self._having = self.__check_fields(*fields, check_operator=True)
            return self
        except Exception as e:
            raise e

    def orhaving(self, *fields):
        try:
            if not self._having  or len(self._having) == 0:
                raise Exception("To use ORHAVING required use before HAVING clause")
            self._orhaving = self.__check_fields(*fields, check_operator=True)
            return self
        except Exception as e:
            raise e

    def orderby(self, *fields):
        try:
            self._orderby =  [order if isinstance(order, list) else [order," ", "ASC"] for order in self.__check_fields(*fields, check_operator=True)]
            return self
        except Exception as e:
            raise e

    def groupby(self, *fields):
        try:
            self._groupby = self.__check_fields(*fields, check_operator=True)
            return self
        except Exception as e:
            raise e

    def limit(self, start, end):
        try:
            self._limit = (start, end)
            return self
        except Exception as e:
            raise e

    def join(self, *tables):
        self._join = self.__check_tables(*tables)
        return self

    def include(self, *tables):
        self._include = self.__check_tables(*tables)
        return self


    def format_join(self, _SELECT, _FROM, _LIST, _TYPE):

        for join in _LIST:
            _SELECT_JOIN = ""

            if not self._select or len(self._select) == 0 or "%s.*"%join in self._select:
                _SELECT_JOIN = ", ".join(["{0}.{1} AS '{0}.{1}'".format(join, field) for field in self._class.__dict__[join].type.__dict__ if not field.startswith("_") and not self._class.__dict__[join].type.__dict__[field].__class__.__name__.startswith("Object")])
            else:
                _SELECT_JOIN = ", ".join(["%s AS '%s'"%(_selected, _selected) for _selected in self._select if "." in _selected and "%s."%join in _selected])

            _FROM_JOIN = "{0} JOIN {1} AS {2} ON {2}.{3} = {4}.{5}".format(
                _TYPE,
                self._class.__dict__[join].__dict__["table"],
                join,
                self._class.__dict__[join].__dict__["key"],
                self._table,
                self._class.__dict__[join].__dict__["reference"],
            )

            _JOIN_CONDITION = [" ".join(condition) for condition in self._where if "%s."%join in condition[0]] if self._where else []
            if len(_JOIN_CONDITION)>0:
                _FROM_JOIN = "{} AND {}".format(_FROM_JOIN, " AND ".join(_JOIN_CONDITION))

            if _SELECT_JOIN != "":
                _SELECT = "{}, {}".format(_SELECT, _SELECT_JOIN)

            _FROM = "{} {}".format(_FROM, _FROM_JOIN)

        return _SELECT, _FROM

    def _write_select_query(self, object=True):

        self.__valid_table()

        # FORMATA SELECT QUERY
        if object:
            if not self._select or len(self._select) == 0 or "%s.*"%self._table in self._select:
                _SELECT = ", ".join(["{0}.{1} AS '{0}.{1}'".format(self._table, field) for field in self._class.__dict__ if not field.startswith("_") and not self._class.__dict__[field].__class__.__name__.startswith("Object")])
            else:
                for pk in self._class.__primary_key__:
                    self._select.append("{}.{}".format(self._table, pk))
                _SELECT = ", ".join(["%s AS '%s'"%(_selected, _selected) for _selected in self._select if "%s."%self._table in _selected])
        else:
            if not self._select or len(self._select) == 0 or "%s.*"%self._table in self._select:
                _SELECT = "%s.*"%self._table
            else:
                _SELECT = ", ".join([_selected for _selected in self._select if not  "." in _selected or "%s."%self._table in _selected])


        if self._distinct and len(self._distinct)>0:
            _SELECT = "{}, {}".format("DISTINCT({})".format(",".join(self._distinct)), _SELECT)

        _FROM = self._table

        if self._join and len(self._join) > 0:
            _SELECT, _FROM = self.format_join(_SELECT, _FROM, self._join, "INNER")

        if self._include and len(self._include) > 0:
            _SELECT, _FROM = self.format_join(_SELECT, _FROM, self._include, "LEFT")

        _QUERY = "SELECT {} FROM {}".format(_SELECT, _FROM)

        if self._where and len(self._where) > 0:
            condition_table = ["".join(condition).strip() for condition in self._where if not "." in condition[0] or "%s."%self._table in condition[0]]
            if len(condition_table)>0:
                _WHERE = " AND ".join(condition_table)
                _QUERY = "{} WHERE ({})".format(_QUERY, _WHERE)
        if self._orwhere and len(self._orwhere) > 0:
            _ORWHERE = " AND ".join(["".join(condition).strip() for condition in self._orwhere if not "." in condition[0] or "%s."%self._table in condition[0]])
            _QUERY = "{} OR ({})".format(_QUERY, _ORWHERE)
        if self._groupby and len(self._groupby) > 0:
            _GROUPBY = " ".join(self._groupby)
            _QUERY = "{} GROUP BY {}".format(_QUERY, _GROUPBY)
        if self._having and len(self._having) > 0:
            _HAVING = " AND ".join(["".join(condition).strip() for condition in self._having if not "." in condition[0] or "%s."%self._table in condition[0]])
            _QUERY = "{} HAVING ({})".format(_QUERY, _HAVING)
        if self._orhaving and len(self._orhaving) > 0:
            _ORHAVING = " AND ".join(["".join(condition).strip() for condition in self._orhaving if not "." in condition[0] or "%s."%self._table in condition[0]])
            _QUERY = "{} OR ({})".format(_QUERY, _ORHAVING)
        if self._orderby and len(self._orderby) > 0:
            _ORDERBY = ", ".join(["".join(condition).strip() for condition in self._orderby])
            _QUERY = "{} ORDER BY {}".format(_QUERY, _ORDERBY)
        if self._limit:
            _QUERY = "{} LIMIT {},{}".format(_QUERY, self._limit[0], self._limit[1])

        return _QUERY

    def insert_query(self, obj):
        obj_data = obj.toDB()
        sql_statement = "INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE {onkeys}".format(
            table = obj.__table__,
            keys = ", ".join(obj_data.keys()),
            values = ", ".join(["%({0})s".format(field) for field in obj_data.keys()]),
            onkeys = ", ".join(["{0}=%({0})s".format(field)for field in obj_data.keys()])
        )
        last_row_id = self._db.save(sql_statement, obj_data)
        if last_row_id:
            obj.__dict__[obj.__primary_key__[0]] = last_row_id

    # EXECUÇÃO DE COMANDO

    def save(self):
        for obj_to_commit in self.__commit__:
            if obj_to_commit.__status__ == EntityStatus.modified or obj_to_commit.__status__ == EntityStatus.addedobject:
                # PRIMEIRO OBJETO PRINCIPAL
                if obj_to_commit.__status__ == EntityStatus.modified:
                     self.insert_query(obj_to_commit)
                # DO OBJECTS LIST
                sub_objects = [ sub_obj for sub_obj in obj_to_commit.__commit__ if sub_obj.__status__ == EntityStatus.modified ]
                for sub_object in sub_objects:
                    field_data = [value for field, value in obj_to_commit.__dict__.items() if field.startswith("__") and not field.endswith("__") and hasattr(value,"table") and value.table == sub_object.__table__ and value.__class__.__name__== "ObjectList"]
                    if len(field_data)==1:
                        #SET KEY FROM PK OBJ
                        setattr(sub_object, field_data[0].key, obj_to_commit.__dict__[field_data[0].reference])
                        self.insert_query(sub_object)
        self._db.commit()

    def add(self, obj = None):
        try:
            if obj!=None:
                if isinstance(obj, self._class):
                    obj.__status__ == EntityStatus.modified
                    self.__commit__.append(obj)
                else:
                    raise Exception("{} table requires {} object".format(self._table, self._class.__name__))
            return None
        except Exception as e:
            raise e

    @property
    def first(self):
        query = self._write_select_query()
        try:
            result = self.__fill(self._db.fetchall(query), self._class)
            return result[0] if len(result)>0 else None
        except Exception as e:
            print(e)
            print("\n\n ERRO QUERY: \n\n {} \n\n".format(query))

    @property
    def all(self):
        query = self._write_select_query()
        try:
            result = self._db.fetchall(query)
            return self.__fill(result, self._class)
        except Exception as e:
            print(e)
            print("\n\n ERRO QUERY: \n\n {} \n\n".format(query))


    # EXECUÇÃO DE COMANDO
    @property
    def fetch(self):
        query = self._write_select_query()
        try:
            return self._db.fetchall(self._write_select_query(False))
        except Exception as e:
            print(e)
            print("\n\n ERRO QUERY: \n\n {} \n\n".format(query))

    def query(self, query, model=None):
        result = self._db.fetchall(query)
        if model:
            return self.__fill(result, model)
        return result

    def __fill(self, data, model):
        object_list = ListType(context=self, type=model)
        for row in data:
            row = {k:v for k,v in row.items() if v is not None}
            object_exit = [obj for obj in object_list if all([getattr(obj, key) == row["%s.%s"%(self._table, key)] for key in self._class.__primary_key__])]
            if len(object_exit)==0:
                obj = model(context=self, **row)
                object_list.append(obj)
            else :
                object_exit[0].__setrelattr__(**row)
        return object_list
