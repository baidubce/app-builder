package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;

import java.util.Map;

import static org.junit.Assert.*;

public class AppListRequestTest {

    private AppListRequest appListRequest;

    @Before
    public void setUp() {
        appListRequest = new AppListRequest();
    }

    @Test
    public void testGetLimit() {
        appListRequest.setLimit(10);
        assertEquals(10, appListRequest.getLimit());
    }

    @Test
    public void testSetLimit() {
        appListRequest.setLimit(20);
        assertEquals(20, appListRequest.getLimit());
    }

    @Test
    public void testGetAfter() {
        appListRequest.setAfter("afterValue");
        assertEquals("afterValue", appListRequest.getAfter());
    }

    @Test
    public void testSetAfter() {
        appListRequest.setAfter("newAfterValue");
        assertEquals("newAfterValue", appListRequest.getAfter());
    }

    @Test
    public void testGetBefore() {
        appListRequest.setBefore("beforeValue");
        assertEquals("beforeValue", appListRequest.getBefore());
    }

    @Test
    public void testSetBefore() {
        appListRequest.setBefore("newBeforeValue");
        assertEquals("newBeforeValue", appListRequest.getBefore());
    }

    @Test
    public void testToMap_WithLimit() {
        appListRequest.setLimit(15);
        appListRequest.setAfter("afterExample");
        appListRequest.setBefore("beforeExample");

        Map<String, Object> resultMap = appListRequest.toMap();

        assertNotNull(resultMap);
        assertEquals(3, resultMap.size());
        assertEquals(15, resultMap.get("limit"));
        assertEquals("afterExample", resultMap.get("after"));
        assertEquals("beforeExample", resultMap.get("before"));
    }

    @Test
    public void testToMap_WithoutLimit() {
        appListRequest.setAfter("afterExample");
        appListRequest.setBefore("beforeExample");

        Map<String, Object> resultMap = appListRequest.toMap();

        assertNotNull(resultMap);
        assertEquals(2, resultMap.size());
        assertNull(resultMap.get("limit"));
        assertEquals("afterExample", resultMap.get("after"));
        assertEquals("beforeExample", resultMap.get("before"));
    }
}