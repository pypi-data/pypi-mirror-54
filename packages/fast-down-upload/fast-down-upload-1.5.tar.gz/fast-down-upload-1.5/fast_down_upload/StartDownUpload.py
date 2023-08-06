# -*- coding:utf-8 -*-
# @Author cc
# @TIME 2019/10/21 23:12
import json

from loguru import logger
from redis_queue_tool import RedisQueue
from redis_queue_tool.RedisQueue import RedisPublish, RedisCustomer

# redis连接配置
from fast_down_upload import configs as config
from fast_down_upload.DownLoad import DownloadVideo
from fast_down_upload.UploadFile import UploadloadVideo

RedisQueue.redis_host = config.redis_host
RedisQueue.redis_password = config.redis_password
RedisQueue.redis_port = config.redis_port
RedisQueue.redis_db = config.redis_db

quenen_name = 'wait_down_upload_file_queue'


def public_downupload_task(down_dict):
    # down_dict = {'down_url':'','file_name':'','file_dir': '','file_type':'','callback':None}
    redis_pub = RedisPublish(queue_name=quenen_name, fliter_rep=False)
    redis_pub.publish_redispy_str(json.dumps(down_dict))


def down_upload_file(msg):
    logger.info(msg)
    msg_dict = json.loads(msg)
    down_url = msg_dict.get('down_url')
    file_name = msg_dict.get('file_name')
    file_dir = msg_dict.get('file_dir')
    file_type = msg_dict.get('file_type')
    callback = msg_dict.get('callback')
    only_down = msg_dict.get('only_down',0)

    download_video  = DownloadVideo(down_url, file_name=file_name, file_dir=file_dir, file_type=file_type, callback=callback)
    download_video.download_video()
    if only_down!=0:
        uploadloadVideo = UploadloadVideo(down_url, file_name=file_name, file_dir=file_dir, file_type=file_type, callback=callback)
        uploadloadVideo.upload_video()


def start_customer_downupload_task(threads_num=100):
    # 多线程消费
    redis_customer = RedisCustomer(quenen_name, consuming_function=down_upload_file, threads_num=threads_num)
    redis_customer.start_consuming_message()


if __name__ == '__main__':
    for i in range(1,21):
        down_dict = {'down_url': 'https://video1.matafy.com/dyvideo/201811/6609568770908228877.mp4', 'file_name': 'test'+str(i),'file_dir': 'douyin', 'file_type': '', 'callback': None}
        public_downupload_task(down_dict)

    start_customer_downupload_task(threads_num=100)