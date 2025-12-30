package com.nttdata.bees_account_consumer.service

import com.google.gson.GsonBuilder
import com.google.gson.internal.LinkedTreeMap
import com.nttdata.bees_account_consumer.client.BeesAccountServiceClient
import com.nttdata.bees_account_consumer.consumer.dto.RequestBodyDTO
import com.nttdata.bees_account_consumer.repository.BeesRequestsRepository
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Service
import java.time.LocalDateTime

@Service
class BeesAccountService(
    private val beesRequestsRepository: BeesRequestsRepository
    ,private val beesAccountServiceClient: BeesAccountServiceClient
) {
    private val logger = LoggerFactory.getLogger(this.javaClass)

    @Value("\${environment.name}")
    private lateinit var currentEnvironment: String

    private lateinit var requestBodyDTO : RequestBodyDTO

    fun processMessage(message: String) {
        this.requestBodyDTO = RequestBodyDTO.jSONStringToRequestBodyDTO(message)
        logger.info("Processing message: ${requestBodyDTO.traceid}")
        logger.debug("Full message: $message")

        logger.info("Saving request message: ${requestBodyDTO.traceid}")
        var savedRequest = beesRequestsRepository.save(requestBodyDTO.toEntity())

        logger.info("Validating payload: ${requestBodyDTO.traceid}")
        requestBodyDTO.validatePayload().let {
            if (it.isNotEmpty()) {
                logger.error("Payload validation failed: ${it}")
                //TODO: Implementar o retorno de erro
                return
            }
        }

        logger.info("Verifying contact data: ${requestBodyDTO.traceid}")
        this.adjustEmailValueForNonProdEnviroments()

        var response : ResponseEntity<String>? = null

        try {
            logger.info("Sending data to Bees Accounts Service: ${requestBodyDTO.traceid}")

            logger.debug("Payload: ${requestBodyDTO.payload.toString()}")
            val gson = GsonBuilder().setPrettyPrinting().create()
            val formattedPayload = gson.toJson(requestBodyDTO.payload)
            logger.debug("Payload: ${formattedPayload}")

            response = beesAccountServiceClient.sendAccount(requestBodyDTO.payload.toString())
            logger.debug("Response: ${response.body}")

            updateRequestsWithResultsOfDataSendRequest(response, savedRequest.id ?: "")
        } catch (e: Exception) {
            logger.error("Error sending request to Bees Account Service: ${requestBodyDTO.traceid} - ${e.message}")
        }

        println("Response StatusCode: ${response?.statusCode}")
        println("=======================")
    }

    private fun updateRequestsWithResultsOfDataSendRequest(response: ResponseEntity<String>, id: String) {
        try {
            logger.info("Saving results of data send request: ${requestBodyDTO.traceid}")

            beesRequestsRepository.findById(id).ifPresent { entity ->
                entity.sent = response.statusCode.is2xxSuccessful
                entity.send_at = LocalDateTime.now()
                entity.send_response = response.body?.let {
                    GsonBuilder().setPrettyPrinting().create().fromJson(it, Map::class.java)
                } as Map<String, Any>? ?: emptyMap()
                if (!entity.sent)
                    entity.send_error = response.body
                beesRequestsRepository.save(entity)
                logger.info("Results of data send request saved: ${requestBodyDTO.traceid}")
            }
        } catch (e: Exception) {
            logger.error("Error saving results of data send request: ${requestBodyDTO.traceid} - ${e.message}")
        }
    }

    fun adjustEmailValueForNonProdEnviroments() {
        val currentOwner = this.requestBodyDTO.payload["owner"] as? LinkedTreeMap<String, String>
        currentOwner?.let {
            it["original_email"] = it["email"]
            if (currentEnvironment != "PROD") {
                it["email"] = "test@bees.com"
            }
        }
    }

    fun createJsonFromPayload() {
        val payload = this.requestBodyDTO.payload
        val jsonPayload = payload.toString()
    }

}

/*

- Os erros do serviço da Bees retornam 200 e
    temos que avaliar pelo "monitor" do bees pq pode demorar para processar

*/