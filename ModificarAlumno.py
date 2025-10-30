import boto3

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # dict con los campos a modificar, por ej: {"nombres": "...", "carrera": "..."}
    alumno_datos = event['body']['alumno_datos']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    # Construimos el update dinámico
    update_expr_parts = []
    expr_attr_values = {}
    expr_attr_names = {}

    for i, (k, v) in enumerate(alumno_datos.items()):
        # #n0 = :v0, #n1 = :v1, ...
        name_key = f"#n{i}"
        value_key = f":v{i}"
        update_expr_parts.append(f"{name_key} = {value_key}")
        expr_attr_names[name_key] = k
        expr_attr_values[value_key] = v

    update_expression = "SET " + ", ".join(update_expr_parts)

    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )

    return {
        'statusCode': 200,
        'message': 'Alumno actualizado',
        'alumno': response['Attributes']
    }
