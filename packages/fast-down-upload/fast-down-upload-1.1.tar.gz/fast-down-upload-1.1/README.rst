**包安装**::

    pip install fast-down-upload

**使用例子**::

    from fast-down-upload import UploadFile,config
    from fast-down-upload import public_downupload_task,start_customer_downupload_task

    # redis连接配置
    config.redis_host = '127.0.0.1'
    config.redis_password = ''
    config.redis_port = 6379
    config.redis_db = 0

    # ALIYUN OSS配置
    config.aliyun_access_key_id = ''
    config.aliyun_access_key_secret = ''
    config.aliyun_endpoint = ''
    config.aliyun_bucket_name = ''

    for i in range(1,21):
        down_dict = {'down_url': 'https://video1.matafy.com/dyvideo/201811/6609568770908228877.mp4', 'file_name': 'test'+str(i),'file_dir': 'douyin', 'file_type': '', 'callback': None}
        public_downupload_task(down_dict)

    start_customer_downupload_task(threads_num=100)