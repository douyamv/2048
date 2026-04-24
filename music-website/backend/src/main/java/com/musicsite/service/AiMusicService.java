package com.musicsite.service;

import com.musicsite.config.AiProperties;
import com.musicsite.dto.GenerateRequest;
import com.musicsite.entity.AiGeneration;
import com.musicsite.entity.Song;
import com.musicsite.repository.AiGenerationRepository;
import com.musicsite.repository.SongRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiMusicService {

    private final AiGenerationRepository generationRepo;
    private final SongRepository songRepo;
    private final RestTemplate restTemplate;
    private final AiProperties props;

    public AiGeneration generate(GenerateRequest req) {
        AiGeneration g = new AiGeneration();
        g.setRequester(req.getRequester() != null ? req.getRequester() : "anonymous");
        g.setPrompt(req.getPrompt());
        g.setStyle(req.getStyle());
        g.setDurationSec(req.getDurationSec() != null ? req.getDurationSec() : 8);
        g.setProvider("replicate");
        g.setStatus("pending");
        g = generationRepo.save(g);

        String token = props.getReplicate().getApiToken();
        boolean tokenSet = token != null && !token.isBlank();
        if (tokenSet) {
            try {
                String audioUrl = callReplicate(g);
                g.setAudioUrl(audioUrl);
                g.setStatus("succeeded");
                g.setCompletedAt(Instant.now());
            } catch (Exception ex) {
                log.warn("Replicate call failed, using fallback: {}", ex.getMessage());
                applyFallback(g, "AI provider error: " + ex.getMessage());
            }
        } else {
            log.info("REPLICATE_API_TOKEN not set, using fallback audio");
            applyFallback(g, "REPLICATE_API_TOKEN not configured");
        }

        AiGeneration saved = generationRepo.save(g);

        if (Boolean.TRUE.equals(req.getSaveAsSong()) && saved.getAudioUrl() != null) {
            Song s = new Song();
            String title = (req.getTitle() != null && !req.getTitle().isBlank())
                ? req.getTitle()
                : ("AI · " + abbreviate(req.getPrompt(), 30));
            s.setTitle(title);
            s.setArtist(saved.getRequester() + " (AI)");
            s.setGenre(req.getStyle() != null ? req.getStyle() : "AI");
            s.setAudioUrl(saved.getAudioUrl());
            s.setCoverUrl(randomCover());
            s.setDurationSec(saved.getDurationSec());
            s.setSource("ai");
            songRepo.save(s);
        }

        return saved;
    }

    private void applyFallback(AiGeneration g, String reason) {
        g.setStatus("fallback");
        g.setAudioUrl(pickFallback());
        g.setErrorMessage(reason);
        g.setCompletedAt(Instant.now());
    }

    private String pickFallback() {
        List<String> urls = props.getFallback().getAudioUrls();
        if (urls == null || urls.isEmpty()) {
            return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3";
        }
        return urls.get(ThreadLocalRandom.current().nextInt(urls.size()));
    }

    private String callReplicate(AiGeneration g) {
        var rep = props.getReplicate();
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Token " + rep.getApiToken());
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> input = new HashMap<>();
        String fullPrompt = g.getPrompt() == null ? "" : g.getPrompt();
        if (g.getStyle() != null && !g.getStyle().isBlank()) {
            fullPrompt = g.getStyle() + " style: " + fullPrompt;
        }
        input.put("prompt", fullPrompt);
        input.put("duration", g.getDurationSec());
        input.put("model_version", "stereo-large");
        input.put("output_format", "mp3");
        input.put("normalization_strategy", "peak");

        Map<String, Object> body = new HashMap<>();
        body.put("version", rep.getModelVersion());
        body.put("input", input);

        ResponseEntity<Map> create = restTemplate.exchange(
            rep.getBaseUrl() + "/predictions",
            HttpMethod.POST,
            new HttpEntity<>(body, headers),
            Map.class
        );

        Map<String, Object> created = create.getBody();
        if (created == null) throw new RuntimeException("Empty response from Replicate");
        String predictionId = (String) created.get("id");
        g.setExternalId(predictionId);

        for (int i = 0; i < 60; i++) {
            try { Thread.sleep(2000); } catch (InterruptedException ignored) {}
            ResponseEntity<Map> poll = restTemplate.exchange(
                rep.getBaseUrl() + "/predictions/" + predictionId,
                HttpMethod.GET,
                new HttpEntity<>(headers),
                Map.class
            );
            Map<String, Object> p = poll.getBody();
            if (p == null) continue;
            String status = String.valueOf(p.get("status"));
            if ("succeeded".equals(status)) {
                Object output = p.get("output");
                if (output instanceof String s) return s;
                if (output instanceof List<?> list && !list.isEmpty()) {
                    return String.valueOf(list.get(0));
                }
                throw new RuntimeException("No output in Replicate response");
            }
            if ("failed".equals(status) || "canceled".equals(status)) {
                throw new RuntimeException("Replicate prediction " + status + ": " + p.get("error"));
            }
        }
        throw new RuntimeException("Replicate prediction timed out");
    }

    private String abbreviate(String s, int max) {
        if (s == null) return "";
        return s.length() <= max ? s : s.substring(0, max) + "...";
    }

    private String randomCover() {
        int seed = ThreadLocalRandom.current().nextInt(1, 1000);
        return "https://picsum.photos/seed/ai" + seed + "/400/400";
    }
}
