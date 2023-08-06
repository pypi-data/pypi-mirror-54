import boto3
from .table import Table

class Database:
    def __init__(self, app_id):
        self._prefix = "{}_".format(app_id)
        self._dynamodb = boto3.client("dynamodb", region_name="us-east-1")

    def getTable(self, table_name):
        real_table_name = "{prefix}{table_name}".format(prefix=self._prefix, table_name=table_name)
        return Table(real_table_name)
    
    # def listTables(self, exclusive_start_table_name=None, limit=100):
    #     params = self._getParamsForListTables(exclusive_start_table_name, limit)
    #     result = self._dynamodb.list_tables(**params)
    #     return result["TableNames"]

    # def _getParamsForListTables(self, exclusive_start_table_name, limit):
    #     prefix = "{}{}".format(self._prefix, exclusive_start_table_name or "")
    #     print(prefix)
    #     params = {
    #         "ExclusiveStartTableName": "sagemaker",
    #         "Limit": limit
    #     }
    #     return params
    