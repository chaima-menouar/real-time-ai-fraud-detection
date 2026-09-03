package com.fraudlive.service;

import com.fraudlive.dto.AiPredictionResponse;
import com.fraudlive.dto.CreateCommentRequest;
import com.fraudlive.exception.ConflictException;
import com.fraudlive.exception.ResourceNotFoundException;
import com.fraudlive.model.Comment;
import com.fraudlive.model.Live;
import com.fraudlive.model.LiveStatus;
import com.fraudlive.repository.CommentRepository;
import com.fraudlive.repository.LiveRepository;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class CommentService {
    private final LiveRepository liveRepository;
    private final CommentRepository commentRepository;
    private final AiModelClient aiModelClient;
    private final SimpMessagingTemplate messagingTemplate;

    public CommentService(LiveRepository liveRepository, CommentRepository commentRepository,
                          AiModelClient aiModelClient, SimpMessagingTemplate messagingTemplate) {
        this.liveRepository = liveRepository;
        this.commentRepository = commentRepository;
        this.aiModelClient = aiModelClient;
        this.messagingTemplate = messagingTemplate;
    }

    @Transactional(readOnly = true)
    public List<Comment> findByLive(Long liveId) {
        if (!liveRepository.existsById(liveId)) {
            throw new ResourceNotFoundException("Live session not found");
        }
        return commentRepository.findByLiveIdOrderByCreatedAtAsc(liveId);
    }

    @Transactional
    public Comment create(Long liveId, CreateCommentRequest request) {
        Live live = liveRepository.findById(liveId)
                .orElseThrow(() -> new ResourceNotFoundException("Live session not found"));
        if (live.getStatus() != LiveStatus.ACTIVE) {
            throw new ConflictException("Comments are accepted only while the live is active");
        }

        AiPredictionResponse prediction = aiModelClient.predict(request.content().trim());
        Comment comment = new Comment(
                live,
                request.author().trim(),
                request.content().trim(),
                prediction.category(),
                prediction.risk(),
                prediction.confidence(),
                prediction.modelVersion()
        );
        Comment saved = commentRepository.save(comment);
        messagingTemplate.convertAndSend("/topic/lives/" + liveId + "/comments", saved);
        return saved;
    }
}
