package com.fraudlive.repository;

import com.fraudlive.model.Live;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LiveRepository extends JpaRepository<Live, Long> {
}
