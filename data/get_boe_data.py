import requests
from bs4 import BeautifulSoup
import xmltodict
import yaml

def download_pdf(url, id):
    file_path = f"C:/Users/2373225/projects/genai-1/data/pdfs/{id}.pdf"
    response = requests.get(url=url, stream=True)

    with open(file_path, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            pdf_file.write(chunk)

url = "https://www.boe.es/datosabiertos/api/boe/sumario/20240101"

headers = {"Accept": "application/xml"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data_dict = xmltodict.parse(response.content)

    sumario = data_dict["response"]["data"]["sumario"]
    print(sumario["diario"]["sumario_diario"])
    for seccion in data_dict["response"]["data"]["sumario"]["diario"]["seccion"]:
        for departamento in seccion["departamento"]:
            if type(departamento["epigrafe"]) == dict:
                if type(departamento["epigrafe"]["item"]) == list:
                    for item in departamento["epigrafe"]["item"]:
                        id = item["identificador"]
                        url_pdf = item["url_pdf"]["#text"]
                        print(id)
                        print(seccion["@nombre"])
                        print(departamento["@nombre"])
                        print(departamento["epigrafe"]["@nombre"])
                        #download_pdf(url=url_pdf, id=id)
                else:
                    id = departamento["epigrafe"]["item"]["identificador"]
                    url_pdf = departamento["epigrafe"]["item"]["url_pdf"]["#text"]
                    print(id)
                    print(seccion["@nombre"])
                    print(departamento["@nombre"])
                    print(departamento["epigrafe"]["@nombre"])
                    #download_pdf(url=url_pdf, id=id)
            else:
                for epigraf in departamento["epigrafe"]:
                    if type(epigraf["item"]) == list:
                        for item in epigraf["item"]:
                            id = item["identificador"]
                            url_pdf = item["url_pdf"]["#text"]
                            print(id)
                            print(seccion["@nombre"])
                            print(departamento["@nombre"])
                            print(epigraf["@nombre"])
                            #download_pdf(url=url_pdf, id=id)
                    else:
                        id = epigraf["item"]["identificador"]
                        url_pdf = epigraf["item"]["url_pdf"]["#text"]
                        print(id)
                        print(seccion["@nombre"])
                        print(departamento["@nombre"])
                        print(epigraf["@nombre"])
                        #download_pdf(url=url_pdf, id=id)



