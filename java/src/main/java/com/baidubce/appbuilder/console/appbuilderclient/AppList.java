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
     * 获取应用列表
     *
     * @param request 请求参数
     * @return 返回会话ID
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
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
