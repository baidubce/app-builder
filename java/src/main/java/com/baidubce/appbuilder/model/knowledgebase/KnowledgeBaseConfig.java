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
        private String esUrl;
        private String username;
        private String password;

        public Index(String type, String esUrl, String username, String password) {
            this.type = type;
            this.esUrl = esUrl;
            this.username = username;
            this.password = password;
        }

        public String getType() {
            return type;
        }

        public String getEsUrl() {
            return esUrl;
        }

        public String getUsername() {
            return username;
        }

        public String getPassword() {
            return password;
        }
    }
}
