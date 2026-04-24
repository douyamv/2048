package com.musicsite.controller;

import com.musicsite.entity.Playlist;
import com.musicsite.entity.Song;
import com.musicsite.repository.PlaylistRepository;
import com.musicsite.repository.SongRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/playlists")
@RequiredArgsConstructor
public class PlaylistController {

    private final PlaylistRepository playlistRepo;
    private final SongRepository songRepo;

    @GetMapping
    public List<Playlist> all(@RequestParam(required = false) String owner) {
        if (owner != null && !owner.isBlank()) {
            return playlistRepo.findByOwnerName(owner);
        }
        return playlistRepo.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Playlist> get(@PathVariable Long id) {
        return playlistRepo.findById(id).map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Playlist create(@RequestBody Playlist p) {
        return playlistRepo.save(p);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Playlist> update(@PathVariable Long id, @RequestBody Playlist body) {
        return playlistRepo.findById(id).map(p -> {
            if (body.getName() != null) p.setName(body.getName());
            if (body.getDescription() != null) p.setDescription(body.getDescription());
            if (body.getCoverUrl() != null) p.setCoverUrl(body.getCoverUrl());
            return ResponseEntity.ok(playlistRepo.save(p));
        }).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/{id}/songs/{songId}")
    public ResponseEntity<Playlist> addSong(@PathVariable Long id, @PathVariable Long songId) {
        var po = playlistRepo.findById(id);
        var so = songRepo.findById(songId);
        if (po.isEmpty() || so.isEmpty()) return ResponseEntity.notFound().build();
        Playlist p = po.get();
        Song s = so.get();
        if (!p.getSongs().contains(s)) {
            p.getSongs().add(s);
            playlistRepo.save(p);
        }
        return ResponseEntity.ok(p);
    }

    @DeleteMapping("/{id}/songs/{songId}")
    public ResponseEntity<Playlist> removeSong(@PathVariable Long id, @PathVariable Long songId) {
        return playlistRepo.findById(id).map(p -> {
            p.getSongs().removeIf(s -> s.getId().equals(songId));
            return ResponseEntity.ok(playlistRepo.save(p));
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!playlistRepo.existsById(id)) return ResponseEntity.notFound().build();
        playlistRepo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
