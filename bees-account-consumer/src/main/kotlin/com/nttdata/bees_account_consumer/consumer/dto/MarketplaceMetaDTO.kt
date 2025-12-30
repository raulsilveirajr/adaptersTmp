package com.nttdata.bees_account_consumer.consumer.dto

import com.nttdata.bees_account_consumer.entity.MarketplaceMetaEntity
import lombok.ToString

@ToString
class MarketplaceMetaDTO {
    lateinit var id: String
    lateinit var name: String
    lateinit var version: String

    override fun toString(): String {
        return "MarketplaceMetaDTO(id='$id', name='$name', version='$version')"
    }

    fun toMap(): Map<String, Any> {
        return mapOf(
            "id" to id,
            "name" to name,
            "version" to version
        )
    }
}
