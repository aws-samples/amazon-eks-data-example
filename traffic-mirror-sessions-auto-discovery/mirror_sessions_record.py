import boto3

# 创建一个DynamoDB客户端对象
dynamodb = boto3.client('dynamodb')

# 创建一个EC2客户端对象
ec2 = boto3.client('ec2')

# 定义一个方法，用来记录Traffic Mirror Target和Session的数量
def record_traffic_mirror_target_session_count(table_name):
    # 创建一个DynamoDB表来存储Traffic Mirror Target和Session的数量
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'TargetId',
                'KeyType': 'HASH'  # 分区键
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'TargetId',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # 等待表创建完成
    dynamodb.get_waiter('table_exists').wait(TableName=table_name)

    # 获取所有的Traffic Mirror Target的信息
    response = ec2.describe_traffic_mirror_targets()

    # 对于每个Traffic Mirror Target，获取它绑定的Session的数量并存储到DynamoDB表中
    for target in response['TrafficMirrorTargets']:
        target_id = target['TrafficMirrorTargetId']
        # 获取这个目标绑定的Session的数量
        session_response = ec2.describe_traffic_mirror_sessions(
            Filters=[
                {
                    'Name': 'traffic-mirror-target-id',
                    'Values': [target_id]
                }
            ]
        )
        session_count = len(session_response['TrafficMirrorSessions'])
        # 将目标ID和Session数量存储到DynamoDB表中
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'TargetId': {'S': target_id},
                'SessionCount': {'N': str(session_count)}
            }
        )
