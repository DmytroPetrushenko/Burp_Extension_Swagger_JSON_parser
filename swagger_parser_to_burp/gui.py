from javax.swing import JPanel, JButton, JLabel, SwingConstants, JTextField, JTextArea, GroupLayout, JScrollPane
from burp import ITab
from api_to_swagger import get_swagger_json


class BurpGui(ITab):

    def __init__(self, burp_extender_object):
        self.burp_extender_object = burp_extender_object
        self.panel = JPanel()
        self.apply_button = JButton('Apply', actionPerformed=self.load_site_map)
        self.url_field = JTextField('https://petstore.swagger.io/v2/swagger.json', 30)
        self.url_label = JLabel("Enter the url of swagger:", SwingConstants.RIGHT)
        self.log_label = JLabel("The logs are here:")
        self.log_area = JTextArea()
        self.log_pane = JScrollPane(self.log_area)
        self.log_area.setLineWrap(True)
        self.log_pane.setViewportView(self.log_area)

        layout = GroupLayout(self.panel)
        self.panel.setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)



        layout.setHorizontalGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                  .addGap(15)
                                  .addGroup(layout.createSequentialGroup()
                                            .addComponent(self.url_label)
                                            .addComponent(self.url_field, GroupLayout.PREFERRED_SIZE,
                                                          GroupLayout.PREFERRED_SIZE, 300)
                                            .addComponent(self.apply_button)
                                            )
                                  .addGap(30)
                                  .addComponent(self.log_label)
                                  .addComponent(self.log_area, GroupLayout.PREFERRED_SIZE,
                                                GroupLayout.PREFERRED_SIZE, 700)
                                  )

        layout.setVerticalGroup(layout.createSequentialGroup()
                                .addGap(15)
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                          .addComponent(self.url_label)
                                          .addComponent(self.url_field, GroupLayout.PREFERRED_SIZE, 30,
                                                        GroupLayout.PREFERRED_SIZE)
                                          .addComponent(self.apply_button)
                                          )
                                .addGap(30)
                                .addComponent(self.log_label)
                                .addComponent(self.log_area, GroupLayout.PREFERRED_SIZE, 700,
                                              GroupLayout.PREFERRED_SIZE)
                                )
        return

    def getTabCaption(self):
        return "Swagger to SiteMap"

    def getUiComponent(self):
        return self.panel

    def load_site_map(self, event):
        url_value = self.url_field.text
        swagger_dict = get_swagger_json(self, url_value)
        self.burp_extender_object.create_site_map(swagger_dict)
