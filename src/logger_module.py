import logging
import os 
class Logger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)

        self.system_log_path = os.path.join(log_dir, "system.log")
        self.traffic_log_path = os.path.join(log_dir, "traffic.log")

        self.system_logger = logging.getLogger("SystemLogger")
        self.system_logger.setLevel(logging.DEBUG)  
        system_handler = logging.FileHandler(self.system_log_path)
        system_handler.setLevel(logging.INFO)  
        system_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
        system_handler.setFormatter(system_formatter)
        self.system_logger.addHandler(system_handler)

        self.traffic_logger = logging.getLogger("TrafficLogger")
        self.traffic_logger.setLevel(logging.DEBUG) 
        traffic_handler = logging.FileHandler(self.traffic_log_path)
        traffic_handler.setLevel(logging.INFO)  
        traffic_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
        traffic_handler.setFormatter(traffic_formatter)
        self.traffic_logger.addHandler(traffic_handler)

    def log_system_info(self, message):
        self.system_logger.info(message)

    def log_system_debug(self, message):
        self.system_logger.debug(message)

    def log_traffic_info(self, message):
        self.traffic_logger.info(message)

    def log_traffic_debug(self, message):
        self.traffic_logger.debug(message)

#if __name__ == "__main__":
#    logger = Logger()
#    logger.log_system_info("This is a system info log.")
#    logger.log_system_debug("This is a system debug log.")
#    logger.log_traffic_info("This is a traffic info log.")
#    logger.log_traffic_debug("This is a traffic debug log.")
