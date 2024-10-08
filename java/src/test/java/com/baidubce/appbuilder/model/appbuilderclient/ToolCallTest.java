package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class ToolCallTest {

    private ToolCall toolCall;

    @Before
    public void setUp() {
        toolCall = new ToolCall();
    }

    @Test
    public void testGetId() {
        toolCall.setId("testId");
        assertEquals("testId", toolCall.getId());
    }

    @Test
    public void testSetId() {
        toolCall.setId("newTestId");
        assertEquals("newTestId", toolCall.getId());
    }

    @Test
    public void testGetType() {
        toolCall.setType("testType");
        assertEquals("testType", toolCall.getType());
    }

    @Test
    public void testSetType() {
        toolCall.setType("newTestType");
        assertEquals("newTestType", toolCall.getType());
    }
}