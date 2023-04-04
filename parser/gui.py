import base64
import json
from java.awt import Dimension
from javax.swing import JPanel, JButton, JLabel, SwingConstants, JTextField, JTextArea, GroupLayout, JScrollPane
from javax.swing import JFileChooser, PopupFactory, JOptionPane
from java.io import BufferedReader, FileReader
from java.util.stream import Collectors
from burp import ITab
from api_to_swagger import get_swagger_json
import datetime
import regex_matcher


# The class responsible for creating the graphical shell in Burp Suit
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
        self.upload_label = JLabel('If you need upload a file with json, PUSH THE BUTTON --->')
        self.upload_button = JButton('UPLOAD', actionPerformed=self.upload_file)

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
                                            .addGroup(layout.createSequentialGroup()
                                                      .addComponent(self.upload_label)
                                                      .addComponent(self.upload_button)
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
                                          .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                                    .addComponent(self.upload_label)
                                                    .addComponent(self.upload_button)
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

    # This method returns the caption that should appear on the custom tab when it is displayed
    def getTabCaption(self):
        return "Swagger to SiteMap"

    # This method to obtain the component that should be used as the contents of the custom tab when it is displayed
    def getUiComponent(self):
        return self.panel

    # This method passes the data received and converted from the graphical shell to the method that creates the SiteMap
    # in Burp Suite
    def load_site_map(self, event):
        authorization = self.create_authorization_credentials()
        url_value = self.url_field.text
        swagger_dict = get_swagger_json(self, url_value, authorization)
        self.burp_extender_object.create_site_map(swagger_dict, url_value, authorization)

    # The method displays logs on the graphical UI
    def set_log(self, message):
        self.log_area.getDocument().insertString(0, message, None)
        self.log_area.setCaretPosition(0)

    # The method implements the file loading mechanism on the graphical UI
    def upload_file(self, event):
        authorization = self.create_authorization_credentials()
        file_chooser = JFileChooser()
        option = file_chooser.showOpenDialog(self.panel)
        if option == JFileChooser.APPROVE_OPTION:
            file = file_chooser.getSelectedFile()
            self.set_log('File selected: ' + file.getName() + '\n')
            reader = BufferedReader(FileReader(file))
            json_lines = reader.lines().collect(Collectors.toList())
            for json_value in json_lines:
                self.set_log('\n' + str(datetime.datetime.now()) + '  ***********  '
                             + 'Start parse json_value and create Site Map: \n<------------start------------>\n'
                             + json_value + '\n<-------------end------------->\n')
                json_dir = self.transform_json_to_dir(json_value)
                self.burp_extender_object.create_site_map(json_dir, None, authorization)

    # The method converts the authorization credentials received from the graphical UI into the desired format
    def create_authorization_credentials(self):
        login = self.auth_login_field.text
        password = self.auth_passw_field.text
        if login != '' and password != '':
            message = login + ':' + password
            return base64.b64encode(message.encode('ascii'))
        return ''

    # The method converts the string received from JSON into a dictionary
    def transform_json_to_dir(self, json_str):
        json_dir = None
        try:
            json_dir = json.loads(json_str)
        except ValueError:
            self.set_log('\n' + str(datetime.datetime.now()) + '  ***********  '
                         + 'No JSON object could be decoded\n')
        return json_dir

    # The method implements a popup window mechanism in case the host was not specified earlier
    def create_popup_form(self, message='A Host is absent in the json! Please enter the url of site!'):
        result_popup = JOptionPane.showInputDialog(self.panel, message, None)
        if result_popup is None:
            return ''
        if not regex_matcher.get_host_from_url(result_popup):
            message = 'The url you entered is incorrect or does not match the specified format, sample url format: ' \
                      'http(s)://example.com/. Please enter it again'
            return self.create_popup_form(message)
        return result_popup
