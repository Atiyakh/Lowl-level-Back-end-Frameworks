import os, pathlib, traceback
from importlib.machinery import SourceFileLoader
models = SourceFileLoader("models", os.path.join(pathlib.Path(__file__).parent.parent.parent, 'models.py')).load_module()
fields_classes = SourceFileLoader("Models", os.path.join(pathlib.Path(__file__).parent, 'Models.py')).load_module()

class ModelsParser:
    def __init__(self):
        self.models_structure = dict()
        self.lookup_table_1 = {
            'DateTimeField': 'DATETIME',
            'DateField': 'DATE',
            'TimeField': 'TIME'
        }
        self.fields_names_list = [
            'ForeignKey', 'DecimalField','TimeField', 
            'DateTimeField','DateField', 'BoolanField',
            'AutoField', 'IntegerField','CharField',
        ]
        self.ExtractModels()
        for model in self.models:
            self.ExtractFields(model)
        self.queries = []
        for model_stucture in self.models_structure:
            self.queries.append(self.GenerateQuery(model_stucture))
        self.classes = self.OrderQuery()
        self.SQLQueriesRecorder()
    def ExtractModels(self):
        self.models = dict() 
        for obj_name in dir(models):
            try:
                obj_value = eval(f"models.{obj_name}()", globals())
                if type(obj_value).__base__.__name__ == 'Model':
                    self.models[obj_name] = obj_value
            except:pass
    def ExtractFields(self, model_name):
        model = self.models[model_name]
        fields = dict()
        for obj in dir(model):
            if type(eval(f"model.{obj}", locals())).__name__ in self.fields_names_list:
                obj_value = eval(f"model.{obj}", locals())
                obj_value.__model__ = model
                obj_value.__modelname__ = model_name
                obj_value.__fieldname__ = obj
                if type(obj_value).__name__ in self.fields_names_list:
                    fields[obj] = obj_value
        self.models_structure[(model_name, model)] = fields
    def GenerateQuery(self, model_structure):
        model_name, model_object = model_structure
        fields = self.models_structure[model_structure]
        # Extract PKs & FKs/Relationships:
        PKs = []; FKs = []
        # PKs
        for field_name in fields:
            field_object = fields[field_name]
            try:
                if field_object.__getattribute__('primary_key'):
                    PKs.append(field_name)
            except AttributeError:pass
        if len(PKs) == 0:
            fields[f'{model_name.capitalize()}ID'] = fields_classes.AutoField(primary_key=True)
            PKs.append(f'{model_name.capitalize()}ID')
        elif len(PKs)>1: raise ValueError(
            f"[WebSock] We do not support compound primary key, {PKs[0]} has been selected."
        )
        # FKs
        for field_name in fields:
            field_object = fields[field_name]
            if type(field_object).__name__ == 'ForeignKey':
                FKs.append([field_name, field_object])
        # FKs Format:
        FKs_format = []
        try:
            for FK in FKs:
                FK_name, FK_object = FK
                FK_format = f"    FOREIGN KEY ({FK_name}) REFERENCES {FK_object.to_table.__modelname__}({FK_object.to_table.__fieldname__}) "
                try:
                    if FK_object.unique == True:
                        FK_format += "UNIQUE "
                except:pass
                try:
                    if FK_object.allow_null == False:
                        FK_format += "NOT NULL "
                except:pass
                FK_format += f"ON DELETE {FK_object.on_delete.val},\n" 
                FKs_format.append(FK_format)
                fields[FK_object.__fieldname__] = eval(f"fields_classes.{type(FK_object.to_table).__name__}()", globals())
        except: raise ValueError(
            "[WebSock] ForigenKeyAssignmentError:"
        )
        # Fields Format:
        fields_format = []
        for field_name in fields:
            field_value = fields[field_name]
            if type(field_value).__name__ == 'CharField':
                f_query_format = f"    {field_name} VARCHAR({field_value.max_length})"
                if not field_value.allow_null:
                    f_query_format += " NOT NULL"
                if field_value.unique:
                    f_query_format += " UNIQUE"
                if field_value.default != None:
                    f_query_format += ' DEFAULT ?'
                f_query_format += ",\n"
            elif type(field_value).__name__ == 'IntegerField':
                f_query_format = f"    {field_name} INT"
                if not field_value.allow_null:
                    f_query_format += " NOT NULL"
                if field_value.unique:
                    f_query_format += " UNIQUE"
                if field_value.default != None:
                    f_query_format += ' DEFAULT ?'
                f_query_format += ",\n"
            elif type(field_value).__name__ == 'AutoField':
                f_query_format = f"    {field_name} INT AUTO_INCREMENT"
                f_query_format += " NOT NULL"
                if field_value.unique:
                    f_query_format += " UNIQUE"
                f_query_format += ",\n"
            elif type(field_value).__name__ == 'BooleanField':
                f_query_format = f"    {field_name} BOOLEAN"
                if not field_value.allow_null:
                    f_query_format += " NOT NULL"
                if field_value.default != None:
                    f_query_format += ' DEFAULT ?'
                f_query_format += ",\n"
            elif type(field_value).__name__ in ['DateField', 'DateTimeField', 'TimeField']:
                data_type = self.lookup_table_1[type(field_value).__name__]
                f_query_format = f"    {field_name} {data_type}"
                if not field_value.allow_null:
                    f_query_format += " NOT NULL"
                if field_value.auto_now_created:
                    f_query_format += ' AUTO NOW CREATE'
                elif field_value.auto_now_modified:
                    f_query_format += ' AUTO NOW MODIFY'
                elif field_value.default != None:
                    f_query_format += ' DEFAULT ?' # FIXME
                f_query_format += ",\n"
            elif type(field_value).__name__ == 'DecimalField':
                if field_value.max_digits and field_value.decimal_places:
                    f_query_format = f"    {field_name} DECIMAL({field_value.max_digits}, {field_value.decimal_places})"
                else:
                    f_query_format = f"    {field_name} DECIMAL"
                if not field_value.allow_null:
                    f_query_format += " NOT NULL"
                if field_value.unique:
                    f_query_format += " UNIQUE"
                if field_value.default != None:
                    f_query_format += ' DEFAULT ?'
                f_query_format += ",\n"
            elif type(field_value).__name__ == 'ForeignKey':
                continue
            fields_format.append(f_query_format)
        # Build Query
        query = f"CREATE TABLE {model_name}(\n"
        for field_format in fields_format:
            query += field_format
        for FK_format in FKs_format:
            query += FK_format
        query += f"    PRIMARY KEY ({PKs[0]})\n"
        query += ");"
        return query
    def OrderQuery(self):
        models_file = open(models.__file__, 'r')
        lines = models_file.readlines()
        models_file.close()
        classes = []
        for line in lines:
            if line.count('class') == 1:
                if line.count('(Models.Model)') == 1:
                    classes.append(line[line.find('class')+5:line.find('(Models.Models):')-15].strip())
        return classes
    padding_name = lambda _, num: ("0"*(4-len(num.__str__())))+str(num)
    def SQLQueriesRecorder(self):
        dirs = os.listdir(os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database\\schemas'))
        schema_count = 0
        for dir_ in dirs:
            try:
                num = int(dir_.split('_')[-1].split('.')[0])
                if num > schema_count: schema_count = num
            except:pass
        schema_file = open(os.path.join(os.getcwd(), 'WebApplication\\MiddleWare\\Database\\schemas', f'schema_{self.padding_name(schema_count+1)}.sql'), 'w')
        self.ordered_queries = []
        for class_ in self.classes:
            for query in self.queries:
                if class_ in query.split('\n')[0][13:]:
                    self.ordered_queries.append(query)
        content = ''
        for query in self.ordered_queries:
            content += query+'\n\n'
        schema_file.write(content[:-2])
        schema_file.close()
        print(f"[WebSock] Your schema has been saved (schema_{self.padding_name(schema_count+1)}.sql)")
