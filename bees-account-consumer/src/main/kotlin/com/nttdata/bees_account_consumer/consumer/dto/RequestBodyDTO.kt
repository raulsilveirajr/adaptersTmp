package com.nttdata.bees_account_consumer.consumer.dto

import com.google.gson.Gson
import com.nttdata.bees_account_consumer.entity.BeesRequestsEntity
import org.slf4j.LoggerFactory
import java.time.LocalDateTime

val mandatoryFields = listOf<String>(
    "vendorAccountId",
    "displayName",
    "legalName",
    "billingAddress?.address",
    "billingAddress?.city",
    "billingAddress?.latitude",
    "billingAddress?.longitude",
    "billingAddress?.state",
    "billingAddress?.zipcode",
    "contacts",
    "contacts.type",
    "contacts.value",
    "deliveryAddress",
    "deliveryAddress.address",
    "deliveryAddress.city",
    "deliveryAddress.latitude",
    "deliveryAddress.longitude",
    "deliveryAddress.state",
    "deliveryAddress.zipcode",
    "liquorLicense?.expirationDate",
    "owner",
    "owner.email",
    "owner.firstName",
    "owner.lastName",
    "owner.phone",
    "paymentTerms?.termPeriods",
    "paymentTerms?.termPeriods.days",
    "paymentTerms?.type",
//    "representatives?.email",
//    "representatives?.role",
//    "representatives?.supervisor",
//    "representatives?.supervisor.phone",
    "segment",
    "status",
    "taxId",
    "taxIds?.type",
    "taxIds?.value"
)

data class RequestBodyDTO(
    var traceid: String = "",
    var vendor: String = "",
    var topic: String = "",
    var marketplace: String = "",
    var marketplace_meta: MarketplaceMetaDTO,
    var payload: Map<String, Any> = emptyMap(),
    var origin_data: Map<String, Any> = emptyMap(),
    @Transient var created_at: LocalDateTime = LocalDateTime.now(),
    @Transient var sent: Boolean = false,
    @Transient var send_at: LocalDateTime? = null,
    @Transient var send_response: Map<String, Any>? = null,
    @Transient var send_error: String? = null,
    @Transient var processed: Boolean = false,
    @Transient var processed_at: LocalDateTime? = null,
    @Transient var processed_response: Map<String, Any>? = null,
    @Transient var processed_error: String? = null
) {

    fun toEntity(): BeesRequestsEntity {
        return BeesRequestsEntity(
            trace_id = this.traceid,
            vendor = this.vendor,
            topic = this.topic,
            marketplace = this.marketplace,
            marketplace_meta = this.marketplace_meta.toMap(),
            payload = this.payload,
            origin_data = this.origin_data,
            created_at = this.created_at ?: LocalDateTime.now(),
            sent = this.sent,
            send_at = this.send_at,
            send_response = this.send_response,
            send_error = this.send_error,
            processed = this.processed,
            processed_at = this.processed_at,
            processed_response = this.processed_response,
            processed_error = this.processed_error
        )
    }

    fun validatePayload() : List<String> {
        val payloadErrors = MutableList(0) { "" }

        if (this.payload.isEmpty()) {
            payloadErrors.add("Payload empty.")
        }

        payloadErrors.addAll(validatePayloadRecursively())

        return payloadErrors
    }

    private fun validatePayloadRecursively(): List<String> {
        val payloadErrors = mutableListOf<String>()

        fun checkField(keys: List<String>, map: Map<String, Any?>): Boolean {
            if (keys.isEmpty()) return true
            val mandatoryObject = !keys[0].endsWith("?")
            val key = keys[0].removeSuffix("?")
            val value = map[key] ?: return !mandatoryObject
            return if (keys.size == 1) {
                true
            } else {
                if (value is Map<*, *>) {
                    checkField(keys.drop(1), value as Map<String, Any?>)
                } else {
                    false
                }
            }
        }

        for (field in mandatoryFields) {
            val keys = field.split(".")
            if (!checkField(keys, this.payload)) {
                payloadErrors.add("Attribute $field is required.")
            }
        }

        return payloadErrors
    }

    companion object {
        @JvmStatic
        fun jSONStringToRequestBodyDTO(rawString: String) : RequestBodyDTO {
            val logger = LoggerFactory.getLogger(Companion::class.java)

            logger.debug("jSONStringToRequestBodyDTO - rawString: $rawString")
            val jsonString = rawString
                .replace("=", ":")
                .replace("'", "\"")
                .replace("\\s+".toRegex(), " ")
                .replace(": ", ":")
                .replace(", ", ",")
                .replace(":[", ": [")
                .replace("\"[", "[")
                .replace("]\"", "]")
                .replace(": {", ": {")
                .replace("\"{", "{")
                .replace("}\"", "}")
            logger.debug("jSONStringToRequestBodyDTO - jsonString: $jsonString")

            try {
                // Convert the adjusted string to JSON object
                val gson = Gson()

                return gson.fromJson(jsonString, RequestBodyDTO::class.java)
            } catch (e: Exception) {
                // TODO: logger.error("Erro ao converter string para JSON: ${e.message}")
                println("Erro ao converter string para JSON após 2 tentativas: ${e.message}")
                throw RuntimeException("Erro ao converter string para JSON após 2 tentativas: ${e.message}")
            }
        }
    }
}