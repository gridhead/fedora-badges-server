import logging

logging.basicConfig(
    format="[FMTS] %(asctime)s [%(levelname)s] %(message)s",
    datefmt="[%Y-%m-%d %I:%M:%S %z]",
    level=logging.INFO,
)

logrobjc = logging.getLogger(__name__)
