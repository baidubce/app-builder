# 安装说明


# AgentBuilder组件
```java
import java.io.IOException;
import java.util.Iterator;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.agentbuilder.AgentBuilder;
import com.baidubce.appbuilder.model.agentbuilder.AgentBuilderResponse;

class AgentBuilderDemo {
    
    public static void main(String[] args) {
        //请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        System.setProperty("APPBUILDER_TOKEN", "bce-YOURTOKEN");
        String appId = "bce-YOURAPPID";

        AgentBuilder agentBuilder = new AgentBuilder(appId);
        String conversationId = agentBuilder.createConversation();
        System.out.println(conversationId);
        String fileId = agentBuilder.uploadLocalFile(conversationId, "java/src/test/com/baidubce/appbuilder/console/files/test.pdf");
        Iterator<AgentBuilderResponse> itor = agentBuilder.run("北京有多少小学生", conversationId, new String[]{fileId}, true);
        while(itor.hasNext())
        {
            AgentBuilderResponse response = itor.next();
            System.out.print(response.getAnswer());
        }
    }
}
```

# console端RAG操作工具(RAG)

```java
import java.io.IOException;
import java.util.Iterator;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.rag.RAG;
import com.baidubce.appbuilder.model.rag.RAGResponse;

public class RAGDemo {
    public static void main(String[] args) throws IOException, AppBuilderServerException {
        //请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        System.setProperty("APPBUILDER_TOKEN", "bce-YOURTOKEN");

        String appID = "bce-YOURAPPID";
        RAG rag = new RAG(appID);

        Iterator<RAGResponse> itor = rag.run("我想了解附近的房产价格，你能帮我查询吗？", "", true);
        System.out.println("输出结果：");
        while (itor.hasNext()) {
            RAGResponse response = itor.next();
            System.out.print(response.getResult().getAnswer());
        }
    }
}

```

# 知识库组件（Dataset）

```java
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.dataset.Dataset;
import com.baidubce.appbuilder.model.dataset.DocumentListData;
import com.baidubce.appbuilder.model.dataset.DocumentListResponse;

public class DatasetDemo {
    public static void main(String[] args) throws IOException, AppBuilderServerException {
        //请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        System.setProperty("APPBUILDER_TOKEN", "bce-YOURTOKEN");

        Dataset ds = new Dataset();
        // 创建数据集
        String datasetId = ds.createDataset("数据集名称");
        System.out.println("datasetId:  " + datasetId);

        // 上传文档
        String filePath = "java/src/test/com/baidubce/appbuilder/console/files/test.pdf";
        String[] documentIds = ds.addDocuments(new ArrayList<>(Collections.singletonList(filePath)), false, null, false);
        System.out.println("documentIds:  " + Arrays.toString(documentIds));

        // 获取文档列表
        DocumentListResponse resp = ds.getDocumentList(1, 20, "");

        System.out.println("document total num:  " + resp.getResult().getTotal());
        for (DocumentListData data : resp.getResult().getData()) {
            System.out.println("document name:  " + data.getName());
        }
        // 删除文档
        ds.deleteDocuments(documentIds);
    }
}
```