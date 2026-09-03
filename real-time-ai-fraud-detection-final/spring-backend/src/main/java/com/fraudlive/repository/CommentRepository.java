package com.fraudlive.repository;

import com.fraudlive.model.Comment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CommentRepository extends JpaRepository<Comment, Long> {
    List<Comment> findByLiveIdOrderByCreatedAtAsc(Long liveId);
}
