package com.musicsite.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.Instant;

@Data
@Entity
@Table(name = "songs")
public class Song {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String title;

    @Column(nullable = false, length = 120)
    private String artist;

    @Column(length = 80)
    private String genre;

    @Column(name = "cover_url", length = 500)
    private String coverUrl;

    @Column(name = "audio_url", nullable = false, length = 1000)
    private String audioUrl;

    @Column(name = "duration_sec")
    private Integer durationSec;

    @Column(name = "play_count")
    private Long playCount = 0L;

    @Column(name = "like_count")
    private Long likeCount = 0L;

    @Column(length = 30)
    private String source = "system";

    @Column(name = "created_at")
    private Instant createdAt = Instant.now();
}
