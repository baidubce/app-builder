package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.assertEquals;

public class EventTest {

    private Event event;
    private Map<String, Object> detail;
    private Map<String, Object> usage;
    private ToolCall[] toolCalls;

    @Before
    public void setUp() {
        detail = new HashMap<>();
        detail.put("key1", "value1");

        usage = new HashMap<>();
        usage.put("usageKey", "usageValue");

        toolCalls = new ToolCall[2];
        toolCalls[0] = new ToolCall();  // 假设 ToolCall 类有默认构造函数
        toolCalls[1] = new ToolCall();

        event = new Event()
                .setCode("200")
                .setMessage("Success")
                .setEventType("eventType")
                .setStatus("completed")
                .setContentType("application/json")
                .setDetail(detail)
                .setUsage(usage)
                .setToolCalls(toolCalls);
    }

    @Test
    public void testGetCode() {
        assertEquals("200", event.getCode());
    }

    @Test
    public void testGetMessage() {
        assertEquals("Success", event.getMessage());
    }

    @Test
    public void testGetEventType() {
        assertEquals("eventType", event.getEventType());
    }

    @Test
    public void testGetStatus() {
        assertEquals("completed", event.getStatus());
    }

    @Test
    public void testGetContentType() {
        assertEquals("application/json", event.getContentType());
    }

    @Test
    public void testGetDetail() {
        assertEquals(detail, event.getDetail());
    }

    @Test
    public void testGetUsage() {
        assertEquals(usage, event.getUsage());
    }

    @Test
    public void testGetToolCalls() {
        assertEquals(toolCalls, event.getToolCalls());
    }

    @Test
    public void testToString() {
        String expected = "Event{" +
                "code='200'" +
                ", message='Success'" +
                ", eventType='eventType'" +
                ", status='completed'" +
                ", contentType='application/json'" +
                ", detail=" + detail + '\'' +
                ", usage=" + usage + '\'' +
                ", toolCalls=" + toolCalls + '}';
        assertEquals(expected, event.toString());
    }
}