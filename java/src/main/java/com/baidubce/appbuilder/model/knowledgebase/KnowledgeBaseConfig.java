package com.baidubce.appbuilder.model.knowledgebase;

public class KnowledgeBaseConfig {
    private Index index;
    private Catalogue catalogue;

    public KnowledgeBaseConfig(Index index) {
        this.index = index;
    }

    public KnowledgeBaseConfig(Index index, Catalogue catalogue) {
        this.index = index;
        this.catalogue = catalogue;
    }

    public Index getIndex() {
        return index;
    }

    public void setIndex(Index index) {
        this.index = index;
    }

    public void setCatalogue(Catalogue catalogue) {
        this.catalogue = catalogue;
    }

    public Catalogue getCatalogue() {
        return catalogue;
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

    public static class Catalogue {
        private String pathPrefix;
        
        public void setPathPrefix(String pathPrefix) {
            this.pathPrefix = pathPrefix;
        }

        public String getPathPrefix() {
            return pathPrefix;
        }
    }
}
