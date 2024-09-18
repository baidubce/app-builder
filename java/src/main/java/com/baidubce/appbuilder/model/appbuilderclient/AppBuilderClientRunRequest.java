package com.baidubce.appbuilder.model.appbuilderclient;

import java.util.Map;
import com.google.gson.annotations.SerializedName;

public class AppBuilderClientRunRequest {
    @SerializedName("app_id")
    private String appId;
    private String query;
    private boolean stream;
    @SerializedName("conversation_id")
    private String conversationID;
    @SerializedName("end_user_id")
    private String endUserId;
    private Tool[] tools;
    @SerializedName("tool_outputs")
    private ToolOutput[] ToolOutputs;
    @SerializedName("tool_choice")
    private ToolChoice ToolChoice;

    public String getAppId() {
        return appId;
    }

    public void setAppId(String appId) {
        this.appId = appId;
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public boolean isStream() {
        return stream;
    }

    public void setStream(boolean stream) {
        this.stream = stream;
    }

    public String getConversationID() {
        return conversationID;
    }

    public void setConversationID(String conversationID) {
        this.conversationID = conversationID;
    }

    public String getEndUserId() {
        return endUserId;
    }

    public void setEndUserId(String endUserId) {
        this.endUserId = endUserId;
    }

    public Tool[] getTools() {
        return tools;
    }

    public void setTools(Tool[] tools) {
        this.tools = tools;
    }

    public ToolOutput[] getToolOutputs() {
        return ToolOutputs;
    }

    public void setToolOutputs(ToolOutput[] toolOutputs) {
        this.ToolOutputs = toolOutputs;
    }

    public ToolChoice getToolChoice() {
        return ToolChoice;
    }

    public void setToolChoice(ToolChoice toolChoice) {
        this.ToolChoice = toolChoice;
    }

    public static class Tool {
        private String type;
        private Function function;

        public Tool(String type, Function function) {
            this.type = type;
            this.function = function;
        }

        public String getType() {
            return type;
        }

        public Function getFunction() {
            return function;
        }


        public static class Function {
            private String name;
            private String description;
            private Map<String, Object> parameters;

            public Function(String name, String description, Map<String, Object> parameters) {
                this.name = name;
                this.description = description;
                this.parameters = parameters;
            }

            public String getName() {
                return name;
            }

            public String getDescription() {
                return description;
            }

            public Map<String, Object> getParameters() {
                return parameters;
            }
        }
    }

    public static class ToolOutput {
        @SerializedName("tool_call_id")
        private String toolCallID;
        private String output;

        public ToolOutput(String toolCallID, String output) {
            this.toolCallID = toolCallID;
            this.output = output;
        }

        public String getToolCallID() {
            return toolCallID;
        }

        public String getOutput() {
            return output;
        }
    }

    public static class ToolChoice {
        private String type;
        private Function function;

        public ToolChoice(String type, Function function) { 
            this.type=type;
            this.function=function;
        }

        public String getType() {
            return type;
        }

        public Function getFunction() {
            return function;
        }

        public static class Function {
            private String name;
            private Map<String, Object> input;

            public Function(String name, Map<String, Object> input) {
                this.name = name;
                this.input = input;
            }

            public String getName() {
                return name;
            }

            public Map<String, Object> getInput() {
                return input;
            }
        }
    }
}
