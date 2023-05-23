# main函数
import datetime
import uuid
def main():
    # 生成随机日志，发送到kinesis
    for i in range(10):
        log = generate_log()
        put_log_to_kinesis(log)


# generate_log函数
def generate_log():
    # 生成随机日志
    log = {
        'log_id': str(uuid.uuid4()),
        'timestamp': str(datetime.now()),
        'message': 'This is a test log.'
    }
    return log


def put_log_to_kinesis(log):
    pass