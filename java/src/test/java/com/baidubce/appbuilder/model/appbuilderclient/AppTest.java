package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class AppTest {

    private App app;

    @Before
    public void setUp() {
        app = new App();
    }

    @Test
    public void testSetGetId() {
        app.setId("app123");
        assertEquals("app123", app.getId());
    }

    @Test
    public void testSetGetName() {
        app.setName("Test App");
        assertEquals("Test App", app.getName());
    }

    @Test
    public void testSetGetDescription() {
        app.setDescription("This is a test app.");
        assertEquals("This is a test app.", app.getDescription());
    }
}