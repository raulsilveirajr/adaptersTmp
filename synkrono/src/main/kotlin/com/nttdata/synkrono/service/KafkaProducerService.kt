package com.nttdata.synkrono.service

import lombok.Builder
import org.springframework.kafka.core.KafkaTemplate
import org.springframework.stereotype.Service

@Service
class KafkaProducerService(private val kafkaTemplate: KafkaTemplate<String, String>) {

    fun sendMessage(topic: String, message: Message) {
        kafkaTemplate.send(topic, 0, message.id, message.content)
    }
}

@Builder
data class Message(
    val id: String,
    val content: String
)