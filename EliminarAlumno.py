import boto3

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        ReturnValues='ALL_OLD'   # para saber qué se borró
    )

    # Si no había item
    if 'Attributes' not in response:
        return {
            'statusCode': 404,
            'message': 'Alumno no encontrado para eliminar',
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }

    return {
        'statusCode': 200,
        'message': 'Alumno eliminado',
        'alumno': response['Attributes']
    }
