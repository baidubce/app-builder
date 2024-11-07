package com.baidubce.appbuilder.model.agentbuilder;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class AgentBuilderResultTest {
    private AgentBuilderResult agentBuilderResult;
    private Event event1;
    private Event event2;

    @Before
    public void setUp() {
        agentBuilderResult = new AgentBuilderResult();

        // Initialize Event objects
        event1 = new Event().setCode("eventCode1").setMessage("First event");
        event2 = new Event().setCode("eventCode2").setMessage("Second event");

        agentBuilderResult.setAnswer("This is an answer")
                          .setEvents(new Event[]{event1, event2});
    }

    @Test
    public void testGetAnswer() {
        assertEquals("This is an answer", agentBuilderResult.getAnswer());
    }

    @Test
    public void testGetEvents() {
        Event[] events = agentBuilderResult.getEvents();
        assertNotNull(events);
        assertEquals(2, events.length);
        assertEquals("eventCode1", events[0].getCode());
        assertEquals("First event", events[0].getMessage());
        assertEquals("eventCode2", events[1].getCode());
        assertEquals("Second event", events[1].getMessage());
    }

    @Test
    public void testToString() {
        String expectedString = "AgentBuilderResult{" +
                "answer='This is an answer'" +
                ", events=[Event{code='eventCode1', message='First event', eventType='null', status='null', contentType='null', detail=null}, " +
                "Event{code='eventCode2', message='Second event', eventType='null', status='null', contentType='null', detail=null}]" +
                '}';
        assertEquals(expectedString, agentBuilderResult.toString());
    }
}