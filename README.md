# Auto.ria.com Scraping script
This script is part of student project https://github.com/Alex-Tsyb/Number_plates_project

The script is aiming to collect dataset for further Neural Network learning. The script picks photos with license plates only.

## Usage

1. Clone the repository:
    ```
    git clone https://github.com/andrii-trebukh/auto.ria.com_scraping_script
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run
    ```
    python3 run_scrapping.py
    ```

## Settings

You may adjust numbers of pages to scrap and annotations files output format (json or xml).

settings.py

    BASE_URL = "https://auto.ria.com"
    START_URL = "/search/?indexName=auto,order_auto,newauto_search&plateNumber.length.gte=1&categories.main.id=1&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=10"
    SCRAP_PAGES = 2  # will stop after scrapping n pages
    DIR_PATH = Path("raw_dataset")
    PHOTO_PATH = DIR_PATH.joinpath("photos")
    PLATE_PATH = DIR_PATH.joinpath("plates")
    ANNOTATION_PATH = DIR_PATH.joinpath("annotations")
    ANNOTATION_FORMAT = "xml"  # "json" | "xml" | None


## Output data

Structure of scrapping data for each photo:

* raw_dataset/photos/"license plate no. 8 characters NNN".jpg – photo of the car
* raw_dataset/plates/"license plate no. 8 characters NNN".png – photo of the cropped license plate
* raw_dataset/annotations/"license plate no. 8 characters NNN".json – annotation file (json or xml)
