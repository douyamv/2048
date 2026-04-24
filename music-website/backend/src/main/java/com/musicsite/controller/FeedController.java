package com.musicsite.controller;

import com.musicsite.entity.FeedPost;
import com.musicsite.repository.FeedPostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/feed")
@RequiredArgsConstructor
public class FeedController {

    private final FeedPostRepository feedRepo;

    @GetMapping
    public Page<FeedPost> list(@RequestParam(required = false) String category,
                               @RequestParam(defaultValue = "0") int page,
                               @RequestParam(defaultValue = "20") int size) {
        var pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        if (category != null && !category.isBlank() && !"all".equals(category)) {
            return feedRepo.findByCategory(category, pageable);
        }
        return feedRepo.findAll(pageable);
    }

    @GetMapping("/hot")
    public List<FeedPost> hot() {
        return feedRepo.findTop10ByIsHotTrueOrderByLikeCountDesc();
    }

    @PostMapping
    public FeedPost create(@RequestBody FeedPost p) {
        return feedRepo.save(p);
    }

    @PostMapping("/{id}/like")
    public ResponseEntity<Map<String, Object>> like(@PathVariable Long id) {
        return feedRepo.findById(id).map(p -> {
            p.setLikeCount(p.getLikeCount() == null ? 1 : p.getLikeCount() + 1);
            feedRepo.save(p);
            return ResponseEntity.ok(Map.<String, Object>of("likeCount", p.getLikeCount()));
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!feedRepo.existsById(id)) return ResponseEntity.notFound().build();
        feedRepo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
