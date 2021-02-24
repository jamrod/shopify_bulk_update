import json
from api_calls import *
import csv
from text_change import NEWTEXT, OLDTEXT

# with open("data/Yerba_Santa_Copy.json", "w") as write_file:
#     data = get_product(4555060707426)
#     if "errors" in data:
#         print("Errors: ", data.get("errors"))
#     json.dump(data, write_file)


def get_products_csv(collection):
    data = get_collection_products(collection)
    if "errors" in data:
        print("Errors: ", data.get("errors"))
    with open("data/bulk_herbs.csv", "w") as write_file:
        count = 0
        herbs = data.get("products")
        file_writer = csv.writer(write_file)
        file_writer.writerow(['Herb Name', 'id'])
        for herb in herbs:
            count = count + 1
            name = herb.get('title')
            herb_id = herb.get('id')
            file_writer.writerow([name, herb_id])
        print("Products downloaded = ", count)


# get_products_csv(229315909)

def get_ids_from_csv(file):
    id_list = []
    with open(file, "r") as read_csv:
        csv_dict = csv.DictReader(read_csv)
        for row in csv_dict:
            id_list.append(row["id"])
    return(id_list)


# print(get_ids_from_csv("data/bulk_herbs.csv"))

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
        price = float(keep_variant.get("price")) / 28.3495
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


# print(update_product_for_grams(4555060707426))


def check_text():
    count = 0
    missing = []
    with open("data/products_bulk_herbs.json", "r") as read_file:
        data = json.load(read_file)
        herbs = data.get("products")
        for herb in herbs:
            body = herb.get("body_html")
            found = False
            for line in body.splitlines():
                if OLDTEXT in line:
                    count = count + 1
                    found = True
            if not found:
                missing.append(herb.get("title"))
    print(missing)
    return count


# print(check_text())

def process_bulk_herbs_for_grams_update():
    with open("data/bulk_herbs.csv") as csv_file:
        csv_data = csv.DictReader(csv_file)
        for herb in csv_data:
            success = update_product_for_grams(herb["id"])
            if success:
                name = herb["name"]
                print(f"{name} updated successfully!")


# process_bulk_herbs_for_grams_update()

def save_collection_to_file(id, fp):
    with open(fp, "w") as write_file:
        data = get_collection_products(id)
        if "errors" in data:
            print("Errors: ", data.get("errors"))
            return False
        json.dump(data, write_file)
        return True


print(save_collection_to_file(229315909, "data/products_bulk_herbs.json"))
