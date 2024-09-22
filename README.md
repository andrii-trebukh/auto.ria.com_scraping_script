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
    python3 run_scrapping
    ```

## Settings

You may adjust numbers of pages to scrap and annotations files output format (json or xml).
settings.py
    ```
    CHANGE ME TO SETTINGS.PY
    ```

## Output data

Structure of scrapping data for each photo:
raw_dataset/photos/"license plate no. 8 characters".jpg – photo of the car
raw_dataset/plates/"license plate no. 8 characters".png – photo of the cropped license plate
raw_dataset/annotations/"license plate no. 8 characters".json – annotation file (json or xml)
