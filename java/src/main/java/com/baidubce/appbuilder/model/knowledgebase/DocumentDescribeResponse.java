package com.baidubce.appbuilder.model.knowledgebase;

public class DocumentDescribeResponse {
    private String id;
    private String name;
    private String createdAt;
    private String displayStatus;
    private Integer wordCount;
    private Boolean enabled;
    private Meta meta;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public String getDisplayStatus() {
        return displayStatus;
    }

    public void setDisplayStatus(String displayStatus) {
        this.displayStatus = displayStatus;
    }

    public Integer getWordCount() {
        return wordCount;
    }

    public void setWordCount(Integer wordCount) {
        this.wordCount = wordCount;
    }

    public Boolean getEnabled() {
        return enabled;
    }

    public void setEnabled(Boolean enabled) {
        this.enabled = enabled;
    }

    public Meta getMeta() {
        return meta;
    }

    public void setMeta(Meta meta) {
        this.meta = meta;
    }

    public static class Meta {
        private String source;
        private String fileId;
        private String url;
        private String mime_type;
        private Integer file_size;


        public String getSource() {
            return source;
        }

        public void setSource(String source) {
            this.source = source;
        }

        public String getFileId() {
            return fileId;
        }

        public void setFileId(String fileId) {
            this.fileId = fileId;
        }

        public String getUrl() {
            return url;
        }

        public void setUrl(String url) {
            this.url = url;
        }
        
        public String getMimeType() {
            return mime_type;
        }

        public void setMimeType(String mime_type) {
            this.mime_type = mime_type;
        }

        public Integer getFileSize() {
            return file_size;
        }

        public void setFileSize(Integer file_size) {
            this.file_size = file_size;
        }
    }
}
