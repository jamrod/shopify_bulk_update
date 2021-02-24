import requests
import json

from secrets import USER, PASSWORD, SHOP

base_url = f"https://{USER}:{PASSWORD}@{SHOP}.myshopify.com/admin/api/2021-01/"


def get_collections():
    url = f"{base_url}custom_collections.json"
    response = requests.get(
        url
    )
    return response.json()


def get_collection_products(id):
    url = f"{base_url}collections/{id}/products.json?limit=250"
    response = requests.get(
        url
    )
    return response.json()


def get_smart_collections():
    url = f"{base_url}smart_collections.json"
    response = requests.get(
        url
    )
    return response.json()


def get_product(id):
    url = f"{base_url}products/{id}.json"
    response = requests.get(
        url
    )
    return response.json()


def get_allvariants(id):
    url = f"{base_url}products/id/variants.json"
    response = requests.get(
        url
    )
    return response.json()


def get_a_variant(id):
    url = f"{base_url}variants/{id}.json"
    response = requests.get(
        url
    )
    return response.json()


def delete_variant(product_id, variant_id):
    url = f"{base_url}products/{product_id}/variants/{variant_id}.json"
    response = requests.delete(
        url
    )
    return response.json()


def update_product(id, new_data):
    url = f"{base_url}products/{id}.json"
    response = requests.put(
        url,
        data=new_data,
        headers={"Content-Type": "application/json"}
    )
    return response.json()
