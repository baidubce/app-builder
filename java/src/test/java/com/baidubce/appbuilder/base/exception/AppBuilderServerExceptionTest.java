package com.baidubce.appbuilder.base.exception;

import org.junit.Test;
import static org.junit.Assert.*;

public class AppBuilderServerExceptionTest {
    
    @Test
    public void testConstructorWithBasicFields() {
        AppBuilderServerException exception = new AppBuilderServerException("request123", 500, "Internal Server Error");

        assertEquals("request123", exception.getRequestId());
        assertEquals(500, exception.getCode());
        assertEquals("Internal Server Error", exception.getMessage());
        assertEquals(0, exception.getAppbuilderCode()); // default value
        assertNull(exception.getAppbuilderMessage());
        assertNull(exception.getResponseBody());
    }

    @Test
    public void testConstructorWithAppbuilderFields() {
        AppBuilderServerException exception = new AppBuilderServerException("request456", 400, "Bad Request", 1001, "Invalid parameter");

        assertEquals("request456", exception.getRequestId());
        assertEquals(400, exception.getCode());
        assertEquals("Bad Request", exception.getMessage());
        assertEquals(1001, exception.getAppbuilderCode());
        assertEquals("Invalid parameter", exception.getAppbuilderMessage());
        assertNull(exception.getResponseBody());
    }

    @Test
    public void testConstructorWithResponseBody() {
        AppBuilderServerException exception = new AppBuilderServerException("request789", 404, "Not Found", "Response body content");

        assertEquals("request789", exception.getRequestId());
        assertEquals(404, exception.getCode());
        assertEquals("Not Found", exception.getMessage());
        assertEquals("Response body content", exception.getResponseBody());
        assertEquals(0, exception.getAppbuilderCode()); // default value
        assertNull(exception.getAppbuilderMessage());
    }

    @Test
    public void testToString() {
        AppBuilderServerException exception = new AppBuilderServerException("request101", 401, "Unauthorized", 2002, "Access denied");
        exception.toString();
        
        String expectedString = "AppBuilderServerException{" +
                "requestId='request101'" +
                ", code=401" +
                ", message='Unauthorized'" +
                ", appbuilderCode=2002" +
                ", appbuilderMessage='Access denied'" +
                ", responseBody='null'" +
                '}';
        assertEquals(expectedString, exception.toString());
    }
}