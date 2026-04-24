package com.musicsite.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.Instant;

@Data
@Entity
@Table(name = "ai_generations")
public class AiGeneration {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 80)
    private String requester;

    @Column(nullable = false, length = 1000)
    private String prompt;

    @Column(length = 100)
    private String style;

    @Column(name = "duration_sec")
    private Integer durationSec = 8;

    @Column(length = 30)
    private String status = "pending";

    @Column(name = "audio_url", length = 1000)
    private String audioUrl;

    @Column(name = "provider", length = 50)
    private String provider;

    @Column(name = "external_id", length = 200)
    private String externalId;

    @Column(name = "error_message", length = 1000)
    private String errorMessage;

    @Column(name = "created_at")
    private Instant createdAt = Instant.now();

    @Column(name = "completed_at")
    private Instant completedAt;
}
