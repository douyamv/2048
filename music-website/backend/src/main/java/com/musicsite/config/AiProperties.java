package com.musicsite.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.ArrayList;
import java.util.List;

@Data
@Configuration
@ConfigurationProperties(prefix = "ai")
public class AiProperties {
    private String provider = "replicate";
    private Replicate replicate = new Replicate();
    private Fallback fallback = new Fallback();

    @Data
    public static class Replicate {
        private String apiToken = "";
        private String modelVersion = "";
        private String baseUrl = "https://api.replicate.com/v1";
    }

    @Data
    public static class Fallback {
        private List<String> audioUrls = new ArrayList<>();
    }
}
