import requests
import csv


def json_request(url):
    """
    Make json request.

    :param url: url
    :return:
    """
    res = requests.get(url)
    return res.json()


def save_data_to_excel(data):
    """
    Save all data to excel file.

    :param data: extracted data.
    :return:
    """
    with open('data.csv', 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def run(url):
    """
    Main loop for data extraction

    :param url:
    :return:
    """
    result = []
    json = json_request(url)['value']
    for el in json:
        temp = [
            el['ID'],
            el['Editor']['DisplayName'],
            el['Solicitante']['DisplayName'],
            el['Top_x0020_10_x0020_YEAR'],
            el['Information'],
            el['Local2'],
            el['MD_x0020_Agenda'],
            el['Start'],
            el['End'],
            el['Solicitante']['Email'],
            el['Modified'],
            el['Cluster']['Value'],
            el['Time']['Value'],
            el['Cultura']['Value'],
            el['TipoEvento']['Value'],
            el['ParticipantsRequired'],
            el['ParticipantsOptional']
        ]
        result.append(temp)
    return result


if __name__ == '__main__':
    url = "https://prod-150.westeurope.logic.azure.com/workflows" \
          "/178c85d7ab2e4cf4b58f7d2361846a46/triggers/manual/paths/" \
          "invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual" \
          "%2Frun&sv=1.0&sig=9a_io37CliRJrreYMM_2Sx1Au5gg73DbP3Q_vuvcRLs"
    save_data_to_excel(run(url))
