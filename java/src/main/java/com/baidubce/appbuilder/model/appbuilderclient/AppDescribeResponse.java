package com.baidubce.appbuilder.model.appbuilderclient;

public class AppDescribeResponse {
    private String requestId;
    private String id;
    private String name;
    private String description;
    private String instruction;
    private String prologue;
    private String[] exampleQueries;
    private FollowUpQueries followUpQueries;
    private Component[] components;
    private KnowledgeBaseConfig knowledgeBaseConfig;
    private ModelConfig modelConfig;
    private BackgroundConfig background;

    // Getters and Setters
    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getInstruction() {
        return instruction;
    }

    public void setInstruction(String instruction) {
        this.instruction = instruction;
    }

    public String getPrologue() {
        return prologue;
    }

    public void setPrologue(String prologue) {
        this.prologue = prologue;
    }

    public String[] getExampleQueries() {
        return exampleQueries;
    }

    public void setExampleQueries(String[] exampleQueries) {
        this.exampleQueries = exampleQueries;
    }

    public FollowUpQueries getFollowUpQueries() {
        return followUpQueries;
    }

    public void setFollowUpQueries(FollowUpQueries followUpQueries) {
        this.followUpQueries = followUpQueries;
    }

    public Component[] getComponents() {
        return components;
    }

    public void setComponents(Component[] components) {
        this.components = components;
    }

    public KnowledgeBaseConfig getKnowledgeBaseConfig() {
        return knowledgeBaseConfig;
    }

    public void setKnowledgeBaseConfig(KnowledgeBaseConfig knowledgeBaseConfig) {
        this.knowledgeBaseConfig = knowledgeBaseConfig;
    }

    public ModelConfig getModelConfig() {
        return modelConfig;
    }

    public void setModelConfig(ModelConfig modelConfig) {
        this.modelConfig = modelConfig;
    }

    public BackgroundConfig getBackground() {
        return background;
    }

    public void setBackground(BackgroundConfig background) {
        this.background = background;
    }

    public static class FollowUpQueries {
        private String type;
        private String prompt;
        private String round;

        // Getters and Setters
        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }
        
        public String getPrompt() {
            return prompt;
        }

        public void setPrompt(String prompt) {
            this.prompt = prompt;
        }

        public String getRound() {
            return round;
        }

        public void setRound(String round) {
            this.round = round;
        }
    }

    public static class Component {
        private String name;
        private String description;
        private String customDesc;

        // Getters and Setters
        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
        
        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }

        public String getCustomDesc() {
            return customDesc;
        }

        public void setCustomDesc(String customDesc) {
            this.customDesc = customDesc;
        }
    }

    public static class KnowledgeBaseConfig {
        private KnowledgeBase[] knowledgeBases;
        private RetrievalConfig retrieval;

        // Getters and Setters
        public KnowledgeBase[] getKnowledgeBases() {
            return knowledgeBases;
        }

        public void setKnowledgeBases(KnowledgeBase[] knowledgeBases) {
            this.knowledgeBases = knowledgeBases;
        }

        public RetrievalConfig getRetrieval() {
            return retrieval;
        }

        public void setRetrieval(RetrievalConfig retrieval) {
            this.retrieval = retrieval;
        }

        public static class KnowledgeBase {
            private String id;
            private String name;
            private String description;

            // Getters and Setters
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

            public String getDescription() {
                return description;
            }

            public void setDescription(String description) {
                this.description = description;
            }
        }

        public static class RetrievalConfig {
            private Boolean enableWebSearch;
            private String order;
            private String strategy;
            private Integer topK;
            private Float threshold;

            // Getters and Setters
            public Boolean getEnableWebSearch() {
                return enableWebSearch;
            }

            public void setEnableWebSearch(Boolean enableWebSearch) {
                this.enableWebSearch = enableWebSearch;
            }

            public String getOrder() {
                return order;
            }

            public void setOrder(String order) {
                this.order = order;
            }

            public String getStrategy() {
                return strategy;
            }

            public void setStrategy(String strategy) {
                this.strategy = strategy;
            }

            public Integer getTopK() {
                return topK;
            }

            public void setTopK(Integer topK) {
                this.topK = topK;
            }

            public Float getThreshold() {
                return threshold;
            }

            public void setThreshold(Float threshold) {
                this.threshold = threshold;
            }
        }
    }

    public static class ModelConfig {
        private PlanConfig plan;
        private ChatConfig chat;

        // Getters and Setters
        public PlanConfig getPlan() {
            return plan;
        }

        public void setPlan(PlanConfig plan) {
            this.plan = plan;
        }

        public ChatConfig getChat() {
            return chat;
        }

        public void setChat(ChatConfig chat) {
            this.chat = chat;
        }

        public static class PlanConfig {
            private String modelId;
            private String model;
            private Integer maxRounds;
            private Config config;

            // Getters and Setters
            public String getModelId() {
                return modelId;
            }

            public void setModelId(String modelId) {
                this.modelId = modelId;
            }

            public String getModel() {
                return model;
            }

            public void setModel(String model) {
                this.model = model;
            }

            public Integer getMaxRounds() {
                return maxRounds;
            }

            public void setMaxRounds(Integer maxRounds) {
                this.maxRounds = maxRounds;
            }

            public Config getConfig() {
                return config;
            }

            public void setConfig(Config config) {
                this.config = config;
            }

            public static class Config {
                private Float temperature;
                private Float topP;

                // Getters and Setters
                public Float getTemperature() {
                    return temperature;
                }

                public void setTemperature(Float temperature) {
                    this.temperature = temperature;
                }
                
                public Float getTopP() {
                    return topP;
                }

                public void setTopP(Float topP) {
                    this.topP = topP;
                }
            }
        }

        public static class ChatConfig {
            private String modelId;
            private String model;
            private Integer historyChatRounds;
            private Config config;
            // Getters and Setters...

            public String getModelId() {
                return modelId;
            }

            public void setModelId(String modelId) {
                this.modelId = modelId;
            }

            public String getModel() {
                return model;
            }

            public void setModel(String model) {
                this.model = model;
            }

            public Integer getHistoryChatRounds() {
                return historyChatRounds;
            }

            public void setHistoryChatRounds(Integer historyChatRounds) {
                this.historyChatRounds = historyChatRounds;
            }

            public Config getConfig() {
                return config;
            }

            public void setConfig(Config config) {
                this.config = config;
            }

            public static class Config {
                private Float temperature;
                private Float topP;

                // Getters and Setters
                public Float getTemperature() {
                    return temperature;
                }

                public void setTemperature(Float temperature) {
                    this.temperature = temperature;
                }

                public Float getTopP() {
                    return topP;
                }

                public void setTopP(Float topP) {
                    this.topP = topP;
                }
            }
        }
    }

    public static class BackgroundConfig {
        private String id;
        private String path;
        private MobileConfig mobileConfig;
        private PcConfig pcConfig;

        // Getters and Setters
        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public String getPath() {
            return path;
        }

        public void setPath(String path) {
            this.path = path;
        }

        public MobileConfig getMobileConfig() {
            return mobileConfig;
        }

        public void setMobileConfig(MobileConfig mobileConfig) {
            this.mobileConfig = mobileConfig;
        }

        public PcConfig getPcConfig() {
            return pcConfig;
        }

        public void setPcConfig(PcConfig pcConfig) {
            this.pcConfig = pcConfig;
        }

        public static class MobileConfig {
            private String left;
            private String top;
            private String height;
            private String color;
            // Getters and Setters...

            public String getLeft() {
                return left;
            }

            public void setLeft(String left) {
                this.left = left;
            }

            public String getTop() {
                return top;
            }
            
            public void setTop(String top) {
                this.top = top;
            }

            public String getHeight() {
                return height;
            }

            public void setHeight(String height) {
                this.height = height;
            }

            public String getColor() {
                return color;
            }

            public void setColor(String color) {
                this.color = color;
            }
        }

        public static class PcConfig {
            private String left;
            private String top;
            private String height;
            private String color;
            // Getters and Setters...

            public String getLeft() {
                return left;
            }

            public void setLeft(String left) {
                this.left = left;
            }

            public String getTop() {
                return top;
            }

            public void setTop(String top) {
                this.top = top;
            }

            public String getHeight() {
                return height;
            }

            public void setHeight(String height) {
                this.height = height;
            }

            public String getColor() {
                return color;
            }

            public void setColor(String color) {
                this.color = color;
            }
        }
    }
}
