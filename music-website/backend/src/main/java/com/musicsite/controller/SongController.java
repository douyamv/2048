package com.musicsite.controller;

import com.musicsite.entity.Song;
import com.musicsite.repository.SongRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/songs")
@RequiredArgsConstructor
public class SongController {

    private final SongRepository songRepo;

    @GetMapping
    public Page<Song> list(@RequestParam(defaultValue = "0") int page,
                           @RequestParam(defaultValue = "20") int size,
                           @RequestParam(required = false) String genre) {
        var pageable = PageRequest.of(page, size);
        if (genre != null && !genre.isBlank() && !"all".equalsIgnoreCase(genre)) {
            return songRepo.findByGenre(genre, pageable);
        }
        return songRepo.findAll(pageable);
    }

    @GetMapping("/hot")
    public List<Song> hot() {
        return songRepo.findTop10ByOrderByPlayCountDesc();
    }

    @GetMapping("/latest")
    public List<Song> latest() {
        return songRepo.findTop12ByOrderByCreatedAtDesc();
    }

    @GetMapping("/search")
    public Page<Song> search(@RequestParam String q,
                             @RequestParam(defaultValue = "0") int page,
                             @RequestParam(defaultValue = "20") int size) {
        return songRepo.findByTitleContainingIgnoreCaseOrArtistContainingIgnoreCase(
            q, q, PageRequest.of(page, size));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Song> get(@PathVariable Long id) {
        return songRepo.findById(id).map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/{id}/play")
    public ResponseEntity<Map<String, Object>> incrementPlay(@PathVariable Long id) {
        return songRepo.findById(id).map(s -> {
            s.setPlayCount(s.getPlayCount() == null ? 1 : s.getPlayCount() + 1);
            songRepo.save(s);
            return ResponseEntity.ok(Map.<String, Object>of("playCount", s.getPlayCount()));
        }).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/{id}/like")
    public ResponseEntity<Map<String, Object>> like(@PathVariable Long id) {
        return songRepo.findById(id).map(s -> {
            s.setLikeCount(s.getLikeCount() == null ? 1 : s.getLikeCount() + 1);
            songRepo.save(s);
            return ResponseEntity.ok(Map.<String, Object>of("likeCount", s.getLikeCount()));
        }).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Song create(@RequestBody Song song) {
        if (song.getSource() == null) song.setSource("user");
        return songRepo.save(song);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!songRepo.existsById(id)) return ResponseEntity.notFound().build();
        songRepo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
