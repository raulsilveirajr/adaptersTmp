package com.nttdata.bees_account_consumer.repository

import com.nttdata.bees_account_consumer.entity.BeesRequestsEntity
import org.springframework.data.repository.CrudRepository
import org.springframework.stereotype.Repository

@Repository
interface BeesRequestsRepository : CrudRepository<BeesRequestsEntity, String> {
//    fun findByTrace_id(trace_id: String): BeesRequestsEntity?
}