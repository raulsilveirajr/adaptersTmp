package com.nttdata.bees_account_consumer

import com.nttdata.bees_account_consumer.consumer.BeesAccountConsumer
import jakarta.annotation.PostConstruct
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.autoconfigure.domain.EntityScan
import org.springframework.boot.runApplication
import org.springframework.cloud.openfeign.EnableFeignClients
import org.springframework.context.annotation.ComponentScan
import org.springframework.data.jpa.repository.config.EnableJpaRepositories

@SpringBootApplication
@EnableFeignClients(basePackages = ["com.nttdata.bees_account_consumer.client"])
@ComponentScan(basePackages = ["com.nttdata.bees_account_consumer"])
@EntityScan(basePackages = [
	"com.nttdata.bees_account_consumer.entity",
	"com.nttdata.bees_account_consumer.client"
])
@EnableJpaRepositories(basePackages = ["com.nttdata.bees_account_consumer.repository"])
class BeesAccountConsumerApplication {

	@Autowired
	private lateinit var beesAccountConsumer: BeesAccountConsumer

	@Value("\${environment.name}")
	private lateinit var currentEnvironment: String

	@Value("\${server.port}")
	private lateinit var serverPort: String

	@Value("\${bees.endpoints.accounts.url}")
	private lateinit var feignClientUrl: String

	@PostConstruct
	fun init() {
		println("PORTA: $serverPort")
		println("Feign Client URL: $feignClientUrl")

		if (currentEnvironment == "development") {
			beesAccountConsumer.emulateMessages()
			System.exit(0)
		}
	}
}

fun main(args: Array<String>) {
	runApplication<BeesAccountConsumerApplication>(*args)
}
