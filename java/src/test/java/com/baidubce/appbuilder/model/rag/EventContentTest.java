package com.baidubce.appbuilder.model.rag;

import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class EventContentTest {

    private EventContent eventContent;

    @Before
    public void setUp() {
        eventContent = new EventContent();
    }

    @Test
    public void testGetSetEventCode() {
        eventContent.setEventCode("eventCode123");
        assertEquals("eventCode123", eventContent.getEventCode());
    }

    @Test
    public void testGetSetEnentMessage() {
        eventContent.setEnentMessage("message123");
        assertEquals("message123", eventContent.getEnentMessage());
    }

    @Test
    public void testGetSetNodeName() {
        eventContent.setNodeName("nodeName123");
        assertEquals("nodeName123", eventContent.getNodeName());
    }

    @Test
    public void testGetSetDependencyNodes() {
        String[] dependencyNodes = new String[]{"node1", "node2"};
        eventContent.setDependencyNodes(dependencyNodes);
        assertArrayEquals(dependencyNodes, eventContent.getDependencyNodes());
    }

    @Test
    public void testGetSetEventType() {
        eventContent.setEventType("eventType123");
        assertEquals("eventType123", eventContent.getEventType());
    }

    @Test
    public void testGetSetEventId() {
        eventContent.setEventId("eventId123");
        assertEquals("eventId123", eventContent.getEventId());
    }

    @Test
    public void testGetSetEventStatus() {
        eventContent.setEventStatus("eventStatus123");
        assertEquals("eventStatus123", eventContent.getEventStatus());
    }

    @Test
    public void testGetSetContentType() {
        eventContent.setContentType("contentType123");
        assertEquals("contentType123", eventContent.getContentType());
    }

    @Test
    public void testGetSetOutputs() {
        Map<String, Object> outputs = new HashMap<>();
        outputs.put("outputKey", "outputValue");
        eventContent.setOutputs(outputs);
        assertEquals(outputs, eventContent.getOutputs());
    }

    @Test
    public void testGetSetDetail() {
        HashMap<String, String> detail = new HashMap<>();
        detail.put("key1", "value1");
        eventContent.setDetail(detail);
        assertEquals(detail, eventContent.getDetail());
    }

    @Test
    public void testToString() {
        eventContent.setEventCode("eventCode123");
        eventContent.setEnentMessage("message123");
        eventContent.setNodeName("nodeName123");
        eventContent.setDependencyNodes(new String[]{"node1", "node2"});
        eventContent.setEventType("eventType123");
        eventContent.setEventId("eventId123");
        eventContent.setEventStatus("eventStatus123");
        eventContent.setContentType("contentType123");

        String expected = "EventContent{eventCode='eventCode123', enentMessage='message123', nodeName='nodeName123', dependencyNodes=[node1, node2], eventType='eventType123', eventId='eventId123', eventStatus='eventStatus123', contentType='contentType123', outputs=null, detail=null}";
        assertEquals(expected, eventContent.toString());
    }
}