import time
import uuid
import os
import yaml
import tarfile
from datetime import datetime

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient
from baidubce.services.bcc import bcc_model
from baidubce.bce_response import BceResponse
from _bcc import InnerBccClient


class AppbuilderSDKInstance:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.bce_config = self.config["bce_config"]
        self.appbuilder_config = self.config["appbuilder_config"]
        self.env = self.config["env"]

        self.tar_file_name = "./demo.tar"
        self.tar_bos_url = ""

        self.instance_id = None
        self.public_ip = None

        self.credentials = BceCredentials(
            self.bce_config["ak"], self.bce_config["sk"])
        self.bos_client = self.create_bos_client()
        self.bcc_client = self.create_bce_client()

    def load_config(self, config_path):
        with open(config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def create_bce_client(self):
        bce_config = BceClientConfiguration(
            self.credentials, endpoint=self.bce_config["host"])
        return InnerBccClient(bce_config)

    def create_bos_client(self):
        bos_config = BceClientConfiguration(
            self.credentials, endpoint=self.bce_config["bos_host"]
        )
        return BosClient(bos_config)

    def create_tar(self):
        local_dir = self.appbuilder_config["local_dir"]
        with tarfile.open(self.tar_file_name, "w") as tar:
            for filename in os.listdir(local_dir):
                file_path = os.path.join(local_dir, filename)
                if os.path.isfile(file_path):
                    tar.add(file_path, arcname=filename)

    def bos_upload(self):
        bucket_name = "appbuilder-sdk-test"

        if not self.bos_client.does_bucket_exist(bucket_name):
            self.bos_client.create_bucket(bucket_name)

        self.bos_client.put_object_from_file(
            bucket_name, "demo.tar", self.tar_file_name)
        timestamp = int(time.time())
        url = self.bos_client.generate_pre_signed_url(
            bucket_name, "demo.tar", timestamp, expiration_in_seconds=3600
        )
        return url.decode("utf-8")

    def build_user_data(self):
        run_script = self.appbuilder_config["run_script"]
        user_data = "#!/bin/bash\\n" + \
            "mkdir /root/test\\n" + \
            "cd /root/test\\n" + \
            f"wget -O demo.tar {self.tar_bos_url}\\n"  + \
            "tar -xvf demo.tar\\n" + \
            "rm demo.tar\\n" + \
            f"chmod a+x {run_script}\\n" + \
            "yum install -y docker\\n" + \
            "docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.8.0\\n" + \
            f"docker run -itd --net=host -v /root/test:/home/test/ --name appbuilder-sdk registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.8.0 /home/test/{run_script}"

        return user_data

    def build_run_script(self):
        commands = []
        for key, value in self.env.items():
            commands.append(f'export {key}="{value}"')
        run_cmd = " && ".join(commands) + " && " + self.appbuilder_config["run_cmd"]
        run_script = self.appbuilder_config["local_dir"] + "/" + self.appbuilder_config["run_script"]
        with open(run_script, 'w') as file:
            file.write('#!/bin/sh\n')
            file.write(run_cmd)

    def create_instance(self):
        now_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        instance = self.bcc_client.create_instance_by_spec(
            spec=self.bce_config["spec"],  # 实例规格
            image_id="m-43wfwG1G",  # 镜像ID
            # 待创建虚拟机实例的系统盘大小，单位GB，默认是40GB，范围为[40,
            # 2048]GB，超过40GB按照云磁盘价格收费。注意指定的系统盘大小需要满足所使用镜像最小磁盘空间限制。
            root_disk_size_in_gb=self.bce_config["root_disk_size_in_gb"],
            network_capacity_in_mbps=1,
            name="instance-appbuilder-sdk-service-{}".format(now_str),
            hostname="host-appbuilder-sdk-service-{}".format(now_str),
            admin_pass=self.bce_config["admin_pass"],
            zone_name="cn-bj-d",
            user_data=self.build_user_data(),
        )
        self.get_instance_id(instance)

    def get_instance_id(self, instance):
        self.instance_id = instance.instance_ids[0]

    def get_public_ip(self, instance_id=None):
        response = None
        if instance_id != None:
            response = self.bcc_client.get_instance(instance_id)
        else:
            response = self.bcc_client.get_instance(self.instance_id)
        self.public_ip = response.instance.public_ip

    def create_security_group(self):
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
        )
        security_group_rule_list = []
        security_group_rule_list.append(security_group_rule)

        self.bcc_client.create_security_group(
            name=security_group_name,
            rules=security_group_rule_list,
            client_token=client_token,
        )

    def clear_local(self):
        os.remove(self.tar_file_name)

    def deploy(self):
        self.build_run_script()
        self.create_tar()
        self.tar_bos_url = self.bos_upload()
        self.clear_local()
        self.create_instance()
        print("instance create successfully! id: {}".format(self.instance_id))
        while self.public_ip is None:
            self.get_public_ip("i-HJOiG7E0")
            if self.public_ip is not None:
                print("public ip create successfully! ip: {}".format(self.public_ip))

if __name__ == "__main__":
    instance = AppbuilderSDKInstance("./config.yaml")
    instance.deploy()
