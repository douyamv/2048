package com.musicsite.repository;

import com.musicsite.entity.Song;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface SongRepository extends JpaRepository<Song, Long> {
    Page<Song> findByTitleContainingIgnoreCaseOrArtistContainingIgnoreCase(
        String title, String artist, Pageable pageable);

    List<Song> findTop10ByOrderByPlayCountDesc();

    List<Song> findTop12ByOrderByCreatedAtDesc();

    Page<Song> findByGenre(String genre, Pageable pageable);
}
