import logging
import logging.config
import warnings

from optiface import ui

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_logging():
    ui.header("This is a header")
    ui.subheader("This is a subheader")
    # ui.special("This is a special message")
    ui.body("This is a body message")
    logger.info("diagnostic info for developer or implementer.")
    logger.debug("diagnostic debug for developer or implementer.")
    logger.warning("warning we can't do anything about but should be noted.")
    # warnings.warn("avoidable warning that we can do something about.")


if __name__ == "__main__":
    test_logging()
