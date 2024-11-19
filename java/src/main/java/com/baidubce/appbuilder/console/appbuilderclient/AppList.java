package com.baidubce.appbuilder.console.appbuilderclient;


import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.appbuilderclient.App;
import com.baidubce.appbuilder.model.appbuilderclient.AppListResponse;
import com.baidubce.appbuilder.model.appbuilderclient.AppsDescribeRequest;
import com.baidubce.appbuilder.model.appbuilderclient.AppsDescribeResponse;
import com.baidubce.appbuilder.model.appbuilderclient.AppListRequest;

public class AppList extends Component {
    public AppList() {
        super();
    }

    /**
     * @deprecated 该方法已被弃用，建议使用新的API接口
     *
     * 根据提供的请求参数，获取应用列表
     *
     * @param request 请求参数对象，包含获取应用列表所需的参数
     * @return 返回应用列表数组
     * @throws IOException 如果发生IO异常，抛出此异常
     * @throws AppBuilderServerException 如果发生AppBuilder服务异常，抛出此异常
     */
    @Deprecated
    public App[] getAppList(AppListRequest request) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.APP_LIST_URL;

        ClassicHttpRequest getRequest = httpClient.createGetRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppListResponse> response = httpClient.execute(getRequest, AppListResponse.class);
        AppListResponse respBody = response.getBody();
        return respBody.getData();
    }
    
    /**
     * 描述应用接口
     *
     * @param request 描述应用请求对象
     * @return 描述应用响应对象
     * @throws IOException                  IO异常
     * @throws AppBuilderServerException 应用构建服务器异常
     */
    public AppsDescribeResponse describeApps(AppsDescribeRequest request) 
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.APPS_DESCRIBE_URL;

        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppsDescribeResponse> response = httpClient.execute(postRequest,
                AppsDescribeResponse.class);
        AppsDescribeResponse respBody = response.getBody();
        return respBody;
    }
}
