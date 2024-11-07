import unittest
import os
import appbuilder


class ErrorComponent(appbuilder.Playground):

    def completion(
        self,
        version,
        base_url,
        request,
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ):
        r"""Send a byte array of an audio file to obtain the result of speech recognition."""

        headers = self.http_client.auth_header(request_id)
        headers["Content-Type"] = "application/json"

        completion_url = "/" + self.version + "/api/llm/" + self.name

        stream = True if request.response_mode == "streaming" else False
        url = self.http_client.service_url(completion_url, self.base_url)
        request.params["model_config"]["model"]["name"] = "<sdk-unittest>"
        request.params["model_config"]["model"]["url"] = "<sdk-unittest>"
        response = self.http_client.session.post(url, json=request.params, headers=headers, timeout=timeout,
                                                 stream=stream)
        return self.gene_response(response, stream) 


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestLlmBase(unittest.TestCase):

    def test_err_request(self):
        """ 测试在消息有效时运行 """
        cmpt = ErrorComponent(prompt_template="{query}", model="ERNIE-3.5-8K")
        msg = appbuilder.Message({
            "query": "小明",
        })

        answer = cmpt.run(message=msg, stream=True, temperature=1)
        with self.assertRaises(Exception):
            for x in answer.content:
                pass


if __name__ == '__main__':
    unittest.main()
