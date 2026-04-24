package com.musicsite.controller;

import com.musicsite.config.AiProperties;
import com.musicsite.dto.GenerateRequest;
import com.musicsite.entity.AiGeneration;
import com.musicsite.repository.AiGenerationRepository;
import com.musicsite.service.AiMusicService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiMusicService aiService;
    private final AiGenerationRepository generationRepo;
    private final AiProperties props;

    @GetMapping("/status")
    public Map<String, Object> status() {
        String token = props.getReplicate().getApiToken();
        boolean configured = token != null && !token.isBlank();
        return Map.of(
            "provider", "replicate",
            "configured", configured,
            "fallbackEnabled", true,
            "message", configured
                ? "AI music generation is configured."
                : "Set REPLICATE_API_TOKEN to enable real AI generation. Currently using fallback tracks."
        );
    }

    @PostMapping("/generate")
    public AiGeneration generate(@RequestBody GenerateRequest req) {
        return aiService.generate(req);
    }

    @GetMapping("/generations")
    public List<AiGeneration> latest() {
        return generationRepo.findTop20ByOrderByCreatedAtDesc();
    }

    @GetMapping("/generations/{id}")
    public ResponseEntity<AiGeneration> get(@PathVariable Long id) {
        return generationRepo.findById(id).map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
