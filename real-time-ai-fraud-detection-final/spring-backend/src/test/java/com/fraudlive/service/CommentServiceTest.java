package com.fraudlive.service;

import com.fraudlive.dto.CreateCommentRequest;
import com.fraudlive.exception.ModelUnavailableException;
import com.fraudlive.model.Live;
import com.fraudlive.model.LiveStatus;
import com.fraudlive.repository.CommentRepository;
import com.fraudlive.repository.LiveRepository;
import org.junit.jupiter.api.Test;
import org.springframework.messaging.simp.SimpMessagingTemplate;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class CommentServiceTest {
    @Test
    void modelFailureDoesNotSaveAnInventedClassification() {
        LiveRepository liveRepository = mock(LiveRepository.class);
        CommentRepository commentRepository = mock(CommentRepository.class);
        AiModelClient modelClient = mock(AiModelClient.class);
        SimpMessagingTemplate messaging = mock(SimpMessagingTemplate.class);
        CommentService service = new CommentService(liveRepository, commentRepository, modelClient, messaging);
        Live live = new Live("Demo");
        live.setStatus(LiveStatus.ACTIVE);
        when(liveRepository.findById(1L)).thenReturn(Optional.of(live));
        when(modelClient.predict("test comment"))
                .thenThrow(new ModelUnavailableException("unavailable", null));

        assertThrows(
                ModelUnavailableException.class,
                () -> service.create(1L, new CreateCommentRequest("reviewer", "test comment"))
        );
        verify(commentRepository, never()).save(org.mockito.ArgumentMatchers.any());
    }
}
