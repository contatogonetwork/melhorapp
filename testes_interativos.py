# testes_interativos.py
# Execute com: python testes_interativos.py

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import importlib

class TestRunner:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.test_results = {}
        
    def run_test(self, test_name, test_function):
        print(f"Executando teste: {test_name}")
        try:
            result = test_function()
            self.test_results[test_name] = result
            print(f"✓ Teste concluído: {test_name}")
            return True
        except Exception as e:
            print(f"✗ Teste falhou: {test_name}")
            print(f"  Erro: {str(e)}")
            self.test_results[test_name] = False
            return False
    
    def test_login_functionality(self):
        """Testa o fluxo de login"""
        try:
            from gui.login_dialog import LoginDialog
            
            login = LoginDialog()
            login.show()
            
            QMessageBox.information(
                None, 
                "Teste Interativo", 
                "Teste de login aberto.\n\n"
                "1. Digite 'admin' e senha 'admin123'\n"
                "2. Clique em Login\n"
                "3. Verifique se o login é bem-sucedido\n\n"
                "Clique OK para continuar."
            )
            
            return True
        except Exception as e:
            raise Exception(f"Erro no teste de login: {str(e)}")
    
    def test_main_interface(self):
        """Testa a interface principal"""
        try:
            from gui.main_window import MainWindow
            
            window = MainWindow()
            window.show()
            
            QMessageBox.information(
                None, 
                "Teste Interativo", 
                "Interface principal aberta.\n\n"
                "1. Verifique se todas as abas estão presentes\n"
                "2. Teste a navegação entre abas\n"
                "3. Verifique se o conteúdo de cada aba é carregado\n\n"
                "Clique OK para continuar."
            )
            
            return True
        except Exception as e:
            raise Exception(f"Erro na interface principal: {str(e)}")
    
    def test_event_creation(self):
        """Testa a criação de eventos"""
        try:
            from gui.widgets.event_widget import EventWidget
            
            widget = EventWidget()
            widget.show()
            
            QMessageBox.information(
                None, 
                "Teste Interativo", 
                "Widget de Eventos aberto.\n\n"
                "1. Tente criar um novo evento\n"
                "2. Verifique se o evento é salvo no banco de dados\n"
                "3. Tente editar um evento existente\n\n"
                "Clique OK para continuar."
            )
            
            return True
        except Exception as e:
            raise Exception(f"Erro no widget de eventos: {str(e)}")

    def test_briefing_functionality(self):
        """Testa a funcionalidade de briefing"""
        try:
            from gui.widgets.briefing_widget import BriefingWidget
            
            widget = BriefingWidget()
            widget.show()
            
            QMessageBox.information(
                None, 
                "Teste Interativo", 
                "Widget de Briefing aberto.\n\n"
                "1. Selecione um evento\n"
                "2. Adicione/edite itens de briefing\n"
                "3. Verifique se as alterações são salvas\n\n"
                "Clique OK para continuar."
            )
            
            return True
        except Exception as e:
            raise Exception(f"Erro no widget de briefing: {str(e)}")

    def test_timeline_functionality(self):
        """Testa a funcionalidade de timeline"""
        try:
            from gui.widgets.timeline_widget import TimelineWidget
            
            widget = TimelineWidget()
            widget.show()
            
            QMessageBox.information(
                None, 
                "Teste Interativo", 
                "Widget de Timeline aberto.\n\n"
                "1. Selecione um evento\n"
                "2. Verifique a visualização da timeline\n"
                "3. Tente adicionar/editar itens da timeline\n\n"
                "Clique OK para continuar."
            )
            
            return True
        except Exception as e:
            raise Exception(f"Erro no widget de timeline: {str(e)}")
    
    def run_all_tests(self):
        """Executa todos os testes disponíveis"""
        tests = [
            ("Login", self.test_login_functionality),
            ("Interface Principal", self.test_main_interface),
            ("Criação de Eventos", self.test_event_creation),
            ("Funcionalidade de Briefing", self.test_briefing_functionality),
            ("Funcionalidade de Timeline", self.test_timeline_functionality)
        ]
        
        print("Iniciando testes interativos...")
        
        for name, func in tests:
            success = self.run_test(name, func)
            if not success:
                if QMessageBox.question(
                    None,
                    "Teste Falhou",
                    f"O teste '{name}' falhou. Deseja continuar com os próximos testes?",
                    QMessageBox.Yes | QMessageBox.No
                ) == QMessageBox.No:
                    break
        
        print("\nResultados dos testes:")
        for name, result in self.test_results.items():
            status = "Passou" if result else "Falhou"
            print(f"{name}: {status}")

if __name__ == "__main__":
    runner = TestRunner()
    runner.run_all_tests()
    sys.exit(0)