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
        gateway = getEnvWithDefault(AppBuilderConfig.APPBUILDER_GATEWAY_URL, gateway, AppBuilderConfig.APPBUILDER_DEFAULT_GATEWAY);
        String gatewayV2 = getEnvWithDefault(AppBuilderConfig.APPBUILDER_GATEWAY_URL_V2, "",
                AppBuilderConfig.APPBUILDER_DEFAULT_GATEWAY_V2);
        
        secretKey = getEnvWithDefault(AppBuilderConfig.APPBUILDER_TOKEN, secretKey, "");
        if (secretKey.isEmpty()) {
            throw new RuntimeException("param secretKey is null and env APPBUILDER_TOKEN not set!");
        }
        String secretKeyPrefix = getEnvWithDefault(AppBuilderConfig.APPBUIDLER_SECRET_KEY_PREFIX, "", AppBuilderConfig.APPBUILDER_DEFAULT_SECRET_KEY_PREFIX);
        if (!secretKey.startsWith(secretKeyPrefix)) {
            secretKey = String.format("%s %s", secretKeyPrefix, secretKey);
        }
        this.httpClient = new HttpClient(secretKey, gateway, gatewayV2);
        this.httpClient.ConsoleOpenAPIPrefix = getEnvWithDefault(AppBuilderConfig.APPBUILDER_CONSOLE_OPENAPI_PREFIX, "",
                AppBuilderConfig.APPBUILDER_DEFAULT_CONSOLE_OPENAPI_PREFIX);
        this.httpClient.ConsoleOpenAPIVersion = getEnvWithDefault(AppBuilderConfig.APPBUILDER_CONSOLE_OPENAPI_VERSION, "",
                AppBuilderConfig.APPBUILDER_DEFAULT_CONSOLE_OPENAPI_VERSION);
    }


    private String getEnvWithDefault(String propertyKey, String currentValue, String defaultValue) {
        if (currentValue == null || currentValue.isEmpty()) {
            currentValue = System.getProperty(propertyKey);
            if (currentValue == null) {
                currentValue = System.getenv(propertyKey);
            }
            if (currentValue == null) {
                currentValue = defaultValue;
            }
        }
        return currentValue;
    }
}

