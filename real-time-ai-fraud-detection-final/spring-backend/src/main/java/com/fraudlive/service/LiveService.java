package com.fraudlive.service;

import com.fraudlive.dto.CreateLiveRequest;
import com.fraudlive.exception.ConflictException;
import com.fraudlive.exception.ResourceNotFoundException;
import com.fraudlive.model.Live;
import com.fraudlive.model.LiveStatus;
import com.fraudlive.repository.LiveRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class LiveService {
    private final LiveRepository repository;

    public LiveService(LiveRepository repository) {
        this.repository = repository;
    }

    @Transactional(readOnly = true)
    public List<Live> findAll() {
        return repository.findAll();
    }

    @Transactional(readOnly = true)
    public Live findById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Live session not found"));
    }

    @Transactional
    public Live create(CreateLiveRequest request) {
        return repository.save(new Live(request.title().trim()));
    }

    @Transactional
    public Live start(Long id) {
        Live live = findById(id);
        if (live.getStatus() != LiveStatus.PLANNED) {
            throw new ConflictException("Only a planned live can be started");
        }
        live.setStatus(LiveStatus.ACTIVE);
        return repository.save(live);
    }

    @Transactional
    public Live end(Long id) {
        Live live = findById(id);
        if (live.getStatus() != LiveStatus.ACTIVE) {
            throw new ConflictException("Only an active live can be ended");
        }
        live.setStatus(LiveStatus.ENDED);
        return repository.save(live);
    }
}
