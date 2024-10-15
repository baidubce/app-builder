package com.baidubce.appbuilder.model.rag;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class RAGResponseTest {

    private RAGResponse ragResponse;

    @Before
    public void setUp() {
        ragResponse = new RAGResponse();
    }

    @Test
    public void testSetGetCode() {
        ragResponse.setCode(200);
        assertEquals(200, ragResponse.getCode());
    }

    @Test
    public void testSetGetMessage() {
        ragResponse.setMessage("Success");
        assertEquals("Success", ragResponse.getMessage());
    }

    @Test
    public void testSetGetTraceId() {
        ragResponse.setTraceId("trace12345");
        assertEquals("trace12345", ragResponse.getTraceId());
    }

    @Test
    public void testSetGetTime() {
        ragResponse.setTime(123456789);
        assertEquals(123456789L, ragResponse.getTime());
    }

    @Test
    public void testSetGetResult() {
        RAGResult mockResult = new RAGResult(); // 假设有 RAGResult 类
        ragResponse.setResult(mockResult);
        assertEquals(mockResult, ragResponse.getResult());
    }

    @Test
    public void testToString() {
        ragResponse.setCode(200);
        ragResponse.setMessage("Success");
        ragResponse.setTraceId("trace12345");
        ragResponse.setTime(123456789);
        RAGResult mockResult = new RAGResult(); // 假设有 RAGResult 类
        ragResponse.setResult(mockResult);

        String expected = "RAGResponse{" +
                "code=200" +
                ", message='Success'" +
                ", traceId='trace12345'" +
                ", time=123456789" +
                ", result=" + mockResult +
                '}';

        assertEquals(expected, ragResponse.toString());
    }
}