package com.musicsite.repository;

import com.musicsite.entity.FeedPost;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface FeedPostRepository extends JpaRepository<FeedPost, Long> {
    Page<FeedPost> findByCategory(String category, Pageable pageable);
    List<FeedPost> findTop10ByIsHotTrueOrderByLikeCountDesc();
}
