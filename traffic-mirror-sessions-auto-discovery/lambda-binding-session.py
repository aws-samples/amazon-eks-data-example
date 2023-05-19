# 在lambda函数中，获取事件中的ec2 id，调用之前定义的函数，将其加入到指定的traffic mirror session中
# 以下是lambda函数的示例代码（需要在lambda控制台中创建和配置）
    
import json
import boto3

# 创建traffic mirror的客户端
tm_client = boto3.client('ec2', region_name='us-east-1')

# 定义一个函数，根据ec2的id获取其网卡id
def get_eni_id(ec2_id):
    response = ec2_client.describe_instances(InstanceIds=[ec2_id])
    eni_id = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['NetworkInterfaceId']
    return eni_id

# 定义一个函数，根据traffic mirror session的id获取其过滤器id和目标id
def get_tm_filter_and_target(tm_session_id):
    response = tm_client.describe_traffic_mirror_sessions(TrafficMirrorSessionIds=[tm_session_id])
    tm_filter_id = response['TrafficMirrorSessions'][0]['TrafficMirrorFilterId']
    tm_target_id = response['TrafficMirrorSessions'][0]['TrafficMirrorTargetId']
    return tm_filter_id, tm_target_id

# 定义一个函数，创建一个新的traffic mirror session，参数为源网卡id，过滤器id和目标id
def create_tm_session(source_eni_id, tm_filter_id, tm_target_id):
    response = tm_client.create_traffic_mirror_session(
        NetworkInterfaceId=source_eni_id,
        TrafficMirrorFilterId=tm_filter_id,
        TrafficMirrorTargetId=tm_target_id,
        SessionNumber=1 # 可以根据需要修改
    )
    return response['TrafficMirrorSession']['TrafficMirrorSessionId']

# 定义lambda函数的主逻辑
def lambda_handler(event, context):
    # 获取事件中的ec2 id
    ec2_id = event['detail']['instance-id']
    # 获取源网卡id
    source_eni_id = get_eni_id(ec2_id)
    # 指定要加入的traffic mirror session id（可以根据需要修改）
    tm_session_id = 'tms-12345678'
    # 获取过滤器id和目标id
    tm_filter_id, tm_target_id = get_tm_filter_and_target(tm_session_id)
    # 创建新的traffic mirror session
    new_tm_session_id = create_tm_session(source_eni_id, tm_filter_id, tm_target_id)
    # 返回结果
    return {
        'statusCode': 200,
        'body': json.dumps('New traffic mirror session created: ' + new_tm_session_id)
    }
