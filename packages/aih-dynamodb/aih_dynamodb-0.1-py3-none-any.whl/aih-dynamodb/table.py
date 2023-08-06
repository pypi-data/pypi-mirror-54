import boto3
import json
from uuid import uuid4
from dynamodb_json import json_util

class Table:
    def __init__(self, table_name):
        self._table_name = table_name
        self._dynamodb = boto3.client("dynamodb", region_name="us-east-1")

    def getRecords(self, params):
        params["TableName"] = self._table_name
        result = self._dynamodb.scan(**params)
        return json_util.loads(result["Items"])

    def getRecordById(self, id):
        params = self._getParamsForGetRecordById(id)
        result = self._dynamodb.get_item(**params)
        return json_util.loads(result["Item"])

    def _getParamsForGetRecordById(self, id, attributes_to_get=None):
        params = self._getSubParamsWithIdAndTableName(id)
        
        if (attributes_to_get):
            params["AttributesToGet"] = attributes_to_get

        return params
    

    def _getSubParamsWithIdAndTableName(self, id):
        params = {
            "TableName": self._table_name,
            "Key": {
                "id": {
                    "S": id
                }
            }
        }

        return params
    
    def _randomId(self):
        return str(uuid4())
    
    def insertRecord(self, data):
        included_id_data = self._injectIdForRecord(data)
        params = self._getParamsForInsertRecord(included_id_data)
        
        self._dynamodb.put_item(**params)
        return included_id_data
    
    def _getParamsForInsertRecord(self, included_id_data):
        params = {
            "TableName": self._table_name,
            "Item": json.loads(json_util.dumps(included_id_data)),
            "ReturnValues": "ALL_OLD"
        }

        return params
    
    def _injectIdForRecord(self, record):
        id = self._randomId()
        included_id_record = {
            **record,
            "id": id
        }

        return included_id_record
    
    def deleteRecordById(self, id):
        params = self._getParamsForDeleteRecordById(id)
        
        try:
            self._dynamodb.delete_item(**params)
            return True
        except:
            return False
    

    def _getParamsForDeleteRecordById(self, id):
        params = self._getSubParamsWithIdAndTableName(id)
        return params
    
    def deleteRecordsByIds(self, ids):
        params = self._getParamsForDeleteRecordsByIds(ids)
        
        try:
            self._dynamodb.batch_write_item(**params)
            return True
        except:
            return False
    

    def _getParamsForDeleteRecordsByIds(self, ids):
        request_items = {}

        def _getParamsForDeleteRecord(id):
            return {
                "DeleteRequest": {
                    "Key": {
                        "id": {
                            "S": id
                        }
                    }
                }
            }

        request_items[self._table_name] = list(map(_getParamsForDeleteRecord, ids))
        params = {
            "RequestItems": request_items,
            "ReturnConsumedCapacity": "TOTAL"
        }

        return params
    
    def insertRecords(self, records):
        included_id_records = list(map(lambda record: self._injectIdForRecord(record), records))
        params = self._getParamForInsertRecords(included_id_records)
        self._dynamodb.batch_write_item(**params)

        return list(map(lambda record: record["id"], included_id_records))

    def _getParamForInsertRecords(self, included_id_records):
        request_items = {}

        def _getParamsForInsertRecord(included_id_record):
            return {
                "PutRequest": {
                    "Item": json.loads(json_util.dumps(included_id_record))
                }
            }

        request_items[self._table_name] = list(map(_getParamsForInsertRecord, included_id_records))
        params = {
            "RequestItems": request_items,
            "ReturnConsumedCapacity": "TOTAL"
        }

        return params
    
    def updateRecordById(self, id, new_data):
        params = self._getParamsForUpdateRecordById(id, new_data)
        result = self._dynamodb.update_item(**params)
        return json_util.loads(result["Attributes"])

    def _getParamsForUpdateRecordById(self, id, new_data):
        params = self._getSubParamsWithIdAndTableName(id)
        update_expression = self._getUpdateExpressionForUpdateRecordById(new_data)
        expression_attribute_names = self._getExpressionAttributeNamesForUpdateRecordById(new_data)
        expression_attribute_values = self._getExpressionAttributeValuesForUpdateRecordById(new_data)

        params["UpdateExpression"] = update_expression
        params["ExpressionAttributeNames"] = expression_attribute_names
        params["ExpressionAttributeValues"] = expression_attribute_values
        params["ReturnValues"] = "ALL_NEW"

        return params
    

    def _getUpdateExpressionForUpdateRecordById(self, new_data):
        return "SET " + ",".join(list(map(lambda key: "#{key}=:{key}".format(key=key), new_data.keys())))
    

    def _getExpressionAttributeNamesForUpdateRecordById(self, new_data):
        result = {}
        for key in new_data.keys():
            result["#{key}".format(key=key)] = key
    
        return result
    

    def _getExpressionAttributeValuesForUpdateRecordById(self, new_data):
        result = {}
        for key in new_data.keys():
            result[":{key}".format(key=key)] = new_data[key]
        return json.loads(json_util.dumps(result))
    
    

    