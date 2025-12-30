package com.nttdata.synkrono.controller.dto

class RequestBodyDTO {
    lateinit var traceid: String
    lateinit var vendor: String
    lateinit var topic: String
    lateinit var marketplace: String
    lateinit var marketplace_meta: MarketplaceMetaDTO
    lateinit var payload: Map<String, Any>
    lateinit var origin_data: Map<String, Any>

    fun getSerializedBody(): String {
        var content = HashMap<String, Any>()
        content.put("traceid", this.traceid)
        content.put("vendor", this.vendor)
        content.put("topic", this.topic)
        content.put("marketplace", this.marketplace)
        content.put("marketplace_meta", this.marketplace_meta.toStringJSON())
        content.put("payload", this.payload)
        content.put("origin_data", this.origin_data)

        return content.toString()
    }
}