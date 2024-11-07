package com.baidubce.appbuilder.base.utils.json;

import com.google.gson.reflect.TypeToken;
import org.junit.Test;
import static org.junit.Assert.assertEquals;
import java.util.Map;

public class JsonUtilsTest {

    @Test
    public void testSerialize() {
        // 准备测试数据
        TestObject testObject = new TestObject("example", 123);
        
        // 进行序列化
        String json = JsonUtils.serialize(testObject);
        
        // 期望的JSON字符串
        String expectedJson = "{\"name\":\"example\",\"value\":123}";
        
        // 验证结果
        assertEquals(expectedJson, json);
    }

    @Test
    public void testDeserialize() {
        // 准备JSON字符串
        String json = "{\"name\":\"example\",\"value\":123}";
        
        // 进行反序列化
        TestObject testObject = JsonUtils.deserialize(json, TestObject.class);
        
        // 验证结果
        assertEquals("example", testObject.getName());
        assertEquals(123, testObject.getValue());
    }

    @Test
    public void testDeserializeToMap() {
        // 准备JSON字符串
        String json = "{\"key1\":\"value1\",\"key2\":\"value2\"}";
        
        // 进行反序列化到Map
        Map<String, String> map = JsonUtils.deserialize(json, new TypeToken<Map<String, String>>(){}.getType());
        
        // 验证结果
        assertEquals("value1", map.get("key1"));
        assertEquals("value2", map.get("key2"));
    }

    // 内部类用于测试对象
    static class TestObject {
        private String name;
        private int value;

        public TestObject(String name, int value) {
            this.name = name;
            this.value = value;
        }

        public String getName() {
            return name;
        }

        public int getValue() {
            return value;
        }
    }
}