package com.baidubce.appbuilder.model.agentbuilder;

import org.junit.Before;
import org.junit.Test;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class EventTest {
    private Event event;

    @Before
    public void setUp() {
        event = new Event();

        Map<String, Object> detail = new HashMap<>();
        detail.put("key1", "value1");
        detail.put("key2", 100);

        event.setCode("eventCode123")
             .setMessage("Event occurred")
             .setEventType("eventType")
             .setStatus("success")
             .setContentType("application/json")
             .setDetail(detail);
    }

    @Test
    public void testCode() {
        assertEquals("eventCode123", event.getCode());
    }

    @Test
    public void testMessage() {
        assertEquals("Event occurred", event.getMessage());
    }

    @Test
    public void testEventType() {
        assertEquals("eventType", event.getEventType());
    }

    @Test
    public void testStatus() {
        assertEquals("success", event.getStatus());
    }

    @Test
    public void testContentType() {
        assertEquals("application/json", event.getContentType());
    }

    @Test
    public void testDetail() {
        Map<String, Object> detail = event.getDetail();
        assertNotNull(detail);
        assertEquals(2, detail.size());
        assertEquals("value1", detail.get("key1"));
        assertEquals(100, detail.get("key2"));
    }

    @Test
    public void testToString() {
        String expectedString = "Event{" +
                "code='eventCode123'" +
                ", message='Event occurred'" +
                ", eventType='eventType'" +
                ", status='success'" +
                ", contentType='application/json'" +
                ", detail={key1=value1, key2=100}" +
                '}';
        assertEquals(expectedString, event.toString());
    }
}