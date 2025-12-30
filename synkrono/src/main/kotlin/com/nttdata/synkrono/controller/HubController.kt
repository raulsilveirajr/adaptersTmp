package com.nttdata.synkrono.controller

import com.nttdata.synkrono.controller.dto.RequestBodyDTO
import com.nttdata.synkrono.service.KafkaProducerService
import com.nttdata.synkrono.service.Message
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestHeader
import org.springframework.web.bind.annotation.RestController

@RestController
class HubController(private val kafkaProducerService: KafkaProducerService) {

    @PostMapping(path = ["/hub"], consumes = ["application/json"], produces = ["application/json"])
    fun createAccount(
        @RequestHeader("Authorization") autorization: String,
        @RequestHeader("vendor") contentType: String,
        @RequestHeader("vendor-version") vendorVersion: String,
        @RequestBody body: RequestBodyDTO): ResponseEntity<Any>
    {
        kafkaProducerService.sendMessage(
            body.topic,
            Message(
                body.traceid,
                body.getSerializedBody()
            )
        )
        return ResponseEntity.ok("Mensagem enviada para o Kafka")
    }
}