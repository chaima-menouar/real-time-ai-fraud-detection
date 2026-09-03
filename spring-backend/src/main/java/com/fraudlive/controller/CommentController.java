package com.fraudlive.controller;

import com.fraudlive.dto.CreateCommentRequest;
import com.fraudlive.model.Comment;
import com.fraudlive.service.CommentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/lives/{liveId}/comments")
public class CommentController {
    private final CommentService service;

    public CommentController(CommentService service) {
        this.service = service;
    }

    @GetMapping
    public List<Comment> findAll(@PathVariable Long liveId) { return service.findByLive(liveId); }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Comment create(@PathVariable Long liveId, @Valid @RequestBody CreateCommentRequest request) {
        return service.create(liveId, request);
    }
}
