package com.baidubce.appbuilder.model.knowledgebase;

public class KnowledgeBaseConfig {
    private Index index;

    public KnowledgeBaseConfig(Index index) {
        this.index = index;
    }

    public Index getIndex() {
        return index;
    }

    public static class Index {
        private String type;
        private String clusterId;
        private String username;
        private String password;
        private String location;

        public Index(String type, String clusterId, String username, String password, String location) {
            this.type = type;
            this.clusterId = clusterId;
            this.username = username;
            this.password = password;
            this.location = location;
        }

        public String getType() {
            return type;
        }

        public String getClusterId() {
            return clusterId;
        }

        public String getUsername() {
            return username;
        }

        public String getPassword() {
            return password;
        }

        public String getLocation() {
            return location;
        }
    }
}
