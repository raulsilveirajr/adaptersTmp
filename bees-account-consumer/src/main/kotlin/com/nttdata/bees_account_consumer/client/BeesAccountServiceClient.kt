package com.nttdata.bees_account_consumer.client

import org.springframework.cloud.openfeign.FeignClient
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
//import kotlin.reflect.full.declaredMemberFunctions
//import kotlin.reflect.full.declaredMemberProperties

@FeignClient(
     name = "beesAccountService",
     url = "\${bees.endpoints.accounts.url}"
)
interface BeesAccountServiceClient {

     @PostMapping("/anything")
     fun sendAccount(@RequestBody payload: String): ResponseEntity<String>
}
