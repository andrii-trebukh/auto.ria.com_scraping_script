from pathlib import Path


BASE_URL = "https://auto.ria.com"
START_URL = "/search/?indexName=auto,order_auto,newauto_search&plateNumber.length.gte=1&categories.main.id=1&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=10"
SCRAP_PAGES = 2  # will stop after scrapping n pages
DIR_PATH = Path("raw_dataset")
PHOTO_PATH = DIR_PATH.joinpath("photos")
PLATE_PATH = DIR_PATH.joinpath("plates")
ANNOTATION_PATH = DIR_PATH.joinpath("annotations")
ANNOTATION_FORMAT = "xml"  # "json" | "xml" | None
