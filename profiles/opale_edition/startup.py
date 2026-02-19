# standard
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from getpass import getuser
from socket import gethostname

# PyQGIS
try:
    from qgis.core import QgsApplication
    from qgis.utils import plugin_times

    IS_PYQGIS_LOADED: bool = True
except ImportError as err:
    logging.error(f"QGIS and its API are not available. Trace: {err}")
    IS_PYQGIS_LOADED: bool = False

# -- GLOBALS
log_filepath = (
    Path.home() / f".qgis/monitoring/qgis_launches_{gethostname()}_{getuser()}.log"
)
log_filepath.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        TimedRotatingFileHandler(
            filename=log_filepath,
            when="D",
            interval=1,
            backupCount=5,
        )
    ],
)

# -- EXécution
logging.info("-" * 80)
logging.info("QGIS Started")

if IS_PYQGIS_LOADED:
    profile_path: Path = Path(QgsApplication.qgisSettingsDirPath())
    logging.info(f"Profile: {profile_path.name}")
    # par contre, impossible d'obtenir le temps de chargement des plugins
    # car ils sont chargés après l'exécution du script startup dans
    # la séquence de démarrage
    for k, v in plugin_times.items():
        logging.info(f"Plugin: {k} - Load time: {v:.3f} seconds")