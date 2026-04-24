package com.musicsite.repository;

import com.musicsite.entity.AiGeneration;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface AiGenerationRepository extends JpaRepository<AiGeneration, Long> {
    List<AiGeneration> findTop20ByOrderByCreatedAtDesc();
    List<AiGeneration> findByRequesterOrderByCreatedAtDesc(String requester);
}
