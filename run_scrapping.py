from pathlib import Path
import json
import time
from xml.dom.minidom import parseString
from urllib.request import urlretrieve
from dicttoxml import dicttoxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

from settings import BASE_URL, START_URL, SCRAP_PAGES, PHOTO_PATH, \
    PLATE_PATH, ANNOTATION_PATH, ANNOTATION_FORMAT
from recognize_module import recognizer


def mk_annotation(filename, img_size, box, save_json=True):

    xmin, ymin, xmax, ymax = box

    annotation = {
        "annotation": {
            "filename": filename,
            "size": {
                "width": img_size[0],
                "height": img_size[1],
                "depth": 3
            },
            "object": {
                "name": "License_Plate",
                "bndbox": {
                    "xmin": int(xmin),
                    "xmax": int(xmax),
                    "ymin": int(ymin),
                    "ymax": int(ymax)
                }
            }
        }
    }

    if save_json:
        file_path = Path(ANNOTATION_PATH).joinpath(
            f"{filename.split(".jpg")[0]}.json"
        )
        with open(file_path, "w", encoding="utf8") as file:
            json.dump(annotation, file, indent=4)
    else:
        file_path = Path(ANNOTATION_PATH).joinpath(
            f"{filename.split(".jpg")[0]}.xml"
        )
        annotation_xml = dicttoxml(
            annotation,
            xml_declaration=False,
            root=False,
            return_bytes=False,
            attr_type=False
        )
        annotation_xml = parseString(annotation_xml).toprettyxml()

        with open(file_path, "w", encoding="utf8") as file:
            file.write(annotation_xml)


def get_imgs(url: str, plate_no: str) -> None:
    response = requests.get(url, timeout=10)
    img_soup = BeautifulSoup(response.text, "lxml")
    imgs_urls = [
        img["src"] for img in img_soup.find_all("img", class_="m-auto")
    ]

    name_index = 0
    for img_url in imgs_urls:
        img = Image.open(requests.get(img_url, stream=True, timeout=10).raw)
        _, plate, box = recognizer.recognize_plate(img)

        # if no plate recognized proceed next photo
        if plate is None:
            continue

        # save original photo
        img_name = f"{plate_no} {name_index:0>3}.jpg"
        urlretrieve(img_url, PHOTO_PATH.joinpath(img_name))

        # save plate
        plate.save(PLATE_PATH.joinpath(f"{plate_no} {name_index:0>3}.png"))

        # make annotation
        if ANNOTATION_FORMAT is not None:
            mk_annotation(
                img_name,
                img.size,
                box,
                ANNOTATION_FORMAT == "json"
            )

        name_index += 1


def main():
    url = START_URL
    # Javascript rendering needed for pagination, so using Selenium
    for _ in range(SCRAP_PAGES):
        driver = webdriver.Firefox()
        driver.get(BASE_URL + url)
        time.sleep(5)
        html = driver.page_source
        driver.close()

        soup = BeautifulSoup(html, "lxml")

        # find all sections with car's individual page link
        sections = soup.find_all("section", class_="ticket-item")
        for section in sections:

            # extracting plate no.
            num = section.find("span", class_="state-num").text
            extra_text = section.find("span", class_="state-num")\
                .find("span").text
            num = num.replace(extra_text, "").replace(" ", "")

            # url of the car's individual page
            sub_url = section.find("a", class_="address")["href"]

            get_imgs(sub_url, num)

        # next page url
        url = soup.find("a", class_="js-next")["href"]


if __name__ == "__main__":
    main()
