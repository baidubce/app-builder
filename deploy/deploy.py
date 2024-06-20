from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient
from baidubce.services.bcc import bcc_model
from baidubce.bce_response import BceResponse
from _bcc import InnerBccClient
import time
import json
import uuid
import os
import yaml
import tarfile
from datetime import datetime


def bos_upload(config, tar_file):
    # 新建BosClient
    bos_client = BosClient(config)
    bucket_name = "appbuilder-sdk-test"

    if not bos_client.does_bucket_exist(bucket_name):
        bos_client.create_bucket(bucket_name)

    bos_client.put_object_from_file(bucket_name, "demo.tar", tar_file)
    timestamp = int(time.time())
    url = bos_client.generate_pre_signed_url(
        bucket_name, "demo.tar", timestamp, expiration_in_seconds=3600
    )
    return url


def create_security_group():
    client_token = str(uuid.uuid4())

    # 设置安全组名称
    security_group_name = "appbuilder-sdk-" + client_token

    # 设置安全组规则
    security_group_rule = bcc_model.SecurityGroupRuleModel(
        "rule_" + client_token,  # 设置备注
        "ingress",  # 设置入站/出站，取值ingress或egress，必选参数
        portRange="1-65535",  # 设置端口范围，默认空时为1-65535，可以指定80等单个端口
        protocol="",  # 设置协议类型
        sourceGroupId="",  # 设置源安全组ID
        sourceIp="",
    )  # 设置源IP地址，与sourceGroupId不能同时设定值
    security_group_rule_list = []
    security_group_rule_list.append(security_group_rule)

    # 设置安全组描述
    client.create_security_group(
        name=security_group_name,
        rules=security_group_rule_list,
        client_token=client_token,
    )


if __name__ == "__main__":
    with open("./config.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    HOST = data["bce_config"]["host"]
    BOS_HOST = data["bce_config"]["bos_host"]
    AK = data["bce_config"]["ak"]
    SK = data["bce_config"]["sk"]
    config = BceClientConfiguration(
        credentials=BceCredentials(AK, SK), endpoint=HOST)
    bos_config = BceClientConfiguration(
        credentials=BceCredentials(AK, SK), endpoint=BOS_HOST
    )
    local_dir = data["appbuilder_config"]["local_dir"]
    cmd = data["appbuilder_config"]["run_cmd"]
    # 创建tar包
    tar_file = "./demo.tar"
    with tarfile.open(tar_file, "w") as tar:
        for filename in os.listdir(local_dir):
            file_path = os.path.join(local_dir, filename)
            if os.path.isfile(file_path):
                tar.add(file_path, arcname=filename)

    url = bos_upload(bos_config, tar_file)
    client = InnerBccClient(config)
    # create_security_group()

    # 当前时间字符串
    now_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # 用户BCC创建后自动执行的启动命令，此处为示例
    user_data = (
        "#!/bin/bash\n"
        "mkdir /root/test\n"
        "cd /root/test\n"
        f"wget -O demo.tar {url.decode('utf-8')}\n"
        "tar -xvf demo.tar\n"
        "yum install -y docker\n"
        "docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.8.0\n"
        f"docker run -it --net=host -v /root/test:/home/test/ --name appbuilder-sdk registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.8.0 /bin/sh -c '{cmd}'"
    )

    spec = data["bce_config"]["spec"]
    disk_gb = int(data["bce_config"]["root_disk_size_in_gb"])
    admin_pass = data["bce_config"]["admin_pass"]

    response = client.create_instance_by_spec(
        spec=spec,  # 实例规格
        image_id="m-43wfwG1G",  # 镜像ID
        # 待创建虚拟机实例的系统盘大小，单位GB，默认是40GB，范围为[40,
        # 2048]GB，超过40GB按照云磁盘价格收费。注意指定的系统盘大小需要满足所使用镜像最小磁盘空间限制。
        root_disk_size_in_gb=disk_gb,
        network_capacity_in_mbps=1,
        name="instance-appbuilder-sdk-service-{}".format(now_str),
        hostname="host-appbuilder-sdk-service-{}".format(now_str),
        admin_pass=admin_pass,
        zone_name="cn-bj-d",
        user_data=user_data,
    )
    print(response)

    res = client.list_instances()
    print(res)
