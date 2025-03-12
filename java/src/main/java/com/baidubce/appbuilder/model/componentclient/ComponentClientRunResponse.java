package com.baidubce.appbuilder.model.componentclient;

import java.util.Map;

import com.google.gson.annotations.SerializedName;

import java.util.HashMap;

public class ComponentClientRunResponse {
    @SerializedName("request_id")
    private String requestID;
    private String code;
    private String message;
    @SerializedName("conversation_id")
    private String conversationID;
    @SerializedName("message_id")
    private String messageID;
    @SerializedName("trace_id")
    private String traceID;
    @SerializedName("user_id")
    private String userID;
    @SerializedName("end_user_id")
    private String endUserID;
    private String status; // 新增的字段
    private String role;
    private Content[] content;

    // Getters and Setters
    public String getRequestID() {
        return requestID;
    }

    public void setRequestID(String requestID) {
        this.requestID = requestID;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getConversationID() {
        return conversationID;
    }

    public void setConversationID(String conversationID) {
        this.conversationID = conversationID;
    }

    public String getMessageID() {
        return messageID;
    }

    public void setMessageID(String messageID) {
        this.messageID = messageID;
    }

    public String getTraceID() {
        return traceID;
    }

    public void setTraceID(String traceID) {
        this.traceID = traceID;
    }

    public String getUserID() {
        return userID;
    }

    public void setUserID(String userID) {
        this.userID = userID;
    }

    public String getEndUserID() {
        return endUserID;
    }

    public void setEndUserID(String endUserID) {
        this.endUserID = endUserID;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Content[] getContent() {
        return content;
    }

    public void setContent(Content[] content) {
        this.content = content;
    }

    public static class Content {
        private String name;
        @SerializedName("visible_scope")
        private String visibleScope;
        @SerializedName("raw_data")
        private Map<String, Object> rawData = new HashMap<>();
        private Map<String, Object> usage = new HashMap<>();
        private Map<String, Object> metrics = new HashMap<>();
        private String type;
        private Map<String, Object> text = new HashMap<>();
        private ComponentEvent event;

        // Getters and Setters
        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getVisibleScope() {
            return visibleScope;
        }

        public void setVisibleScope(String visibleScope) {
            this.visibleScope = visibleScope;
        }

        public Map<String, Object> getRawData() {
            return rawData;
        }

        public void setRawData(Map<String, Object> rawData) {
            this.rawData = rawData;
        }

        public Map<String, Object> getUsage() {
            return usage;
        }

        public void setUsage(Map<String, Object> usage) {
            this.usage = usage;
        }

        public Map<String, Object> getMetrics() {
            return metrics;
        }

        public void setMetrics(Map<String, Object> metrics) {
            this.metrics = metrics;
        }

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }

        public Map<String, Object> getText() {
            return text;
        }

        public void setText(Map<String, Object> text) {
            this.text = text;
        }

        public ComponentEvent getEvent() {
            return event;
        }

        public void setEvent(ComponentEvent event) {
            this.event = event;
        }

        public static class ComponentEvent {
            private String id;
            private String status;
            private String name;
            @SerializedName("created_time")
            private String createdTime;
            @SerializedName("error_code")
            private String errorCode;
            @SerializedName("error_message")
            private String errorMessage;

            // Getters and Setters
            public String getId() {
                return id;
            }

            public void setId(String id) {
                this.id = id;
            }

            public String getStatus() {
                return status;
            }

            public void setStatus(String status) {
                this.status = status;
            }

            public String getName() {
                return name;
            }

            public void setName(String name) {
                this.name = name;
            }

            public String getCreatedTime() {
                return createdTime;
            }

            public void setCreatedTime(String createdTime) {
                this.createdTime = createdTime;
            }

            public String getErrorCode() {
                return errorCode;
            }

            public void setErrorCode(String errorCode) {
                this.errorCode = errorCode;
            }

            public String getErrorMessage() {
                return errorMessage;
            }

            public void setErrorMessage(String errorMessage) {
                this.errorMessage = errorMessage;
            }
        }
    }
}
