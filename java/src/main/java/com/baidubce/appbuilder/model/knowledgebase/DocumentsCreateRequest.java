package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class DocumentsCreateRequest {
    @SerializedName("id")
    private String knowledgeBaseId;
    private String contentFormat;
    private Source source;
    private ProcessOption processOption;

    public DocumentsCreateRequest(String knowledgeBaseId, String contentFormat, Source source,
            ProcessOption processOption) {
        this.knowledgeBaseId = knowledgeBaseId;
        this.contentFormat = contentFormat;
        this.source = source;
        this.processOption = processOption;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public String getContentFormat() {
        return contentFormat;
    }

    public Source getSource() {
        return source;
    }

    public ProcessOption getProcessOption() {
        return processOption;
    }

    public static class Source {
        private String type;
        private String[] urls;
        private Integer urlDepth;

        public Source(String type, String[] urls, Integer urlDepth) {
            this.type = type;
            this.urls = urls;
            this.urlDepth = urlDepth;
        }

        public String getType() {
            return type;
        }

        public String[] getUrls() {
            return urls;
        }

        public Integer getUrlDepth() {
            return urlDepth;
        }
    }

    public static class ProcessOption {
        private String template;
        private Parser parser;
        private Chunker chunker;
        private KnowledgeAugmentation knowledgeAugmentation;

        public ProcessOption(String template, Parser parser, Chunker chunker,
                KnowledgeAugmentation knowledgeAugmentation) {
            this.template = template;
            this.parser = parser;
            this.chunker = chunker;
            this.knowledgeAugmentation = knowledgeAugmentation;
        }

        public String getTemplate() {
            return template;
        }

        public Parser getParser() {
            return parser;
        }

        public Chunker getChunker() {
            return chunker;
        }

        public KnowledgeAugmentation getKnowledgeAugmentation() {
            return knowledgeAugmentation;
        }

        public static class Parser {
            private String[] choices;

            public Parser(String[] choices) {
                this.choices = choices;
            }

            public String[] getChoices() {
                return choices;
            }
        }

        public static class Chunker {
            private String[] choices;
            private Separator separator;
            private Pattern pattern;
            private String[] prependInfo;

            public Chunker(String[] choices, Separator separator, Pattern pattern,
                    String[] prependInfo) {
                this.choices = choices;
                this.separator = separator;
                this.pattern = pattern;
                this.prependInfo = prependInfo;
            }

            public String[] getChoices() {
                return choices;
            }

            public Separator getSeparator() {
                return separator;
            }

            public Pattern getPattern() {
                return pattern;
            }

            public String[] getPrependInfo() {
                return prependInfo;
            }

            public static class Separator {
                private String[] separators;
                private Integer targetLength;
                private Double overlapRate;

                public Separator(String[] separators, Integer targetLength, Double overlapRate) {
                    this.separators = separators;
                    this.targetLength = targetLength;
                    this.overlapRate = overlapRate;
                }

                public String[] getSeparators() {
                    return separators;
                }

                public Integer getTargetLength() {
                    return targetLength;
                }

                public Double getOverlapRate() {
                    return overlapRate;
                }
            }

            public static class Pattern {
                private String markPosition;
                private String regex;
                private Integer targetLength;
                private Double overlapRate;

                public Pattern(String markPosition, String regex, Integer targetLength,
                        Double overlapRate) {
                    this.markPosition = markPosition;
                    this.regex = regex;
                    this.targetLength = targetLength;
                    this.overlapRate = overlapRate;
                }

                public String getMarkPosition() {
                    return markPosition;
                }

                public String getRegex() {
                    return regex;
                }

                public Integer getTargetLength() {
                    return targetLength;
                }

                public Double getOverlapRate() {
                    return overlapRate;
                }
            }
        }

        public static class KnowledgeAugmentation {
            private String[] choices;

            public KnowledgeAugmentation(String[] choices) {
                this.choices = choices;
            }

            public String[] getChoices() {
                return choices;
            }
        }
    }
}
