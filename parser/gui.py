import base64

from javax.swing import JPanel, JButton, JLabel, SwingConstants, JTextField, JTextArea, GroupLayout, JScrollPane
from burp import ITab
from api_to_swagger import get_swagger_json
import datetime


class BurpGui(ITab):

    def __init__(self, burp_extender_object):
        self.burp_extender_object = burp_extender_object
        self.panel = JPanel()
        self.apply_button = JButton('Apply', actionPerformed=self.load_site_map)
        self.url_field = JTextField('https://petstore.swagger.io/v2/swagger.json', 30)
        self.log_pane = JScrollPane()
        self.url_label = JLabel("Enter the url of swagger:", SwingConstants.RIGHT)
        self.log_label = JLabel("The logs are here:")
        self.log_area = JTextArea()
        self.log_area.setLineWrap(True)
        self.log_pane.setViewportView(self.log_area)
        self.auth_label = JLabel("If need Authorization header with some credentials, fill out the fields below "
                                 "- login and password!")
        self.auth_login_label = JLabel("Login: ")
        self.auth_login_field = JTextField('', 20)
        self.auth_passw_label = JLabel("Password: ")
        self.auth_passw_field = JTextField('', 20)

        layout = GroupLayout(self.panel)
        self.panel.setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)

        layout.setHorizontalGroup(layout.createSequentialGroup()
                                  .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                            .addGap(15)
                                            .addGroup(layout.createSequentialGroup()
                                                      .addComponent(self.url_label)
                                                      .addComponent(self.url_field, GroupLayout.PREFERRED_SIZE,
                                                                    GroupLayout.PREFERRED_SIZE, 300)
                                                      .addComponent(self.apply_button)
                                                      )
                                            .addGap(30)
                                            .addComponent(self.log_label)
                                            .addComponent(self.log_pane, GroupLayout.PREFERRED_SIZE,
                                                          GroupLayout.PREFERRED_SIZE, 700)
                                            )
                                  .addGap(30)
                                  .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                            .addGap(15)
                                            .addComponent(self.auth_label)
                                            .addGap(15)
                                            .addComponent(self.auth_login_label)
                                            .addComponent(self.auth_login_field, GroupLayout.PREFERRED_SIZE,
                                                          GroupLayout.PREFERRED_SIZE, 20)
                                            .addComponent(self.auth_passw_label)
                                            .addComponent(self.auth_passw_field, GroupLayout.PREFERRED_SIZE,
                                                          GroupLayout.PREFERRED_SIZE, 20)
                                            )

                                  )

        layout.setVerticalGroup(layout.createParallelGroup()
                                .addGroup(layout.createSequentialGroup()
                                          .addGap(15)
                                          .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                                    .addComponent(self.url_label)
                                                    .addComponent(self.url_field, GroupLayout.PREFERRED_SIZE, 30,
                                                                  GroupLayout.PREFERRED_SIZE)
                                                    .addComponent(self.apply_button)
                                                    )
                                          .addGap(30)
                                          .addComponent(self.log_label)
                                          .addComponent(self.log_pane, GroupLayout.PREFERRED_SIZE, 700,
                                                        GroupLayout.PREFERRED_SIZE)
                                          )
                                .addGap(30)
                                .addGroup(layout.createSequentialGroup()
                                          .addGap(15)
                                          .addComponent(self.auth_label)
                                          .addGap(15)
                                          .addComponent(self.auth_login_label)
                                          .addComponent(self.auth_login_field, GroupLayout.PREFERRED_SIZE, 20,
                                                        GroupLayout.PREFERRED_SIZE)
                                          .addComponent(self.auth_passw_label)
                                          .addComponent(self.auth_passw_field, GroupLayout.PREFERRED_SIZE, 20,
                                                        GroupLayout.PREFERRED_SIZE)
                                          )
                                )
        return

    def getTabCaption(self):
        return "Swagger to SiteMap"

    def getUiComponent(self):
        return self.panel

    def load_site_map(self, event):
        login = self.auth_login_field.text
        password = self.auth_passw_field.text
        authorization = ''
        url_value = self.url_field.text
        if login != '' and password != '':
            message = login + ':' + password
            authorization = base64.b64encode(message.encode('ascii'))
        swagger_dict = get_swagger_json(self, url_value, authorization)
        self.burp_extender_object.create_site_map(swagger_dict, url_value, authorization)

    def set_log(self, message):
        self.log_area.getDocument().insertString(0, message, None)
        self.log_area.setCaretPosition(0)
