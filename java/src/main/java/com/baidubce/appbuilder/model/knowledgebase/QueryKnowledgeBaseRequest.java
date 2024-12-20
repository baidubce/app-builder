package com.baidubce.appbuilder.model.knowledgebase;

import java.util.List;

public class QueryKnowledgeBaseRequest {
    private String query;
    private String type;
    private Integer top;
    private Integer skip;
    private MetadataFilters metadata_filters;
    private QueryPipelineConfig pipeline_config;

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Integer getTop() {
        return top;
    }

    public void setTop(Integer top) {
        this.top = top;
    }

    public Integer getSkip() {
        return skip;
    }

    public void setSkip(Integer skip) {
        this.skip = skip;
    }

    public MetadataFilters getMetadata_filters() {
        return metadata_filters;
    }

    public void setMetadata_filters(MetadataFilters metadata_filters) {
        this.metadata_filters = metadata_filters;
    }

    public QueryPipelineConfig getPipeline_config() {
        return pipeline_config;
    }

    public void setPipeline_config(QueryPipelineConfig pipeline_config) {
        this.pipeline_config = pipeline_config;
    }

    public static class MetadataFilter {
        private String operator;
        private String field;
        private Object value;

        public String getOperator() {
            return operator;
        }

        public void setOperator(String operator) {
            this.operator = operator;
        }

        public String getField() {
            return field;
        }

        public void setField(String field) {
            this.field = field;
        }

        public Object getValue() {
            return value;
        }

        public void setValue(Object value) {
            this.value = value;
        }
    }

    public static class MetadataFilters {
        private List<MetadataFilter> filters;
        private String condition;

        public List<MetadataFilter> getFilters() {
            return filters;
        }

        public void setFilters(List<MetadataFilter> filters) {
            this.filters = filters;
        }

        public String getCondition() {
            return condition;
        }

        public void setCondition(String condition) {
            this.condition = condition;
        }
    }

    public static class PreRankingConfig {
        private Double bm25_weight;
        private Double vec_weight;
        private Double bm25_b;
        private Double bm25_k1;
        private Double bm25_max_score;

        public Double getBm25_weight() {
            return bm25_weight;
        }

        public void setBm25_weight(Double bm25_weight) {
            this.bm25_weight = bm25_weight;
        }

        public Double getVec_weight() {
            return vec_weight;
        }

        public void setVec_weight(Double vec_weight) {
            this.vec_weight = vec_weight;
        }

        public Double getBm25_b() {
            return bm25_b;
        }

        public void setBm25_b(Double bm25_b) {
            this.bm25_b = bm25_b;
        }

        public Double getBm25_k1() {
            return bm25_k1;
        }

        public void setBm25_k1(Double bm25_k1) {
            this.bm25_k1 = bm25_k1;
        }

        public Double getBm25_max_score() {
            return bm25_max_score;
        }

        public void setBm25_max_score(Double bm25_max_score) {
            this.bm25_max_score = bm25_max_score;
        }
    }

    public static class ElasticSearchRetrieveConfig {
        private String name;
        private String type;
        private Double threshold;
        private Integer top;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }

        public Double getThreshold() {
            return threshold;
        }

        public void setThreshold(Double threshold) {
            this.threshold = threshold;
        }

        public Integer getTop() {
            return top;
        }

        public void setTop(Integer top) {
            this.top = top;
        }
    }

    public static class RankingConfig {
        private String name;
        private String type;
        private List<String> inputs;
        private String model_name;
        private Integer top;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }

        public List<String> getInputs() {
            return inputs;
        }

        public void setInputs(List<String> inputs) {
            this.inputs = inputs;
        }

        public String getModel_name() {
            return model_name;
        }

        public void setModel_name(String model_name) {
            this.model_name = model_name;
        }

        public Integer getTop() {
            return top;
        }

        public void setTop(Integer top) {
            this.top = top;
        }
    }

    public static class QueryPipelineConfig {
        private String id;
        private List<Object> pipeline; 

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public List<Object> getPipeline() {
            return pipeline;
        }

        public void setPipeline(List<Object> pipeline) {
            this.pipeline = pipeline;
        }
    }
}
