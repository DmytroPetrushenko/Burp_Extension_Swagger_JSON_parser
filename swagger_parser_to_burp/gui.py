from javax.swing import JPanel, JButton, JLabel, SwingConstants, JTextField, JTextArea
from java.awt import BorderLayout, GridLayout
from burp import ITab
from api_to_swagger import get_swagger_json


class BurpGui(ITab):

    def __init__(self, burp_extender_object):
        self.burp_extender_object = burp_extender_object
        self.panel = JPanel()
        self.apply_button = JButton('Apply', actionPerformed=self.load_site_map)
        self.url_field = JTextField('', 30)
        self.url_label = JLabel("Enter the url of swagger:", SwingConstants.RIGHT)
        self.panel.add(self.url_label)
        self.panel.add(self.url_field)
        self.panel.add(self.apply_button)

    def getTabCaption(self):
        return "Swagger to SiteMap"

    def getUiComponent(self):
        return self.panel

    def load_site_map(self, event):
        url_value = self.url_field.text
        swagger_dict = get_swagger_json(url_value)
        self.burp_extender_object.create_site_map(swagger_dict)
