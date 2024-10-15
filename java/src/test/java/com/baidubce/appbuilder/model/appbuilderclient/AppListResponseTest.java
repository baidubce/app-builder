package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class AppListResponseTest {

    private AppListResponse appListResponse;

    @Before
    public void setUp() {
        appListResponse = new AppListResponse();
    }

    @Test
    public void testGetSetRequestId() {
        appListResponse.setRequestId("req123");
        assertEquals("req123", appListResponse.getRequestId());
    }

    @Test
    public void testGetSetData() {
        App[] apps = new App[2];
        apps[0] = new App();  // Assuming App class has a default constructor
        apps[1] = new App();
        appListResponse.setData(apps);
        assertEquals(apps, appListResponse.getData());
    }

    @Test
    public void testGetSetCode() {
        appListResponse.setCode("200");
        assertEquals("200", appListResponse.getCode());
    }

    @Test
    public void testGetSetMessage() {
        appListResponse.setMessage("Success");
        assertEquals("Success", appListResponse.getMessage());
    }
}