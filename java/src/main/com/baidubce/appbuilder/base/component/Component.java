package com.baidubce.appbuilder.base.component;

import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.utils.http.HttpClient;

public class Component {
    protected HttpClient httpClient;

    public Component() {
        //从环境变量获取
        initClient("", "");
    }

    public Component(String secretKey) {
        initClient(secretKey, "");
    }

    public Component(String secretKey, String gateway) {
        initClient(secretKey, gateway);
    }

    private void initClient(String secretKey, String gateway) {
        if (secretKey == null || secretKey.isEmpty()) {
            if ((secretKey = System.getProperty(AppBuilderConfig.APPBUILDER_TOKEN)) == null &&
                    (secretKey = System.getenv(AppBuilderConfig.APPBUILDER_TOKEN)) == null) {
                throw new RuntimeException("param secretKey is null and env APPBUILDER_TOKEN not set!");
            }
        }
        if (gateway == null || gateway.isEmpty()) {
            if ((gateway = System.getProperty(AppBuilderConfig.APPBUILDER_GATEWAY_URL)) == null &&
                    (gateway = System.getenv(AppBuilderConfig.APPBUILDER_GATEWAY_URL)) == null) {
                gateway = AppBuilderConfig.APPBUILDER_DEFAULT_GATEWAY;
            }
        }
        //通过secretKey获取
        if (!secretKey.startsWith("Bearer")) {
            secretKey = String.format("Bearer %s", secretKey);
        }
        this.httpClient = new HttpClient(secretKey, gateway);
    }

}
