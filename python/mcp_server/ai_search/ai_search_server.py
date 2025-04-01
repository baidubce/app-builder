"""
Baidu AI Search MCP Server stdio server file.
We also support access via SSE protocol. The access address is:
http://appbuilder.baidu.com/v2/ai_search/mcp/sse?api_key=<your api_key>
You can refer to this webpage https://cloud.baidu.com/doc/AppBuilder/s/klv2eywua to obtain the api_key, in the format of "Bearer+bce…".
"""
import os
import json
from mcp.server import FastMCP
from appbuilder.core.components.rag_with_baidu_search_pro import RagWithBaiduSearchPro
from types import SimpleNamespace

# You can refer to this webpage https://cloud.baidu.com/doc/AppBuilder/s/klv2eywua to obtain the api_key
# format is "bce-v3/ALTAK-..."
# os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-..."
server = FastMCP(name="AB Component Server")

# You can switch to other models supported by AppBuilder
init_args = {
    "model": "Qianfan-Agent-Speed-8K",
}


@server.tool()
def AIsearch(
    query,
    stream=False,
    instruction=None,
    temperature=1e-10,
    top_p=1e-10,
    search_top_k=4,
    hide_corner_markers=True,
):
    """
    执行搜索。

    Args:
        query (str): 搜索请求。
        stream (bool, optional): 是否以流的形式接收响应数据。默认为False。
        instruction (Instruction, optional): 指令信息对象。默认为None。
        temperature (float, optional): 温度参数，控制生成文本的随机性。默认为1e-10。
        top_p (float, optional): 累积概率阈值，用于控制生成文本的多样性。默认为1e-10。
        search_top_k (int, optional): 搜索候选结果的数量。默认为4。
        hide_corner_markers (bool, optional): 是否隐藏响应中的边界标记。默认为True。

    Returns:
        Message: 处理后的信息对象。

    Raises:
        AppBuilderServerException: 如果输入信息或指令过长，将抛出此异常。
    """
    os.environ["APPBUILDER_SDK_MCP_CONTEXT"] = "server"
    message = SimpleNamespace(role="user", content="{}".format(query))
    search_instance = RagWithBaiduSearchPro(
        model=init_args["model"]
    )
    response = search_instance.run(
        message=message,
        stream=stream,
        instruction=instruction,
        model=init_args["model"],
        temperature=temperature,
        top_p=top_p,
        search_top_k=search_top_k,
        hide_corner_markers=hide_corner_markers,
    )
    return response.content + "\n\n" + json.dumps(response.extra, ensure_ascii=False)


if __name__ == "__main__":
    server.run()
