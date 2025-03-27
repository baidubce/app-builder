# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time
import uuid
import os
import yaml
import tarfile
import argparse
from datetime import datetime

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient
from baidubce.services.bcc import bcc_model

from appbuilder.utils.logger_util import logger
from appbuilder.utils._bcc import InnerBccClient


class AppbuilderSDKInstance:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()

        self.credentials = BceCredentials(self.bce_config["ak"], self.bce_config["sk"])
        self.bos_client = self.create_bos_client()
        self.bcc_client = self.create_bce_client()

    def load_config(self):
        with open(self.config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.config = config

        self.bce_config = self.config["bce_config"]
        self.security_group_id = self.bce_config["security_group_id"]
        self.admin_pass = self.bce_config["admin_pass"]
        self.zone_name = self.bce_config["zone_name"]

        self.appbuilder_config = self.config["appbuilder_config"]
        self.env = self.config["env"]

    def save_config(self, config):
        self.config["bce_config"]["security_group_id"] = self.security_group_id
        with open(self.config_path, "w") as f:
            yaml.dump(config, f, indent=4)

    def create_bce_client(self):
        bce_config = BceClientConfiguration(
            self.credentials, endpoint=self.bce_config["host"]
        )
        return InnerBccClient(bce_config)

    def create_bos_client(self):
        bos_config = BceClientConfiguration(
            self.credentials, endpoint=self.bce_config["bos_host"]
        )
        return BosClient(bos_config)

    def create_tar(self):
        local_dir = self.appbuilder_config["local_dir"]
        timestamp = int(time.time())
        self.tar_file_name = "pkg_" + str(timestamp) + ".tar"
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
            bucket_name, self.tar_file_name, self.tar_file_name
        )
        timestamp = int(time.time())
        url = self.bos_client.generate_pre_signed_url(
            bucket_name, self.tar_file_name, timestamp, expiration_in_seconds=3600
        )
        self.tar_bos_url = url.decode("utf-8")
        if self.tar_bos_url == None:
            raise Exception("upload to bos failed")
        self.log.debug("upload to bos successfully! url: {}".format(self.tar_bos_url))

    def clear_local(self):
        os.remove(self.run_script)
        os.remove(self.tar_file_name)

    def build_user_data(self):
        workspace = self.appbuilder_config["workspace"]
        user_data = (
            "#!/bin/bash\\n"
            + "mkdir /root/test\\n"
            + "chmod 777 /root/test\\n"
            + "cd /root/test\\n"
            + f"wget -O {self.tar_file_name} {self.tar_bos_url}\\n"
            + f"tar -xvf {self.tar_file_name}\\n"
            + f"rm {self.tar_file_name}\\n"
            + f"chmod a+x {self.run_script_name}\\n"
            + "yum install -y docker\\n"
            + "docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-cloud:1.0.4\\n"
            + f"docker run -itd --net=host -v /root/test:{workspace} --name appbuilder-sdk registry.baidubce.com/appbuilder/appbuilder-sdk-cloud:1.0.4 {workspace}/{self.run_script_name}"
        )

        return user_data

    def build_run_script(self):
        timestamp = int(time.time())
        self.run_script_name = "start_" + str(timestamp) + ".sh"
        self.run_script = os.path.join(
            self.appbuilder_config["local_dir"], self.run_script_name
        )

        commands = []
        workspace = self.appbuilder_config["workspace"]
        for key, value in self.env.items():
            commands.append(f'export {key}="{value}"')
        run_cmd = " && ".join(commands) + " && " + self.appbuilder_config["run_cmd"]

        with open(self.run_script, "w") as file:
            file.write("#!/bin/sh\n")
            file.write(f"cd {workspace}\n")
            file.write(run_cmd)

    def create_instance(self):
        if self.security_group_id == None or self.security_group_id == "":
            self.create_security_group()
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
            admin_pass=self.admin_pass,
            zone_name=self.zone_name,
            user_data=self.build_user_data(),
        )
        self.log.debug("create instance info: {}".format(instance))
        self.get_instance_id(instance)
        if self.instance_id == None:
            raise Exception("create instance failed")
        self.log.info("instance create successfully! id: {}".format(self.instance_id))

    def get_instance_id(self, instance):
        self.instance_id = instance.instance_ids[0]

    def get_public_ip(self, instance_id=None):
        if instance_id == None and self.instance_id == None:
            return

        self.public_ip = None
        while self.public_ip is None or self.public_ip == "":
            time.sleep(3)
            response = None
            if instance_id != None:
                response = self.bcc_client.get_instance(instance_id)
            else:
                response = self.bcc_client.get_instance(self.instance_id)
            self.log.debug("get instance info: {}".format(response))
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

        response = self.bcc_client.create_security_group(
            name=security_group_name,
            rules=security_group_rule_list,
            client_token=client_token,
        )
        self.security_group_id = response.security_group_id
        if self.security_group_id == None:
            raise Exception("create security group failed")

        self.log.info(
            "security group create successfully！id: {}".format(self.security_group_id)
        )
        self.save_config(self.config)

    def bind_security_group(self):
        response = self.bcc_client.bind_instance_to_security_group(
            self.instance_id, self.security_group_id
        )
        self.log.debug("bind instance to security group: {}".format(response))

    def _pre_deploy(self):
        self.log = logger
        self.log.info(
            "The deployment to cloud feature is currently in the beta testing stage.If any issues arise, please submit an issue or contact us through our WeChat group."
        )
        self.build_run_script()
        self.log.debug("build run script done!")
        self.create_tar()
        self.log.debug("create tar done!")
        self.bos_upload()
        self.log.debug("upload tar to bos done!")
        self.clear_local()

    def _deploy(self):
        self.create_instance()

    def _after_deploy(self):
        self.get_public_ip()
        self.bind_security_group()
        self.log.info("deployment finished! public ip: {}".format(self.public_ip))

    def deploy(self):
        self._pre_deploy()
        self._deploy()
        self._after_deploy()


def deploy():
    parser = argparse.ArgumentParser(description="configuration")
    parser.add_argument("--conf", type=str, help="config yaml file")
    args = parser.parse_args()
    conf = args.conf
    instance = AppbuilderSDKInstance(conf)
    instance.deploy()


if __name__ == "__main__":
    deploy()
