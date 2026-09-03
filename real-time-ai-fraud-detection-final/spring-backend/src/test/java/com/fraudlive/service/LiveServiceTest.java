package com.fraudlive.service;

import com.fraudlive.dto.CreateLiveRequest;
import com.fraudlive.exception.ConflictException;
import com.fraudlive.model.Live;
import com.fraudlive.model.LiveStatus;
import com.fraudlive.repository.LiveRepository;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class LiveServiceTest {
    private final LiveRepository repository = mock(LiveRepository.class);
    private final LiveService service = new LiveService(repository);

    @Test
    void createsTrimmedPlannedLive() {
        Live live = new Live("Demo");
        when(repository.save(org.mockito.ArgumentMatchers.any(Live.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        Live result = service.create(new CreateLiveRequest("  Demo  "));

        assertEquals("Demo", result.getTitle());
        assertEquals(LiveStatus.PLANNED, result.getStatus());
    }

    @Test
    void cannotStartAnEndedLive() {
        Live live = new Live("Ended");
        live.setStatus(LiveStatus.ENDED);
        when(repository.findById(7L)).thenReturn(Optional.of(live));

        assertThrows(ConflictException.class, () -> service.start(7L));
    }
}
