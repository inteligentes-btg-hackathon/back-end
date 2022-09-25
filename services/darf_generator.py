import pdfkit
import bs4

DARF_TEMPLATE = 'services/assets/darf_template.html'

#total_geral = document.getElementById("total_geral")
#emitido_em = document.getElementById("emitido_em")
#CPF = document.getElementById("CPF")
#codigo = document.getElementById("codigo")
#principal = document.getElementById("principal")


class Template:
    def __init__(self):
        self.template_path = DARF_TEMPLATE
        self.template = None

    def load(self):
        with open(self.template_path, 'r') as f:
            self.template = f.read()

    def update_value_id(self, id, value):
        if (self.template is None):
            self.load()
        soup = bs4.BeautifulSoup(self.template, 'html.parser')
        tag = soup.find(id=id)
        if tag is not None:
            tag.string = value
        self.template = str(soup)

    def render(self, **kwargs):
        if self.template is None:
            self.load()
        return self.template.format(**kwargs)

    def generate_pdf(self, output_path, **kwargs):
        html = self.render(**kwargs)
        pdf = pdfkit.from_string(html, output_path)


if __name__ == "__main__":  # Verify if the script is being executed directly
    template = Template()
    template.update_value_id('total_geral', 'R$ 1.000,00')
    template.update_value_id('emitido_em', '01/01/2020')
    template.update_value_id('CPF', '000.000.000-00')
    template.update_value_id('codigo', '001')
    pdf = template.generate_pdf('darf_temp.pdf')
