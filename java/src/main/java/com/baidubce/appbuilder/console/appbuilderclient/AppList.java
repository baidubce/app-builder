package com.baidubce.appbuilder.console.appbuilderclient;


import java.io.IOException;

import org.apache.hc.core5.http.ClassicHttpRequest;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.model.appbuilderclient.App;
import com.baidubce.appbuilder.model.appbuilderclient.AppsResponse;
import com.baidubce.appbuilder.model.appbuilderclient.GetAppsRequest;

public class AppList extends Component {
    public AppList() {
        super();
    }

    /**
     * 获取应用列表
     *
     * @return 返回会话ID
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public  App[] getApps(GetAppsRequest request) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.APP_LIST_URL;

        ClassicHttpRequest getRequest = httpClient.createGetRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppsResponse> response = httpClient.execute(getRequest, AppsResponse.class);
        AppsResponse respBody = response.getBody();
        return respBody.getData();
    }
}
