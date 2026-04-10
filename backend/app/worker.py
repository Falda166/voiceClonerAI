import time
import structlog

logger = structlog.get_logger()


def main() -> None:
    logger.info('worker.started')
    while True:
        logger.info('worker.heartbeat')
        time.sleep(30)


if __name__ == '__main__':
    main()
