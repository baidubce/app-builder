package com.baidubce.appbuilder.model.componentclient;

import java.util.HashMap;
import java.util.Map;

public class ComponentClientRunRequest {
    public static final String SysOriginQuery = "_sys_origin_query";
    public static final String SysFileUrls = "_sys_file_urls";
    public static final String SysConversationID = "_sys_conversation_id";
    public static final String SysEndUserID = "_sys_end_user_id";
    public static final String SysChatHistory = "_sys_chat_history";

    private boolean stream;
    private Map<String, Object> parameters = new HashMap<>();

    public boolean isStream() {
        return stream;
    }

    public void setStream(boolean stream) {
        this.stream = stream;
    }

    public Map<String, Object> getParameters() {
        return parameters;
    }

    public void setParameters(Map<String, Object> parameters) {
        this.parameters = parameters;
    }
}
