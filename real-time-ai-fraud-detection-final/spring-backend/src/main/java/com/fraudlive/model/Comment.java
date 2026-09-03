package com.fraudlive.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.time.Instant;

@Entity
@Table(name = "live_comments")
public class Comment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @JsonIgnore
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Live live;

    @Column(nullable = false, length = 80)
    private String author;
    @Column(nullable = false, length = 2000)
    private String content;
    @Column(nullable = false, length = 120)
    private String category;
    private boolean risk;
    private double confidence;
    @Column(nullable = false, length = 160)
    private String modelVersion;
    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    protected Comment() {
    }

    public Comment(Live live, String author, String content, String category,
                   boolean risk, double confidence, String modelVersion) {
        this.live = live;
        this.author = author;
        this.content = content;
        this.category = category;
        this.risk = risk;
        this.confidence = confidence;
        this.modelVersion = modelVersion;
    }

    public Long getId() { return id; }
    public Long getLiveId() { return live.getId(); }
    public String getAuthor() { return author; }
    public String getContent() { return content; }
    public String getCategory() { return category; }
    public boolean isRisk() { return risk; }
    public double getConfidence() { return confidence; }
    public String getModelVersion() { return modelVersion; }
    public Instant getCreatedAt() { return createdAt; }
}
