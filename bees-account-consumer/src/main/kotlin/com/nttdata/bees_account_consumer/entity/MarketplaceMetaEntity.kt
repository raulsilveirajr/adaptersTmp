package com.nttdata.bees_account_consumer.entity

import jakarta.persistence.Id
import jakarta.persistence.MappedSuperclass
import lombok.Data

@Data
@MappedSuperclass
data class MarketplaceMetaEntity(
    @Id
    var id: String,
    var name: String,
    var version: String
) {
    fun toJson(): String {
        return "{\"id\":\"$id\",\"name\":\"$name\",\"version\":\"$version\"}"
    }
}
