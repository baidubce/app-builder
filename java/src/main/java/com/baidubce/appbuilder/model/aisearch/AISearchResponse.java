package com.baidubce.appbuilder.model.aisearch;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class AISearchResponse {
    @SerializedName("request_id")
    private String requestId;

    @SerializedName("is_safe")
    private Boolean isSafe;

    private List<Choice> choices;

    private String code;

    private String message;

    private Usage usage;

    private List<Reference> references;

    @SerializedName("followup_queries")
    private List<String> followupQueries;

    public String getRequestId() {
        return requestId;
    }

    public AISearchResponse setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }

    public Boolean getIsSafe() {
        return isSafe;
    }

    public AISearchResponse setIsSafe(Boolean isSafe) {
        this.isSafe = isSafe;
        return this;
    }

    public List<Choice> getChoices() {
        return choices;
    }

    public AISearchResponse setChoices(List<Choice> choices) {
        this.choices = choices;
        return this;
    }

    public String getCode() {
        return code;
    }

    public AISearchResponse setCode(String code) {
        this.code = code;
        return this;
    }

    public String getMessage() {
        return message;
    }

    public AISearchResponse setMessage(String message) {
        this.message = message;
        return this;
    }

    public Usage getUsage() {
        return usage;
    }

    public AISearchResponse setUsage(Usage usage) {
        this.usage = usage;
        return this;
    }

    public List<Reference> getReferences() {
        return references;
    }

    public AISearchResponse setReferences(List<Reference> references) {
        this.references = references;
        return this;
    }

    public List<String> getFollowupQueries() {
        return followupQueries;
    }

    public AISearchResponse setFollowupQueries(List<String> followupQueries) {
        this.followupQueries = followupQueries;
        return this;
    }

    // region 内部类
    public static class Usage {
        @SerializedName("completion_tokens")
        private Integer completionTokens;

        @SerializedName("prompt_tokens")
        private Integer promptTokens;

        @SerializedName("total_tokens")
        private Integer totalTokens;
        // getters/setters
        public Integer getCompletionTokens() {
            return completionTokens;
        }

        public Usage setCompletionTokens(Integer completionTokens) {
            this.completionTokens = completionTokens;
            return this;
        }

        public Integer getPromptTokens() {
            return promptTokens;
        }

        public Usage setPromptTokens(Integer promptTokens) {
            this.promptTokens = promptTokens;
            return this;
        }

        public Integer getTotalTokens() {
            return totalTokens;
        }

        public Usage setTotalTokens(Integer totalTokens) {
            this.totalTokens = totalTokens;
            return this;
        }
    }

    public static class VideoDetail {
        private String url;
        private String height;
        private String width;
        private String size;
        private String duration;

        @SerializedName("hover_pic")
        private String hoverPic;
        // getters/setters
        public String getUrl() {
            return url;
        }

        public VideoDetail setUrl(String url) {
            this.url = url;
            return this;
        }

        public String getHeight() {
            return height;
        }

        public VideoDetail setHeight(String height) {
            this.height = height;
            return this;
        }

        public String getWidth() {
            return width;
        }

        public VideoDetail setWidth(String width) {
            this.width = width;
            return this;
        }

        public String getSize() {
            return size;
        }

        public VideoDetail setSize(String size) {
            this.size = size;
            return this;
        }

        public String getDuration() {
            return duration;
        }

        public VideoDetail setDuration(String duration) {
            this.duration = duration;
            return this;
        }

        @SerializedName("hover_pic")
        public String getHoverPic() {
            return hoverPic;
        }

        public VideoDetail setHoverPic(String hoverPic) {
            this.hoverPic = hoverPic;
            return this;
        }
    }

    public static class ImageDetail {
        private String url;
        private String height;
        private String width;
        // getters/setters
        public String getUrl() {
            return url;
        }

        public ImageDetail setUrl(String url) {
            this.url = url;
            return this;
        }

        public String getHeight() {
            return height;
        }

        public ImageDetail setHeight(String height) {
            this.height = height;
            return this;
        }

        public String getWidth() {
            return width;
        }

        public ImageDetail setWidth(String width) {
            this.width = width;
            return this;
        }
    }

    public static class Reference {
        private Integer id;

        private String title;

        private String url;

        @SerializedName("web_anchor")
        private String webAnchor;
        private String icon;
        private String content;
        private String date;
        private String type;
        private ImageDetail image;
        private VideoDetail video;
        // getters/setters

        public Integer getId() {
            return id;
        }

        public Reference setId(Integer id) {
            this.id = id;
            return this;
        }

        public String getTitle() {
            return title;
        }

        public Reference setTitle(String title) {
            this.title = title;
            return this;
        }

        public String getUrl() {
            return url;
        }

        public Reference setUrl(String url) {
            this.url = url;
            return this;
        }

        public String getWebAnchor() {
            return webAnchor;
        }

        public Reference setWebAnchor(String webAnchor) {
            this.webAnchor = webAnchor;
            return this;
        }

        public String getIcon() {
            return icon;
        }

        public Reference setIcon(String icon) {
            this.icon = icon;
            return this;
        }

        public String getContent() {
            return content;
        }

        public Reference setContent(String content) {
            this.content = content;
            return this;
        }

        public String getDate() {
            return date;
        }

        public Reference setDate(String date) {
            this.date = date;
            return this;
        }

        public String getType() {
            return type;
        }

        public Reference setType(String type) {
            this.type = type;
            return this;
        }

        public ImageDetail getImage() {
            return image;
        }

        public Reference setImage(ImageDetail image) {
            this.image = image;
            return this;
        }

        public VideoDetail getVideo() {
            return video;
        }

        public Reference setVideo(VideoDetail video) {
            this.video = video;
            return this;
        }
    }

    public static class Delta {
        private String content;

        private String role;

        @SerializedName("reasoning_content")
        private String reasoningContent;
        // getters/setters

        public Delta setContent(String content) {
            this.content = content;
            return this;
        }

        public String getContent() {
            return content;
        }

        public String getRole() {
            return role;
        }

        public Delta setRole(String role) {
            this.role = role;
            return this;
        }

        public String getReasoningContent() {
            return reasoningContent;
        }

        public Delta setReasoningContent(String reasoningContent) {
            this.reasoningContent = reasoningContent;
            return this;
        }
    }

    public static class ChoiceMessage {
        private String content;

        private String role;

        @SerializedName("reasoning_content")
        private String reasoningContent;

        public String getContent() {
            return content;
        }

        public ChoiceMessage setContent(String content) {
            this.content = content;
            return this;
        }

        public String getRole() {
            return role;
        }

        public ChoiceMessage setRole(String role) {
            this.role = role;
            return this;
        }

        public String getReasoningContent() {
            return reasoningContent;
        }

        public ChoiceMessage setReasoningContent(String reasoningContent) {
            this.reasoningContent = reasoningContent;
            return this;
        }
    }

    public static class Choice {
        private int index;

        @SerializedName("finish_reason")
        private String finishReason;

        private ChoiceMessage message;
        private Delta delta;
        
        public int getIndex() {
            return index;
        }

        public Choice setIndex(int index) {
            this.index = index;
            return this;
        }

        public String getFinishReason() {
            return finishReason;
        }

        public Choice setFinishReason(String finishReason) {
            this.finishReason = finishReason;
            return this;
        }

        public ChoiceMessage getMessage() {
            return message;
        }

        public Choice setMessage(ChoiceMessage message) {
            this.message = message;
            return this;
        }

        public Delta getDelta() {
            return delta;
        }

        public Choice setDelta(Delta delta) {
            this.delta = delta;
            return this;
        }
    }
}