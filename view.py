from kivymd.uix.screen import Screen                        
from kivymd.uix.datatables import MDDataTable              
from kivy.metrics import dp                                
from kivymd.uix.textfield import MDTextField                
from kivymd.uix.boxlayout import MDBoxLayout                
from kivymd.uix.button import MDRaisedButton               
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from datetime import datetime

class View:
    def __init__(self, controller):
        self.controller = controller

        self.title = "Valentine Lorena | Controle Finaçeiro - CDF.py"          

        self.screen = Screen()                                             

        self.tabela = MDDataTable(                          
            background_color_header="#ff048c",
            background_color_selected_cell="#ff7ac2",
            pos_hint = {'center_x':0.5,                   
                        'center_y':0.65},                   
            size_hint=(0.9,0.6),                           
            check = True,                                   
            use_pagination = True,                         
            rows_num = 6,                                   
            pagination_menu_height = '120dp',                
            column_data = [                                 
                ("ID", dp(20)),
                ("Nome", dp(20)),
                ("Valor", dp(30)),
                ("Data d.Gasto", dp(40)),
                ("Quantidade", dp(20))
            ],
            row_data = []                                                
        )


        self.tabela.bind(on_check_press = self.checked)     
        self.tabela.bind(on_row_press=self.on_row_press)
                                   

        self.textfield_codigo = MDLabel(
            text="ID",
            theme_text_color="Hint",
            size_hint_x=None,
            width=60,
            # readonly = True,
            # mode = "rectangle", 
            # max_text_length=0, 
            size_hint_y ="0.1"        
        )                                                  

        self.textfield_nome = MDTextField(
            hint_text="Nome",
            #helper_text="Nome",
            max_text_length=20,
            width=150,
        )

        self.textfield_valor = MDTextField(
            hint_text="Valor",
            #helper_text="Valor",
            max_text_length=15,
            size_hint_x=None,
            width=150,
            input_filter="float",
        )
        
        self.textfield_datadgasto = MDTextField(
            hint_text="Data d.Gasto",
            helper_text="dd/mm/aaaa",
            max_text_length=10,
            width=150,
        )

        self.textfield_quant = MDTextField(
            hint_text="Quantidade",
            #helper_text="Quantidade",
            max_text_length=100,
            width=150,
            input_filter="int",
        )

        data = self.controller.model.get_data()  
        self.update_data_table(data)        

        self.boxLayout1 = MDBoxLayout(spacing="20dp",padding="50dp",pos_hint = {'center_x': 0.5,'center_y':0.65})    
        self.boxLayout1.add_widget(self.textfield_codigo)   
        self.boxLayout1.add_widget(self.textfield_nome)     
        self.boxLayout1.add_widget(self.textfield_valor) 
        self.boxLayout1.add_widget(self.textfield_datadgasto)        
        self.boxLayout1.add_widget(self.textfield_quant) 


        adicionar_button = MDRaisedButton(text="Adicionar") 
        atualizar_button = MDRaisedButton(text="Atualizar") 
        eliminar_button = MDRaisedButton(text="Eliminar")
        soma_button = MDRaisedButton(text="Soma")
        

        self.boxLayout2 = MDBoxLayout(spacing="25dp", padding="55dp")   
        self.boxLayout2.add_widget(adicionar_button)        
        self.boxLayout2.add_widget(atualizar_button)        
        self.boxLayout2.add_widget(eliminar_button)
        self.boxLayout2.add_widget(soma_button)
        
        self.screen.add_widget(self.tabela)                 
        self.screen.add_widget(self.boxLayout1)             
        self.screen.add_widget(self.boxLayout2)

        self.dados_selecionados_linha = None                

        adicionar_button.bind(on_release=self.add_data)
        eliminar_button.bind(on_release=self.delete_data)
        atualizar_button.bind(on_release=self.update_data)
        soma_button.bind(on_release=self.calculate_sum)


    def get_root_widget(self):
        return self.screen
    
    
    

    def checked(self, tabela, linha):
        self.dados_selecionados_linha = linha            
        self.textfield_codigo.text = "ID: "+linha[0]
        self.textfield_nome.text = linha[1]
        self.textfield_valor.text = linha[2]
        self.textfield_datadgasto.text = linha[3]
        self.textfield_quant.text = linha[4]


    def on_row_press(self,a, linha):
            if linha.ids.check.state == "down":
                linha.change_check_state_no_notify("down")            
            else:
                linha.change_check_state_no_notify("normal") 
                self.textfield_codigo.text = "ID: "
                self.textfield_nome.text = ""
                self.textfield_valor.text = ""
                self.textfield_datadgasto.text = ""
                self.textfield_quant.text = "" 

    def is_valid_salary(self, valor): 
        try:
           
            valor_float = float(valor)
            return valor_float >= 0  
        except ValueError:
            return False
        

    def add_data(self, instance):
        nome = self.textfield_nome.text
        valor = self.textfield_valor.text
        datadgasto = self.textfield_datadgasto.text
        quant = self.textfield_quant.text

    
        if not self.is_valid_salary(valor):
            self.show_message("O valor deve ser um número válido.")
            return
        

        try:
            
            data_formatada = datetime.strptime(datadgasto, "%d/%m/%Y")  
           
            datadgasto = data_formatada.strftime("%d/%m/%Y")
        except ValueError:
            self.show_message("A data do gasto deve estar no formato DD/MM/AAAA.")
            return

        if nome and valor and datadgasto and quant :
            valor = float(valor)
            self.controller.insert_data(nome, valor, datadgasto, quant)

        
            data = self.controller.model.get_data()
            self.update_data_table(data)
            self.clear_text_fields()
        else:
            self.show_message("Preencha todos os campos")


    def delete_data(self, instance):
        if self.dados_selecionados_linha:
            id = int(self.dados_selecionados_linha[0])
            self.controller.delete_data(id)

           
            data = self.controller.model.get_data()
            self.update_data_table(data)

            self.clear_text_fields()
        else:
            self.show_message("Selecione um registro para excluir")


    def update_data(self, instance):
        if self.dados_selecionados_linha:
            id = int(self.dados_selecionados_linha[0])
            nome = self.textfield_nome.text
            valor = self.textfield_valor.text
            datadgasto = self.textfield_datadgasto.text
            quant = self.textfield_quant.text

            if not self.is_valid_salary(valor):
                self.show_message("O valor deve ser um número válido.")
                return

            if nome and valor and datadgasto and quant:
                valor = float(valor) 
                self.controller.update_data(id,  nome, valor, datadgasto, quant)

                
                data = self.controller.model.get_data()
                self.update_data_table(data)
                self.clear_text_fields()
            else:
                self.show_message("Preencha todos os campos")
        else:
            self.show_message("Selecione um registro para atualizar")
    
    def calculate_sum(self, instance):
        try:
         
            data = self.controller.model.get_data()  
            total = sum(float(row[2]) for row in data)  

            self.show_message(f"A soma total dos valores é: {total:.2f}")
        except Exception as e:
            self.show_message(f"Erro ao calcular a soma: {str(e)}")



    def show_message(self, message):
        dialog = MDDialog(
            title="Mensagem",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_text_fields(self):
        self.textfield_nome.text = ""
        self.textfield_valor.text = ""
        self.textfield_datadgasto.text = ""
        self.textfield_quant.text = ""
        self.textfield_codigo.text = "ID: "
        self.dados_selecionados_linha = None 

    def update_data_table(self, data):

        self.tabela.row_data = data

    
        self.textfield_codigo.text = "ID: "
        self.textfield_nome.text = ""
        self.textfield_valor.text = ""
        self.textfield_datadgasto.text = ""
        self.textfield_quant.text = ""
        self.dados_selecionados_linha = None   

    