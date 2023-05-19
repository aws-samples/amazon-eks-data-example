# 导入需要的模块
import boto3
import json

# 创建ec2和traffic mirror的客户端
ec2_client = boto3.client('ec2')
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

# 定义一个函数，监控ec2的启动事件，并执行相应的操作
def monitor_ec2_launch():
    # 创建一个事件桥接的客户端
    event_client = boto3.client('events')
    # 创建一个规则，匹配ec2的启动事件
    rule_name = 'ec2-launch-rule'
    event_pattern = json.dumps({
        "source": ["aws.ec2"],
        "detail-type": ["EC2 Instance State-change Notification"],
        "detail": {
            "state": ["running"]
        }
    })
    event_client.put_rule(
        Name=rule_name,
        EventPattern=event_pattern,
        State='ENABLED'
    )
    # 创建一个目标，指向一个lambda函数（需要提前创建）
    target_arn = 'arn:aws:lambda:us-east-1:123456789012:function:ec2-launch-handler' # 修改为实际的lambda函数arn
    event_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': target_arn
            }
        ]
    )