import json
from api_calls import get_product, delete_variant, update_product
import csv
from text_change import NEWTEXT, OLDTEXT


def update_product_for_grams(id):
    data = get_product(id)
    product = data.get("product")
    title = product.get("title")
    variants = product.get("variants")
    keep_variant = {}
    delete_variants = []
    found_variant = False

    for variant in variants:
        variant_title = variant.get("title")
        if "1 oz net" in variant_title and "0.1" not in variant_title:
            keep_variant = variant
            found_variant = True
        else:
            delete_variants.append(variant.get("id"))
    if found_variant:
        keep_variant["title"] = "1 gram"
        keep_variant["option1"] = "1 gram"
        price = float(keep_variant.get("price")) / 28
        price = "{:.2f}".format(price)
        keep_variant["price"] = price
        keep_variant["weight_unit"] = "g"
        keep_variant["grams"] = 1
        keep_variant["weight"] = 1
        for variant_id in delete_variants:
            response = delete_variant(id, variant_id)
            if "errors" in response:
                print(
                    f"error on variant_delete for {title} : {variant_id} : ", response.get("errors"))
    else:
        keep_variant = variants
        print(f"Variants not altered for {title}")
    body = product.get("body_html")
    result = process_text(body)
    if result[1]:
        print(f"error on process_text for {title}")
    new_text = result[0]
    updates = {
        "product": {
            "id": id,
            "body_html": new_text,
            "template_suffix": "bulk-herb",
            "variants": [
                keep_variant
            ]
        }
    }
    response = update_product(id, json.dumps(updates))
    if "errors" in response:
        print(response.get("errors"))
        return False
    return True


def process_text(body):
    new_text = ""
    not_found = True
    for line in body.splitlines():
        if OLDTEXT in line:
            new_text += NEWTEXT
            not_found = False
        else:
            new_text += line
    return new_text, not_found


def process_bulk_herbs_for_grams_update():
    with open("data/bulk_herbs_round_2.csv") as csv_file:
        csv_data = csv.DictReader(csv_file)
        for herb in csv_data:
            name = herb["name"]
            success = update_product_for_grams(herb["id"])
            if success:
                print(f"{name} updated successfully!")


if __name__ == "__main__":
    process_bulk_herbs_for_grams_update()
