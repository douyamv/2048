package com.musicsite.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.Instant;

@Data
@Entity
@Table(name = "feed_posts")
public class FeedPost {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 80)
    private String author;

    @Column(length = 80)
    private String avatar;

    @Column(length = 50)
    private String category;

    @Column(nullable = false, length = 2000)
    private String content;

    @Column(name = "image_url", length = 500)
    private String imageUrl;

    @Column(name = "song_id")
    private Long songId;

    @Column(name = "like_count")
    private Long likeCount = 0L;

    @Column(name = "reply_count")
    private Long replyCount = 0L;

    @Column(name = "is_hot")
    private Boolean isHot = false;

    @Column(name = "created_at")
    private Instant createdAt = Instant.now();
}
