package com.fraudlive.controller;

import com.fraudlive.dto.CreateLiveRequest;
import com.fraudlive.model.Live;
import com.fraudlive.service.LiveService;
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
@RequestMapping("/api/lives")
public class LiveController {
    private final LiveService service;

    public LiveController(LiveService service) {
        this.service = service;
    }

    @GetMapping
    public List<Live> findAll() { return service.findAll(); }

    @GetMapping("/{id}")
    public Live findById(@PathVariable Long id) { return service.findById(id); }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Live create(@Valid @RequestBody CreateLiveRequest request) { return service.create(request); }

    @PostMapping("/{id}/start")
    public Live start(@PathVariable Long id) { return service.start(id); }

    @PostMapping("/{id}/end")
    public Live end(@PathVariable Long id) { return service.end(id); }
}
