import openpyxl
import datetime
import os

class ExcelExportPipeline:
    def open_spider(self, spider):
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "Resultados"
        self.sheet.append(["Termo", "Estado", "Cidade", "Bairro", "Nome", "Endereço", "Telefone", "Website"])
        
         # Cria o caminho absoluto baseado no local da pipeline.py
        self.results_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        )
        os.makedirs(self.results_folder, exist_ok=True)

    def process_item(self, item, spider):
        self.sheet.append([
            item['termo_busca'],
            item['estado'],
            item['cidade'],
            item['bairro'],
            item['nome'],
            item['endereco'],
            item['telefone'],
            item['website']
        ])
        return item

    def close_spider(self, spider):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.results_folder, f"leads_{timestamp}.xlsx")
        self.workbook.save(filepath)
