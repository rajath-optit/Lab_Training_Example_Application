package in.optit.optitlabservice;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class HomeController {
	private static final Logger log = LoggerFactory.getLogger(HomeController.class);

	@GetMapping("/")
	public String getGreeting() {
		log.info("Greetings from Opt IT Lab Sample Application");
		// log.error("Error level log");
    		// log.warn("Warn level log");
    		// log.info("Info level log");
    		// log.debug("Debug level log");
    		// log.trace("Trace level log");
		
		return "Welcome to the Opt IT Lab Sample Application!";
	}

	@GetMapping("/_status/healthz")
	public String getHealth() {
		return "OK";
	}

}
