package com.musicsite.controller;

import com.musicsite.entity.Comment;
import com.musicsite.repository.CommentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/comments")
@RequiredArgsConstructor
public class CommentController {

    private final CommentRepository commentRepo;

    @GetMapping
    public List<Comment> bySong(@RequestParam Long songId) {
        return commentRepo.findBySongIdOrderByCreatedAtDesc(songId);
    }

    @PostMapping
    public Comment create(@RequestBody Comment c) {
        return commentRepo.save(c);
    }

    @PostMapping("/{id}/like")
    public ResponseEntity<Map<String, Object>> like(@PathVariable Long id) {
        return commentRepo.findById(id).map(c -> {
            c.setLikeCount(c.getLikeCount() == null ? 1 : c.getLikeCount() + 1);
            commentRepo.save(c);
            return ResponseEntity.ok(Map.<String, Object>of("likeCount", c.getLikeCount()));
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!commentRepo.existsById(id)) return ResponseEntity.notFound().build();
        commentRepo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
