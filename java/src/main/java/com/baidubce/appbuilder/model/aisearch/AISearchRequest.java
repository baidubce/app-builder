package com.baidubce.appbuilder.model.aisearch;

import com.google.gson.annotations.SerializedName;

public class AISearchRequest {
    // region 主字段
    @SerializedName("messages")
    private Message[] messages;
    @SerializedName("search_source")
    private String searchSource = "baidu_search_v1";
    @SerializedName("resource_type_filter")
    private SearchResource[] resourceTypeFilter;
    @SerializedName("search_filter")
    private SearchFilter searchFilter;
    @SerializedName("search_recency_filter")
    private String searchRecencyFilter;
    @SerializedName("search_domain_filter")
    private String[] searchDomainFilter;
    @SerializedName("model")
    private String model;
    @SerializedName("instruction")
    private String instruction = "";
    @SerializedName("temperature")
    private Double temperature = 1e-10;
    @SerializedName("top_p")
    private Double topP = 1e-10;
    @SerializedName("prompt_template")
    private String promptTemplate;
    @SerializedName("search_mode")
    private String searchMode = "auto";
    @SerializedName("enable_reasoning")
    private Boolean enableReasoning = true;
    @SerializedName("enable_deep_search")
    private Boolean enableDeepSearch = false;
    @SerializedName("additional_knowledge")
    private Knowledge[] additionalKnowledge;
    @SerializedName("max_completion_tokens")
    private Integer maxCompletionTokens = 2048;
    @SerializedName("response_format")
    private String responseFormat = "auto";
    @SerializedName("enable_corner_markers")
    private Boolean enableCornerMarkers = true;
    @SerializedName("enable_followup_queries")
    private Boolean enableFollowupQueries = false;
    @SerializedName("stream")
    private Boolean stream = false;
    @SerializedName("safety_level")
    private String safetyLevel;
    @SerializedName("max_refer_search_items")
    private Integer maxReferSearchItems = 100;
    @SerializedName("config_id")
    private String configId = "";
    @SerializedName("model_appid")
    private String modelAppid = "";

    public static class Message {
        @SerializedName("role")
        private String role;

        @SerializedName("content")
        private Object content; // String or List<MessageContent>

        public Message(String role, Object content) {
            this.role = role;
            this.content = content;
        }
        
        public void setRole(String role) {
            this.role = role;
        }

        public void setContent(Object content) {
            this.content = content;
        }

        public String getRole() {
            return role;
        }

        public Object getContent() {
            return content;
        }
    }

    public static class SearchResource {
        @SerializedName("top_k")
        private int topK;

        @SerializedName("type")
        private String type;

        public SearchResource(int topK, String type) {
            this.topK = topK;
            this.type = type;
        }

        public int getTopK() {
            return topK;
        }

        public String getType() {
            return type;
        }

        public void setTopK(int topK) {
            this.topK = topK;
        }

        public void setType(String type) {
            this.type = type;
        }
    }

    public static class SearchFilter {
        @SerializedName("range")
        private Range range;

        @SerializedName("match")
        private Match match;

        public SearchFilter(Range range, Match match) {
            this.range = range;
            this.match = match;
        }

        public Range getRange() {
            return range;
        }

        public Match getMatch() {
            return match;
        }

        public void setRange(Range range) {
            this.range = range;
        }

        public void setMatch(Match match) {
            this.match = match;
        }
    }

    public static class Range {
        @SerializedName("page_time")
        private PageTime pageTime;
        
        public Range(PageTime pageTime) {
            this.pageTime = pageTime;
        }

        public PageTime getPageTime() {
            return pageTime;
        }

        public void setPageTime(PageTime pageTime) {
            this.pageTime = pageTime;
        }
    }

    public static class PageTime {
        @SerializedName("gth")
        private String gth = "";
        @SerializedName("gt")
        private String gt = "";
        @SerializedName("lth")
        private String lth = "";
        @SerializedName("lt")
        private String lt = "";

        public PageTime(String gth, String gt, String lth, String lt) {
            this.gth = gth;
            this.gt = gt;
            this.lth = lth;
            this.lt = lt;
        }


        public String getGth() {
            return gth;
        }

        public String getGt() {
            return gt;
        }

        public String getLth() {
            return lth;
        }

        public String getLt() {
            return lt;
        }

        public void setGth(String gth) {
            this.gth = gth;
        }

        public void setGt(String gt) {
            this.gt = gt;
        }

        public void setLth(String lth) {
            this.lth = lth;
        }

        public void setLt(String lt) {
            this.lt = lt;
        }
    }

    public static class Match {
        @SerializedName("site")
        private String[] site;

        public Match(String[] site) {
            this.site = site;
        }

        public String[] getSite() {
            return site;
        }

        public void setSite(String[] site) {
            this.site = site;
        }
    }

    public static class Knowledge {
        @SerializedName("priority")
        private Integer priority = 0;

        @SerializedName("data_type")
        private String dataType;

        @SerializedName("data")
        private KnowledgeData data;

        public Knowledge(Integer priority, String dataType, KnowledgeData data) {
            this.priority = priority;
            this.dataType = dataType;
            this.data = data;
        }

        public Integer getPriority() {
            return priority;
        }

        public String getDataType() {
            return dataType;
        }

        public KnowledgeData getData() {
            return data;
        }

        public void setPriority(Integer priority) {
            this.priority = priority;
        }

        public void setDataType(String dataType) {
            this.dataType = dataType;
        }

        public void setData(KnowledgeData data) {
            this.data = data;
        }
    }

    public static class KnowledgeData {
        @SerializedName("content")
        private String content;

        @SerializedName("title")
        private String title;

        @SerializedName("url")
        private String url;

        @SerializedName("release_date")
        private String releaseDate;

        public KnowledgeData(String content, String title, String url, String releaseDate) {
            this.content = content;
            this.title = title;
            this.url = url;
            this.releaseDate = releaseDate;
        }

        public String getContent() {
            return content;
        }

        public String getTitle() {
            return title;
        }

        public String getUrl() {
            return url;
        }

        public String getReleaseDate() {
            return releaseDate;
        }

        public void setContent(String content) {
            this.content = content;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public void setUrl(String url) {
            this.url = url;
        }

        public void setReleaseDate(String releaseDate) {
            this.releaseDate = releaseDate;
        }
    }


    public Message[] getMessages() {
        return messages;
    }

    public AISearchRequest setMessages(Message[] messages) {
        this.messages = messages;
        return this;
    }

    public String getSearchSource() {
        return searchSource;
    }

    public AISearchRequest setSearchSource(String searchSource) {
        this.searchSource = searchSource;
        return this;
    }

    public SearchResource[] getResourceTypeFilter() {
        return resourceTypeFilter;
    }

    public AISearchRequest setResourceTypeFilter(SearchResource[] resourceTypeFilter) {
        this.resourceTypeFilter = resourceTypeFilter;
        return this;
    }

    public SearchFilter getSearchFilter() {
        return searchFilter;
    }

    public AISearchRequest setSearchFilter(SearchFilter searchFilter) {
        this.searchFilter = searchFilter;
        return this;
    }

    public String getSearchRecencyFilter() {
        return searchRecencyFilter;
    }

    public AISearchRequest setSearchRecencyFilter(String searchRecencyFilter) {
        this.searchRecencyFilter = searchRecencyFilter;
        return this;
    }

    public String[] getSearchDomainFilter() {
        return searchDomainFilter;
    }

    public AISearchRequest setSearchDomainFilter(String[] searchDomainFilter) {
        this.searchDomainFilter = searchDomainFilter;
        return this;
    }

    public String getModel() {
        return model;
    }

    public AISearchRequest setModel(String model) {
        this.model = model;
        return this;
    }

    public String getInstruction() {
        return instruction;
    }

    public AISearchRequest setInstruction(String instruction) {
        this.instruction = instruction;
        return this;
    }

    public Double getTemperature() {
        return temperature;
    }

    public AISearchRequest setTemperature(Double temperature) {
        this.temperature = temperature;
        return this;
    }

    public Double getTopP() {
        return topP;
    }

    public AISearchRequest setTopP(Double topP) {
        this.topP = topP;
        return this;
    }

    public String getPromptTemplate() {
        return promptTemplate;
    }

    public AISearchRequest setPromptTemplate(String promptTemplate) {
        this.promptTemplate = promptTemplate;
        return this;
    }

    public String getSearchMode() {
        return searchMode;
    }

    public AISearchRequest setSearchMode(String searchMode) {
        this.searchMode = searchMode;
        return this;
    }

    public Boolean getEnableReasoning() {
        return enableReasoning;
    }

    public AISearchRequest setEnableReasoning(Boolean enableReasoning) {
        this.enableReasoning = enableReasoning;
        return this;
    }

    public Boolean getEnableDeepSearch() {
        return enableDeepSearch;
    }

    public AISearchRequest setEnableDeepSearch(Boolean enableDeepSearch) {
        this.enableDeepSearch = enableDeepSearch;
        return this;
    }

    public Knowledge[] getAdditionalKnowledge() {
        return additionalKnowledge;
    }

    public AISearchRequest setAdditionalKnowledge(Knowledge[] additionalKnowledge) {
        this.additionalKnowledge = additionalKnowledge;
        return this;
    }

    public Integer getMaxCompletionTokens() {
        return maxCompletionTokens;
    }

    public AISearchRequest setMaxCompletionTokens(Integer maxCompletionTokens) {
        this.maxCompletionTokens = maxCompletionTokens;
        return this;
    }

    public String getResponseFormat() {
        return responseFormat;
    }

    public AISearchRequest setResponseFormat(String responseFormat) {
        this.responseFormat = responseFormat;
        return this;
    }

    public Boolean getEnableCornerMarkers() {
        return enableCornerMarkers;
    }

    public AISearchRequest setEnableCornerMarkers(Boolean enableCornerMarkers) {
        this.enableCornerMarkers = enableCornerMarkers;
        return this;
    }

    public Boolean getEnableFollowupQueries() {
        return enableFollowupQueries;
    }

    public AISearchRequest setEnableFollowupQueries(Boolean enableFollowupQueries) {
        this.enableFollowupQueries = enableFollowupQueries;
        return this;
    }

    public Boolean getStream() {
        return stream;
    }

    public AISearchRequest setStream(Boolean stream) {
        this.stream = stream;
        return this;
    }

    public String getSafetyLevel() {
        return safetyLevel;
    }

    public AISearchRequest setSafetyLevel(String safetyLevel) {
        this.safetyLevel = safetyLevel;
        return this;
    }

    public Integer getMaxReferSearchItems() {
        return maxReferSearchItems;
    }

    public AISearchRequest setMaxReferSearchItems(Integer maxReferSearchItems) {
        this.maxReferSearchItems = maxReferSearchItems;
        return this;
    }

    public String getConfigId() {
        return configId;
    }

    public AISearchRequest setConfigId(String configId) {
        this.configId = configId;
        return this;
    }

    public String getModelAppid() {
        return modelAppid;
    }

    public AISearchRequest setModelAppid(String modelAppid) {
        this.modelAppid = modelAppid;
        return this;
    }
}