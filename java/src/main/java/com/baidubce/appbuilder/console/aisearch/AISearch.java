package com.baidubce.appbuilder.console.aisearch;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.aisearch.*;

public class AISearch extends Component {
    public AISearch() {
        super();
    }

    public AISearch(String secretKey) {
        super(secretKey);
    }

    public AISearch(String secretKey, String gateway) {
        super(secretKey, gateway);
    }


    public AISearchIterator run(AISearchRequest request)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.AI_SEARCH_URL;

        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<StreamIterator<AISearchResponse>> response =
                httpClient.executeSSE(postRequest, AISearchResponse.class);
        return new AISearchIterator(response.getBody());
    }
}
