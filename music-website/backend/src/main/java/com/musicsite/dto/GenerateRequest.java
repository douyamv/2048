package com.musicsite.dto;

import lombok.Data;

@Data
public class GenerateRequest {
    private String requester = "anonymous";
    private String prompt;
    private String style;
    private Integer durationSec = 8;
    private Boolean saveAsSong = false;
    private String title;
}
