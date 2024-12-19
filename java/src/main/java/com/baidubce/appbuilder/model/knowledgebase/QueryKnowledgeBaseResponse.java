package com.baidubce.appbuilder.model.knowledgebase;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

public class QueryKnowledgeBaseResponse {
    private String requestId;
    private String code;
    private String message;
    private List<Chunk> chunks;
    private int total_count;

    public String getRequestId() { return requestId; }

    public void setRequestId(String requestId) { this.requestId = requestId; }

    public String getCode() { return code; }

    public void setCode(String code) { this.code = code; }

    public String getMessage() { return message; }

    public void setMessage(String message) { this.message = message; }

    public List<Chunk> getChunks() { return chunks; }

    public void setChunks(List<Chunk> chunks) { this.chunks = chunks; }

    public int getTotal_count() { return total_count; }

    public void setTotal_count(int total_count) { this.total_count = total_count; }

    public static class Chunk {
        private String chunk_id;
        private String knowledgebase_id;
        private String document_id;
        private String document_name;
        private Map<String, Object> meta;
        private String type;
        private String content;
        private LocalDateTime create_time;
        private LocalDateTime update_time;
        private float retrieval_score;
        private float rank_score;
        private List<ChunkLocation> locations;
        private List<Chunk> children;

        public String getChunk_id() { return chunk_id; }

        public void setChunk_id(String chunk_id) { this.chunk_id = chunk_id; }

        public String getKnowledgebase_id() { return knowledgebase_id; }

        public void setKnowledgebase_id(String knowledgebase_id) { this.knowledgebase_id = knowledgebase_id; }

        public String getDocument_id() { return document_id; }

        public void setDocument_id(String document_id) { this.document_id = document_id; }

        public String getDocument_name() { return document_name; }

        public void setDocument_name(String document_name) { this.document_name = document_name; }

        public Map<String, Object> getMeta() { return meta; }

        public void setMeta(Map<String, Object> meta) { this.meta = meta; }

        public String getType() { return type; }

        public void setType(String type) { this.type = type; }

        public String getContent() { return content; }

        public void setContent(String content) { this.content = content; }

        public LocalDateTime getCreate_time() { return create_time; }

        public void setCreate_time(LocalDateTime create_time) { this.create_time = create_time; }

        public LocalDateTime getUpdate_time() { return update_time; }

        public void setUpdate_time(LocalDateTime update_time) { this.update_time = update_time; }

        public float getRetrieval_score() { return retrieval_score; }

        public void setRetrieval_score(float retrieval_score) { this.retrieval_score = retrieval_score; }

        public float getRank_score() { return rank_score; }

        public void setRank_score(float rank_score) { this.rank_score = rank_score; }

        public List<ChunkLocation> getLocations() { return locations; }

        public void setLocations(List<ChunkLocation> locations) { this.locations = locations; }

        public List<Chunk> getChildren() { return children; }

        public void setChildren(List<Chunk> children) { this.children = children; }
    }

    public static class ChunkLocation {
        private List<Integer> paget_num;
        private List<List<Integer>> box;

        public List<Integer> getPaget_num() {
            return paget_num;
        }

        public void setPaget_num(List<Integer> paget_num) {
            this.paget_num = paget_num;
        }

        public List<List<Integer>> getBox() {
            return box;
        }

        public void setBox(List<List<Integer>> box) {
            this.box = box;
        }
    }
}
