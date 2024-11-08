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


from baidubce.services.bcc import bcc_client, bcc_model
from baidubce.utils import aes128_encrypt_16char_key
from baidubce.http import http_methods
import json
import uuid


class InnerBccClient(bcc_client.BccClient):
    def __init__(self, config=None):
        bcc_client.BccClient.__init__(self, config)

    def create_instance_by_spec(
        self,
        spec,
        image_id,
        root_disk_size_in_gb=0,
        root_disk_storage_type=None,
        ephemeral_disks=None,
        create_cds_list=None,
        network_capacity_in_mbps=0,
        eip_name=None,
        internet_charge_type=None,
        purchase_count=1,
        name=None,
        hostname=None,
        auto_seq_suffix=None,
        is_open_hostname_domain=None,
        admin_pass=None,
        billing=None,
        zone_name=None,
        subnet_id=None,
        security_group_id=None,
        enterprise_security_group_id=None,
        security_group_ids=None,
        enterprise_security_group_ids=None,
        relation_tag=None,
        is_open_ipv6=None,
        tags=None,
        key_pair_id=None,
        auto_renew_time_unit=None,
        auto_renew_time=0,
        cds_auto_renew=None,
        asp_id=None,
        bid_model=None,
        bid_price=None,
        dedicate_host_id=None,
        deploy_id=None,
        deploy_id_list=None,
        client_token=None,
        config=None,
        user_data=None,
    ):
        path = b"/instanceBySpec"
        params = {}
        if client_token is None:
            params["clientToken"] = str(uuid.uuid4())
        else:
            params["clientToken"] = client_token
        if billing is None:
            billing = bcc_model.Billing("Postpaid")
        body = {"spec": spec, "imageId": image_id, "billing": billing.__dict__}
        if root_disk_size_in_gb != 0:
            body["rootDiskSizeInGb"] = root_disk_size_in_gb
        if root_disk_storage_type is not None:
            body["rootDiskStorageType"] = root_disk_storage_type
        if create_cds_list is not None:
            body["createCdsList"] = [
                create_cds.__dict__ for create_cds in create_cds_list
            ]
        if network_capacity_in_mbps != 0:
            body["networkCapacityInMbps"] = network_capacity_in_mbps
        if eip_name is not None:
            body["eipName"] = eip_name
        if purchase_count > 0:
            body["purchaseCount"] = purchase_count
        if name is not None:
            body["name"] = name
        if hostname is not None:
            body["hostname"] = hostname
        if auto_seq_suffix is not None:
            body["autoSeqSuffix"] = auto_seq_suffix
        if is_open_hostname_domain is not None:
            body["isOpenHostnameDomain"] = is_open_hostname_domain
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(
                admin_pass, secret_access_key)
            body["adminPass"] = cipher_admin_pass
        if zone_name is not None:
            body["zoneName"] = zone_name
        if subnet_id is not None:
            body["subnetId"] = subnet_id
        if security_group_id is not None:
            body["securityGroupId"] = security_group_id
        if enterprise_security_group_id is not None:
            body["enterpriseSecurityGroupId"] = enterprise_security_group_id
        if security_group_ids is not None:
            body["securityGroupIds"] = security_group_ids
        if enterprise_security_group_ids is not None:
            body["enterpriseSecurityGroupIds"] = enterprise_security_group_ids
        if auto_renew_time != 0:
            body["autoRenewTime"] = auto_renew_time
        if auto_renew_time_unit is None:
            body["autoRenewTimeUnit"] = "month"
        else:
            body["autoRenewTimeUnit"] = auto_renew_time_unit
        if ephemeral_disks is not None:
            body["ephemeralDisks"] = [
                ephemeral_disk.__dict__ for ephemeral_disk in ephemeral_disks
            ]
        if dedicate_host_id is not None:
            body["dedicatedHostId"] = dedicate_host_id
        if deploy_id is not None:
            body["deployId"] = deploy_id
        if deploy_id_list is not None:
            body["deployIdList"] = deploy_id_list
        if bid_model is not None:
            body["bidModel"] = bid_model
        if bid_price is not None:
            body["bidPrice"] = bid_price
        if key_pair_id is not None:
            body["keypairId"] = key_pair_id
        if internet_charge_type is not None:
            body["internetChargeType"] = internet_charge_type
        if asp_id is not None:
            body["aspId"] = asp_id
        if relation_tag is not None:
            body["relationTag"] = relation_tag
        if is_open_ipv6 is not None:
            body["isOpenIpv6"] = is_open_ipv6
        if user_data is not None:
            body["userData"] = user_data
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body["tags"] = tag_list
        body["cdsAutoRenew"] = cds_auto_renew
        return self._send_request(
            http_methods.POST, path, json.dumps(body), params=params, config=config
        )

    def _compute_service_id(self):
        return "bcc"
