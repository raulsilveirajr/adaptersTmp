package com.nttdata.synkrono.controller.dto

import lombok.ToString

@ToString
class MarketplaceMetaDTO {
    lateinit var id: String
    lateinit var name: String
    lateinit var version: String

    override fun toString(): String {
        return "MarketplaceMetaDTO(id='$id', name='$name', version='$version')"
    }

    fun toStringJSON(): Any {
        return "{id='$id', name='$name', version='$version'}"
    }
}
