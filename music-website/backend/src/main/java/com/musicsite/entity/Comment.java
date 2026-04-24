package com.musicsite.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.Instant;

@Data
@Entity
@Table(name = "comments")
public class Comment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "song_id")
    private Long songId;

    @Column(nullable = false, length = 80)
    private String author;

    @Column(nullable = false, length = 1000)
    private String content;

    @Column(name = "like_count")
    private Long likeCount = 0L;

    @Column(name = "created_at")
    private Instant createdAt = Instant.now();
}
