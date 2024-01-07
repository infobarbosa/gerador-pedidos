import boto3
import time

def get_shard_iterator(stream_name, shard_id):
    client = boto3.client('kinesis')
    response = client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )
    return response['ShardIterator']

def read_stream_data(shard_iterator):
    client = boto3.client('kinesis')
    while True:
        response = client.get_records(
            ShardIterator=shard_iterator,
            Limit=1
        )
        shard_iterator = response['NextShardIterator']
        if response['Records']:
            for record in response['Records']:
                print(record['Data'])
#        time.sleep(1) # descomente essa linha para ler os dados mais lentamente

def main():
    stream_name = 'pedidos'
    shard_id = 'shardId-000000000000'  # substitua pelo seu shard id
    shard_iterator = get_shard_iterator(stream_name, shard_id)
    read_stream_data(shard_iterator)

if __name__ == "__main__":
    main()