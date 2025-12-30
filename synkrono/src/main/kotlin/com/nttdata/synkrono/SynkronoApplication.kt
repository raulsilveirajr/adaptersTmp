package com.nttdata.synkrono

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class SynkronoApplication

fun main(args: Array<String>) {
	runApplication<SynkronoApplication>(*args)
}
