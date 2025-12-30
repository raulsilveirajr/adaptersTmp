package com.nttdata.bees_account_consumer.entity

import io.hypersistence.utils.hibernate.type.json.JsonType
import jakarta.persistence.*
import lombok.Data
import org.hibernate.annotations.Type
import java.time.LocalDateTime

@Data
@Entity
@Table(name = "bees_requests")
data class BeesRequestsEntity(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: String? = null,

    @Column(name = "trace_id", nullable = false)
    val trace_id: String,

    @Column(name = "vendor", nullable = false)
    val vendor: String,

    @Column(name = "topic", nullable = false)
    val topic: String,

    @Column(name = "marketplace", nullable = false)
    val marketplace: String,

    @Type(JsonType::class)
    @Column(name = "marketplace_meta", nullable = false, columnDefinition = "jsonb")
    val marketplace_meta: Map<String, Any>,

    @Type(JsonType::class)
    @Column(name = "payload", nullable = false, columnDefinition = "jsonb")
    val payload: Map<String, Any>,

    @Type(JsonType::class)
    @Column(name = "origin_data", nullable = false, columnDefinition = "jsonb")
    val origin_data: Map<String, Any>,

    @Column(name = "created_at", nullable = false)
    val created_at: LocalDateTime = LocalDateTime.now(),

    @Column(name = "sent", nullable = false)
    var sent: Boolean = false,

    @Column(name = "send_at")
    var send_at: LocalDateTime? = null,

    @Type(JsonType::class)
    @Column(name = "send_response", columnDefinition = "jsonb")
    var send_response: Map<String, Any>? = null,

    @Column(name = "send_error")
    var send_error: String? = null,

    @Column(name = "processed", nullable = false)
    val processed: Boolean = false,

    @Column(name = "processed_at")
    val processed_at: LocalDateTime? = null,

    @Type(JsonType::class)
    @Column(name = "processed_response", columnDefinition = "jsonb")
    val processed_response: Map<String, Any>? = null,

    @Column(name = "processed_error")
    val processed_error: String? = null
) {
    // Construtor padrão necessário para o Hibernate
    constructor() : this(
        id = null,
        trace_id = "",
        vendor = "",
        topic = "",
        marketplace = "",
        marketplace_meta = emptyMap(),
        payload = emptyMap(),
        origin_data = emptyMap(),
        created_at = LocalDateTime.now()
    )
}