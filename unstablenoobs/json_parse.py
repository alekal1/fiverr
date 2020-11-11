import requests
import json
import csv

URL = 'https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo'
DATA = []

def main():
    json_objects = get_json_from_url(URL)
    for object in json_objects:
        json_entry = json_objects[object]
        temp = [
            json_entry['id'],
            handle_publicKey_type(json_entry),
            handle_publicKey_owner(json_entry),
            handle_authentication_type(json_entry),
            handle_authentication_publicKey(json_entry),
            handle_service_metadata(json_entry)[0],
            handle_service_metadata(json_entry)[1],
            handle_service_metadata(json_entry)[2],
            handle_service_metadata(json_entry)[3],
            handle_service_metadata(json_entry)[4],
            handle_service_metadata(json_entry)[5],
            handle_service_metadata(json_entry)[6],
            handle_service_metadata(json_entry)[7],
            handle_service_metadata(json_entry)[8],
            handle_service_metadata(json_entry)[9],
            handle_service_metadata(json_entry)[10],
            handle_service_metadata(json_entry)[11],
            handle_service_metadata(json_entry)[12],
            handle_service_metadata(json_entry)[13],
            handle_service_metadata(json_entry)[14],
            handle_service_metadata(json_entry)[15],
            handle_service_metadata(json_entry)[16],
            handle_service_metadata(json_entry)[17],
            handle_service_metadata(json_entry)[18],
            handle_service_metadata(json_entry)[19],
            handle_service_metadata(json_entry)[20],
            # TODO SERVICE,
            json_entry['dataToken'],
            json_entry['created'],
            json_entry['proof']['created'],
            json_entry['proof']['creator'],
            json_entry['proof']['type'],
            json_entry['proof']['signatureValue'],
            json_entry['dataTokenInfo']['address'],
            json_entry['dataTokenInfo']['name'],
            json_entry['dataTokenInfo']['symbol'],
            json_entry['dataTokenInfo']['decimals'],
            json_entry['dataTokenInfo']['totalSupply'],
            json_entry['dataTokenInfo']['cap'],
            json_entry['dataTokenInfo']['minter'],
            json_entry['dataTokenInfo']['minterBalance'],
            json_entry['updated'],
            json_entry['price']['datatoken'],
            json_entry['price']['ocean'],
            json_entry['price']['value'],
            json_entry['price']['type'],
            json_entry['price']['address'],
            json_entry['price']['address'],
            handle_price_tools(json_entry),
        ]
        DATA.append(temp)
        print(len(json_entry['service']))


def handle_publicKey_type(json_entry):
    string_to_return = ""
    for el in json_entry['publicKey']:
        string_to_return = string_to_return + f' {el["type"]}'
    return string_to_return


def handle_publicKey_owner(json_entry):
    string_to_return = ""
    for el in json_entry['publicKey']:
        string_to_return = string_to_return + f' {el["owner"]}'
    return string_to_return


def handle_authentication_type(json_entry):
    string_to_return = ""
    for el in json_entry['authentication']:
        string_to_return = string_to_return + f' {el["type"]}'
    return string_to_return


def handle_authentication_publicKey(json_entry):
    string_to_return = ""
    for el in json_entry['authentication']:
        string_to_return = string_to_return + f' {el["publicKey"]}'
    return string_to_return


def handle_service_metadata(json_entry):
    service_metadata = json_entry['service'][0]
    type = service_metadata['type']
    curation_rating = service_metadata['attributes']['curation']['rating']
    curation_numVotes = service_metadata['attributes']['curation']['numVotes']
    curation_isListed = service_metadata['attributes']['curation']['isListed']
    main_type = service_metadata['attributes']['main']['type']
    main_name = service_metadata['attributes']['main']['name']
    main_dateCreated = service_metadata['attributes']['main']['dateCreated']
    main_author = service_metadata['attributes']['main']['author']
    main_license = service_metadata['attributes']['main']['license']
    try:
        main_files_contentLength = service_metadata['attributes']['main']['files'][0]['contentLength']
    except KeyError:
        main_files_contentLength = 'unknown'
    main_files_contentType = service_metadata['attributes']['main']['files'][0]['contentType']
    main_files_index = service_metadata['attributes']['main']['files'][0]['index']
    main_datePublished = service_metadata['attributes']['main']['datePublished']
    additionalInformation_description = service_metadata['attributes']['additionalInformation']['description']
    tags = ''
    try:
        for elem in service_metadata['attributes']['additionalInformation']['tags']:
            tags = tags + f' {elem}'
    except KeyError:
        pass
    try:
        links_contentLength = service_metadata['attributes']['additionalInformation']['links'][0]['contentLength']
    except KeyError:
        links_contentLength = 'unknown'
    except IndexError:
        links_contentLength = ''
    try:
        links_contentType = service_metadata['attributes']['additionalInformation']['links'][0]['contentType']
    except KeyError:
        links_contentType = 'unknown'
    except IndexError:
        links_contentType = ''
    try:
        links_url = service_metadata['attributes']['additionalInformation']['links'][0]['url']
    except KeyError:
        links_url = 'unknown'
    except IndexError:
        links_url = ''
    termsAndConditions = service_metadata['attributes']['additionalInformation']['termsAndConditions']
    encryptedFiles = service_metadata['attributes']['encryptedFiles']
    index = service_metadata['index']
    return (type, curation_rating, curation_numVotes, curation_isListed, main_type, main_name, main_dateCreated, main_author, main_license, main_files_contentLength, main_files_contentType, main_files_index, main_datePublished, additionalInformation_description, tags, links_contentLength, links_contentType, links_url, termsAndConditions, encryptedFiles, index)


def handle_price_tools(json_entry):
    string_to_return = ""
    for el in json_entry['price']['pools']:
        string_to_return = string_to_return + f' {el}'
    return string_to_return


def get_json_from_url(url):
    r = requests.get(url)
    return r.json()


def save_data_to_excel(data):
    """
    Saves data into csv file.

    :param data: all parsed countries with their airports
    :return:
    """
    with open('data.csv', 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == '__main__':
    main()
    save_data_to_excel(DATA)
